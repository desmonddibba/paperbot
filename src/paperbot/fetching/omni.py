import requests, logging
from urllib.parse import urlparse, urldefrag
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Paperbot)"
}

MORGONSVEPET_URL = "https://omni.se/upptack?sok=viktigaste+nyheterna+p%C3%A5+tre+minuter"

def fetch_html(url: str) -> str:
    """" Fetch the HTML of a given URL. """
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.text


def fetch_latest_post_url() -> str | None:
    """Fetch the latest Morgonsvepet post URL from Omni."""
    html_content = fetch_html(MORGONSVEPET_URL)
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the canonical link. Filter fetched links to find "Morgonsvepet" newsposts.
    links = soup.find_all("a", href=lambda href: href and "viktigaste-nyheterna" in href)

    if not links:
        logger.warning(
        "No Morgonsvepet links found on Omni page (%s)",
        MORGONSVEPET_URL,
        )
        return None

    # Select the first "Morgonsvepet" link as the latest post
    link_el = links[0]
    url = urldefrag(link_el.get("href"))[0]

    # Make sure the URL is absolute
    if url.startswith("/"):
        parsed = urlparse(MORGONSVEPET_URL)
        url = f"{parsed.scheme}://{parsed.netloc}{url}"

    return url
