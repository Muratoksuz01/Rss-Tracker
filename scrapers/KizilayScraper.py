from datetime import datetime
import requests as rq
from bs4 import BeautifulSoup
from typing import List
from urllib.parse import urljoin

from core.FeedScraper import FeedScraper
from models.models import Feed, RssSource

class KizilayScraper(FeedScraper):
    
    def __init__(self, rss_source: RssSource):
        super().__init__()
        self.source = rss_source

    def scrape(self) -> List[Feed]:
        print(f"Kızılay kontrol ediliyor: {self.source.name}")

        # 1. HTTP isteği
        try:
            resp = rq.get(self.source.url, timeout=10,headers=self.headers)
            resp.raise_for_status()
        except Exception as e:
            print(f"❌ İstek hatası: {e}")
            return []

        # 2. HTML parse
        soup = BeautifulSoup(resp.text, "html.parser")

        # 3. İlan satırlarını seç (.GR ve .GAR)
        rows = soup.select(self.source.selector)   # örn: ".GR, .GAR"
        feeds: List[Feed] = []

        for row in rows:
            # ilan başlığı <a> etiketinden
            a_tag = row.find("a", class_="GL")
            if not a_tag:
                continue

            content = a_tag.get_text(strip=True)
            href = a_tag.get("href")

            # Linki tam URL yap (çünkü href /3azs... şeklinde relative geliyor)
            full_link = urljoin(self.source.url, href)

         
            pub_date = datetime.now()

            feeds.append(
                Feed(
                    source=self.source,
                    content=content,
                    url=full_link,
                    pub_date=pub_date
                )
            )

        print(f"✅ {len(feeds)} ilan bulundu.")
        return feeds
