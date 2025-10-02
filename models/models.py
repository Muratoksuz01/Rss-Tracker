
from dataclasses import dataclass
from datetime import datetime

# ── Kaynak tanımı ────────────────────────────────
class RssSource:
    def __init__(self, name, url, selector=None):
        self.name = name
        self.url = url
        self.selector = selector

# ── Feed modeli ──────────────────────────────────
@dataclass
class Feed:
    source: RssSource
    content: str
    url: str
    pub_date: datetime
    image: str | None = None
    location:str | None = None



