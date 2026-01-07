from dataclasses import dataclass, field
from typing import Dict, Optional, List

@dataclass
class Morgonsvepet:
    title: str
    articles: List['Article'] = field(default_factory=list)
    news_links: List['NewsLink'] = field(default_factory=list)
    daily_watch: Optional['DailyWatch'] = None
    author: Optional[str] = None
    published_date: Optional[str] = None
    url: Optional[str] = None

@dataclass
class Article:
    title: str
    content: List[str] = field(default_factory=list)
    read_more_link: Optional[str] = None

@dataclass
class NewsLink:
    items: Dict[str, str] = field(default_factory=dict)

@dataclass
class DailyWatch:
    title: str
    items: List[str] = field(default_factory=list)
