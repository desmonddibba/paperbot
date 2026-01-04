from bs4 import BeautifulSoup
from paperbot.fetching.omni import fetch_html, fetch_latest_post_url


def parse_morning_letter():
    url = fetch_latest_post_url()
    html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")

    # Title
    title_el = soup.select_one("h1[class*='Title_articleTitle']")
    title = title_el.get_text(strip=True) if title_el else None

    # Subheading
    subheading_el = soup.select_one("h2[class*='SubHeading']")
    subheading = subheading_el.get_text(strip=True) if subheading_el else None


    return {
        "title": title,
        "subheading": subheading,
        "url": url
    }
