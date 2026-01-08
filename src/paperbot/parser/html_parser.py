from urllib.parse import urljoin
from paperbot.models.morgonsvepet import Article, DailyWatch, NewsLink, Morgonsvepet
from bs4 import BeautifulSoup
from paperbot.fetching.omni import fetch_html
import logging
from typing import List

logger = logging.getLogger(__name__)

def parse_morning_letter(url: str) -> Morgonsvepet:
    """Parse the articles section of the morning letter.
    Args:
        url (str): The URL of the Morgonsvepet post.
    Returns:
        Morgonsvepet: The parsed Morgonsvepet object.
    """
    html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")

    morgon = Morgonsvepet(
        title=soup.select_one("h1[class*='Title_articleTitle']").get_text(strip=True),
        url=url,
        author=soup.select_one("div[class*='Byline']").select_one("span").get_text(strip=True),
        published_date=soup.select_one("time[class*='Timestamp']").get_text(strip=True),
    )
    paid_article_subheading = None

    # Find all subheadings
    subheading_els = soup.select("h2[class*='SubHeading']")

    # Iterate through subheadings and collect content
    for subheading_el in subheading_els:
        if paid_article_subheading and subheading_el.get_text(strip=True).lower() == paid_article_subheading:
            logger.debug(f"Skipping paid article section: {paid_article_subheading}")
            paid_article_subheading = None
            continue

        subheading_text = subheading_el.get_text(strip=True)
        
        # Skip the "Till sist" section
        if subheading_text == "Till sist":
            continue

        # Fler nyheter i korthet
        if subheading_text == "Fler nyheter i korthet":
            items = {}
            for sibling in subheading_el.find_next_siblings():
                if sibling.name == "div" and any('InternalArticle' in cls for cls in sibling.get('class', [])):   
                    link_el = sibling.find("a", href=True)
                    if link_el:
                        article_title = link_el.find("span").get_text(strip=True)
                        items[article_title] = urljoin(url, link_el['href'])

                if sibling.name == "h2" and any('SubHeading' in cls for cls in sibling.get('class', [])):
                    paid_article_subheading = sibling.get_text(strip=True).lower()
                    logger.debug(f"Found paid article subheading: {paid_article_subheading}")
                    break

            morgon.news_links.append(NewsLink(items=items))
            continue

        # Håll utkik under dagen
        if subheading_text == "Håll utkik under dagen":
            li_items = []
            for sibling in subheading_el.find_next_siblings():

                if sibling.name == "h2" and any('SubHeading' in cls for cls in sibling.get('class', [])):
                    break

                for li in sibling.find_all("li"):
                    text = li.get_text(strip=True)
                    if text:
                        li_items.append(text)

            morgon.daily_watch = DailyWatch(title=subheading_text, items=li_items)
            continue
        
        # Articles
        content: List[str] = []
        read_more_link: str = None

        for sibling in subheading_el.find_next_siblings():
            if sibling.name == "h2" and any('SubHeading' in cls for cls in sibling.get('class', [])):
                break

            # Check for paragraphs
            if sibling.name == "div" and any('Text' in cls for cls in sibling.get('class', [])):
                paragraphs = sibling.find_all("p")
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    if text:
                        content.append(text)

            # Check for "Read more" links
            if sibling.name == "div" and any('InternalArticle' in cls for cls in sibling.get('class', [])):
                link_el = sibling.find("a", href=True)
                if link_el:
                    read_more_link = urljoin(url, link_el['href'])
        
        morgon.articles.append(Article(
            title=subheading_text,
            content=content,
            read_more_link=read_more_link
        ))

    return morgon