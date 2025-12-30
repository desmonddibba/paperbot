import requests
from urllib.parse import urlparse, urldefrag
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Paperbot)"
}


MORGONSVEPET_URL = "https://omni.se/upptack?sok=viktigaste+nyheterna+p%C3%A5+tre+minuter"

def fetch_html(url: str) -> str:
    """" Fetch the HTML of a given"""
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.text


# TODO: Set up a filter to only fetch valid URL's from searchquery. (Morgonsvepet newsposts, NOT paid articles etc)
def fetch_latest_post_url() -> str | None:
    """Fetch the latest Morgonsvepet post URL from Omni."""
    html_content = fetch_html(MORGONSVEPET_URL)
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the canonical link
    link_el = soup.find("a", rel="canonical")
    if not link_el:
        return None

    url = urldefrag(link_el.get("href"))[0]

    # Make sure the URL is absolute
    if url.startswith("/"):
        parsed = urlparse(MORGONSVEPET_URL)
        url = f"{parsed.scheme}://{parsed.netloc}{url}"

    return url
