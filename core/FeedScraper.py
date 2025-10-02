from abc import ABC, abstractmethod
from datetime import datetime
import os
from google.cloud import firestore
# from plyer import notification
from models.models import Feed, RssSource
import requests
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / "config" / ".env"
load_dotenv(dotenv_path=env_path)

class FeedScraper(ABC):
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    def __init__(self):
        # Firestore client
        self.db = firestore.Client()

    @abstractmethod
    def scrape(self) -> list[Feed]:
        ...

    def notify(self, feed: Feed):
        if not self.TELEGRAM_BOT_TOKEN or not self.TELEGRAM_CHAT_ID:
            print("Telegram ayarı yok, bildirim atlanıyor.")
            return

        msg = (
            f"📢 Yeni içerik!\n\n"
            f"📰 Kaynak: {feed.source.name}\n"
            f"🔗 {feed.url}\n"
            f"➕ {feed.content}"
            f"{'📍 ' + feed.location if feed.location else ''}"

        )
        try:
            r = requests.post(
                f"https://api.telegram.org/bot{self.TELEGRAM_BOT_TOKEN}/sendMessage",
                data={"chat_id": self.TELEGRAM_CHAT_ID, "text": msg}
            )
            r.raise_for_status()
            print(f"Telegram bildirimi gitti → {feed.source.name}")
            
            """ if len(feed) > 0 and False: # true yaparsan windows bildirmi alırsın 
                notification.notify(
                    title="RSS Takip Botu",
                    message=f" {feed.source.name}'de {len(feed)} adet yeni içerik bulundu!",
                    app_name="RSS Tracker",
                    timeout=10
                ) """
        except Exception as e:
            print("Telegram hatası:", e)

    def save_feeds(self, feeds: list[Feed]):
        if not feeds:
            print("Kaydedilecek feed yok.")
            return

        try:
            # kaynak (source) için dokümanı al ya da oluştur
            src = feeds[0].source
            src_query = (
                self.db.collection("rss_sources")
                .where("name", "==", src.name)
                .where("url", "==", src.url)
                .limit(1)
                .get()
            )

            if src_query:
                source_doc = src_query[0]
                source_id = source_doc.id
                source_name=source_doc.get("name") 
                # last_refreshed güncelle
                self.db.collection("rss_sources").document(source_id).update({
                    "last_refreshed": datetime.utcnow().isoformat()
                })
            else:
                new_doc = self.db.collection("rss_sources").document()
                new_doc.set({
                    "name": src.name,
                    "url": src.url,
                    "selector": src.selector,
                    "last_refreshed": datetime.utcnow().isoformat()
                })
                source_id = new_doc.id
                source_name=src.name
                print(f"[KAYNAK EKLENDİ] {src.name}")

            for feed in feeds:
                # feed zaten kayıtlı mı kontrol et (feed_url + source_id ile)
                dup_check = (
                    self.db.collection("rss_contents")
                    .where("source_id", "==", source_id)
                    .where("feed_url", "==", feed.url)
                    .limit(1)
                    .get()
                )

                if dup_check:
                    # zaten varsa atla
                    print(f"[ZATEN VAR] {feed.url}")
                    continue

                # yeni feed ekle
                self.db.collection("rss_contents").add({
                    "source_id": source_id,
                    "source_name":source_name,
                    "content": feed.content,
                    "feed_url": feed.url,
                    "pub_date": feed.pub_date.isoformat(),
                    "image": feed.image or None ,
                    "location":feed.location or None
                    # "created_at": datetime.utcnow().isoformat()
                })
                print(f"[YENİ İÇERİK] {feed.url}")
                self.notify(feed)

        except Exception as e:
            print("Kayıt hatası:", e)


    def deleteRssSource(self, source: RssSource):
        """
        Verilen source name'e göre Firestore'dan RSS kaynağını ve
        ona bağlı tüm içerikleri siler.
        """
        try:
            # Önce kaynağı bul
            src_query = (
                self.db.collection("rss_sources")
                .where("name", "==", source.name)
                .limit(1)
                .get()
            )

            if not src_query:
                print(f"[BİLGİ] '{source.name}' adında bir kaynak bulunamadı.")
                return

            source_doc = src_query[0]
            source_id = source_doc.id

            # Kaynağa bağlı içerikleri sil
            contents_query = (
                self.db.collection("rss_contents")
                .where("source_id", "==", source_id)
                .stream()
            )

            deleted_count = 0
            for content in contents_query:
                self.db.collection("rss_contents").document(content.id).delete()
                deleted_count += 1

            # Kaynağı sil
            self.db.collection("rss_sources").document(source_id).delete()

            print(f"[OK] '{source.name}' kaynağı ve {deleted_count} içerik silindi.")

        except Exception as e:
            print(f"[HATA] '{source.name}' kaynağı silinirken hata: {e}")
