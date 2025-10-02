from datetime import datetime
import time
from models.models import RssSource
# from plyer import notification
from scrapers.IlanGovScraper import IlanGovScraper
from scrapers.KariyerNetScraper import KariyerNetScraper
from scrapers.KizilayScraper import KizilayScraper
from scrapers.SaglikBakanligiScraper import SaglikBakanligiScraper

# scraper importları vs.

if __name__ == "__main__":
    sources = [
       KizilayScraper(RssSource("kızılay","https://basvuru.kizilaykariyer.com/ilan/site.aspx",".GR,.GAR")),
       SaglikBakanligiScraper(RssSource("saglık bakanlıgı","https://www.saglik.gov.tr/TR-99316/personel-duyurulari.html","#ada_TumPersonelHaberleri_items > table  tr")),
       IlanGovScraper(RssSource("ilan.gov.tr","https://www.ilan.gov.tr/api/api/services/app/Ad/AdsByFilter")),
       KariyerNetScraper(RssSource("kariyer.net", "https://candidatesearchapigateway.kariyer.net/search")),
    ]

    while True:
        print(f"--- Kontrol başlıyor {datetime.now()} ---")
        total_new = 0

        for scraper in sources:
            feeds = scraper.scrape()
            scraper.save_feeds(feeds)

        

        print("2 saat uykuya geçiyorum...\n")
        time.sleep(7200)








# i=KariyerNetScraper(RssSource("kariyer.net", "https://candidatesearchapigateway.kariyer.net/search"))
# feeds=i.scrape()
# i.save_feeds(feeds)



# i=KariyerNetScraper(RssSource("kariyer.net", "https://candidatesearchapigateway.kariyer.net/search"))
# feeds=i.deleteRssSource(i.source)


