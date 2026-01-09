from typing import Callable
from paperbot.fetching.robots import RobotsChecker
from paperbot.models.morgonsvepet import Morgonsvepet
import logging

logger = logging.getLogger(__name__)

class PaperBotService:
    def __init__(
        self,
        storage,
        fetcher: Callable[[], str],
        parser: Callable[[str], Morgonsvepet]
    ):
        self.storage = storage
        self.fetcher = fetcher
        self.parser = parser

    def mark_seen(self, url: str) -> None:
        self.storage.mark_seen(url)
    
    def has_seen(self, url: str) -> bool:
        return self.storage.has_seen(url)
    
    def fetch_paper(self) -> Morgonsvepet:
        url = self.fetcher()

        if not RobotsChecker.can_fetch(url):
            logger.warning(f"Skipping {url}: disallowed by robots.txt")
            return None

        if self.has_seen(url):
            logger.info(f"URL already seen: {url}")
            return None
            
        self.mark_seen(url)
        logger.info("New URL marked: {url}")
        return self.parser(url)

