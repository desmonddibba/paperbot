from typing import Callable
from paperbot.models.morgonsvepet import Morgonsvepet

class PaperBotService:
    def __init__(
        self,
        repository,
        fetcher: Callable[[], str],
        parser: Callable[[str], Morgonsvepet]
    ):
        self.repository = repository
        self.fetcher = fetcher
        self.parser = parser

    def mark_seen(self, url: str) -> None:
        self.repository.mark_seen(url)
    
    def has_seen(self, url: str) -> bool:
        return self.repository.has_seen(url)
    
    def fetch_paper(self) -> Morgonsvepet:
        url = self.fetcher()
        if not self.has_seen(url):
            self.mark_seen(url)
        return self.parser(url)
