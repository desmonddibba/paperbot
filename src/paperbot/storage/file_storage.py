import json, logging
from pathlib import Path

logger = logging.getLogger(__name__)

class FileStorage:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self._seen: set[str] = set()
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            logger.info("Storage file does not exist, starting fresh: %s", self.path)
            return
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            self._seen = set(data)
        except Exception:
            logger.exception("Failed to load storage file, starting empty")
            self._seen = set()

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(sorted(self._seen), indent=2),
            encoding="utf-8"
        )

    def has_seen(self, url: str) -> bool:
        return url in self._seen
    
    def mark_seen(self, url: str) -> None:
        if url in self._seen:
            return
        
        self._seen.add(url)
        self._save()
        logger.debug("Marked URL as seen: %s", url)


