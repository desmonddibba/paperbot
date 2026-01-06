from urllib.parse import urljoin
from bs4 import BeautifulSoup
from paperbot.fetching.omni import fetch_html, fetch_latest_post_url
import logging


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def parse_morning_letter():
    url = fetch_latest_post_url()
    html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")

    content_sections = []

    # Title "Viktigaste nyheterna på tre minuter"
    title_el = soup.select_one("h1[class*='Title_articleTitle']")
    title = title_el.get_text(strip=True) if title_el else None

    # Find all subheadings
    subheading_els = soup.select("h2[class*='SubHeading']")
    

    # Iterate through subheadings and collect content
    for subheading_el in subheading_els:
        section = {
            "subheading": subheading_el.get_text(strip=True),
            "content": [],
            "read_more_link": None
        }

        subheading_text = subheading_el.get_text(strip=True).lower()

        # Skip the "Till sist" section
        if subheading_text == "till sist":
            continue

        # Collect content until the next subheading
        for sibling in subheading_el.find_next_siblings():
            if sibling.name == "h2" and any('SubHeading' in cls for cls in sibling.get('class', [])):
                break

            # Check for paragraphs
            if sibling.name == "div" and any('Text' in cls for cls in sibling.get('class', [])):
                paragraphs = sibling.find_all("p")
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    if text:
                        section["content"].append(text)
                        section["content"].append("\n")

            # Check for "Read more" links
            if sibling.name == "div" and any('InternalArticle' in cls for cls in sibling.get('class', [])):
                link_el = sibling.find("a", href=True)
                if link_el:
                    section["read_more_link"] = urljoin(url, link_el['href'])

        content_sections.append(section)

    return content_sections
