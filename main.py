import time
from models.models import RssSource
from datetime import datetime
from scrapers.KizilayScraper import KizilayScraper
from scrapers.SaglikBakanligiScraper import SaglikBakanligiScraper
from scrapers.IlanGovScraper import IlanGovScraper
import os
import logging

# gRPC / Firestore uyarılarını gizle
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_ENABLE_FORK_SUPPORT"] = "0"
logging.getLogger("google.cloud").setLevel(logging.ERROR)
logging.getLogger("absl").setLevel(logging.ERROR)
logging.getLogger("grpc").setLevel(logging.ERROR)

#InstagramScraper(RssSource("Ali IG", "https://instagram.com/ali")),

if __name__ == "__main__":
    sources = [
       KizilayScraper(RssSource("kızılay","https://basvuru.kizilaykariyer.com/ilan/site.aspx",".GR,.GAR")),
       SaglikBakanligiScraper(RssSource("saglık bakanlıgı","https://www.saglik.gov.tr/TR-99316/personel-duyurulari.html","#ada_TumPersonelHaberleri_items > table  tr")),
       IlanGovScraper(RssSource("ilan.gov.tr","https://www.ilan.gov.tr/api/api/services/app/Ad/AdsByFilter")),
         ]

    while True:
        print(f"--- Kontrol başlıyor {datetime.now()} ---")
        for scraper in sources:
            feeds = scraper.scrape()
            scraper.save_feeds(feeds)

        print("30 dakika uykuya geçiyorum...\n")
        time.sleep(1800)  # 1800 saniye = 30 dakika


  

# i=IlanGovScraper(RssSource("ilan.gov.tr","https://www.ilan.gov.tr/api/api/services/app/Ad/AdsByFilter"))
# feeds=i.scrape()
# i.save_feeds(feeds)