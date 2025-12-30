import requests
from urllib.parse import urlparse, urldefrag
from lxml import html

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Paperbot)"
}



MORGONSVEPET_URL = "https://omni.se/upptack?sok=viktigaste+nyheterna+p%C3%A5+tre+minute"


def fetch_html(url: str) -> html.HtmlComment:
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return html.fromstring(response.content)


def fetch_latest_post_url() -> str | None:
    response = requests.get(MORGONSVEPET_URL, headers=HEADERS, timeout=10)
    response.raise_for_status()

    tree = html.fromstring(response.content)
    links = tree.xpath("//a[@rel='canonical']/@href")

    if not links:
        return None
    
    url = urldefrag(links[0])[0]

    if url.startswith("/"):
        parsed = urlparse(MORGONSVEPET_URL)
        url = f"{parsed.scheme}://{parsed.netloc}{url}"

    return url
