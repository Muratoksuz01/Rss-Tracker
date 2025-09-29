from datetime import datetime
import core.FeedScraper as FeedScraper
from models.models import Feed, RssSource


class InstagramScraper(FeedScraper):
    def __init__(self, rss_source: RssSource):
        super().__init__()
        self.source = rss_source

    def scrape(self) -> list[Feed]:
        # burada gerçek scraping olacak
        self.notify()        
        print(f"Instagram kontrol: {self.source.name}")
        return [Feed(
            source=self.source,
            content="Yeni Instagram gönderisi",
            url="https://instagram.com/somepost",
            pub_date=datetime.now()
        )]