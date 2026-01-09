from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

class RobotsChecker:
    _parsers: dict[str, RobotFileParser] = {}

    @classmethod
    def can_fetch(cls, url:str, user_agent: str = "*") -> bool:
        """
            Checks robots.txt to see if the URL can be fetched.

        """
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"

        if base_url not in cls._parsers:
            parser = RobotFileParser()
            parser.set_url(f"{base_url}/robots.txt")
            try:
                parser.read()
            except Exception as e:
                parser = None
                
            cls._parsers[base_url] = parser

        parser = cls._parsers[base_url]
        if parser is None:
            return True
        return parser.can_fetch(user_agent, url)