import discord
from paperbot.models.morgonsvepet import Morgonsvepet

bullet = "◦"
arrow = "→"

def _format_article_content(paragraphs: list[str]) -> str:
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    if not paragraphs:
        return " " 
    if len(paragraphs) == 1:
        return paragraphs[0]
    
    mid = len(paragraphs) // 2
    first = " ".join(paragraphs[:mid])
    second = " ".join(paragraphs[mid:])

    return f"{first}\n\n{second}"


def create_morgonsvepet_embed(paper: Morgonsvepet) -> discord.Embed:
    embed = discord.Embed(
        title=paper.title,
        url=paper.url,
        description=f"\n\n",
        color=0x78a295,
    )

    embed.set_image(url=paper.image_url)

    for article in paper.articles:
        content = _format_article_content(article.content)

        if article.read_more_link:
            content += f"\n[{arrow} Läs mer]({article.read_more_link})"
        
        embed.add_field(
            name=article.title, 
            value=content or " ", 
            inline=False
            )

    # Add news links
    for news_link in paper.news_links:
        links_text = "\n".join(f"{bullet} [{title}]({url})" for title, url in news_link.items.items())
        if links_text:
            embed.add_field(name=news_link.title, value=links_text, inline=False)

    if paper.daily_watch:
        daily_text = "\n".join(f"{bullet} {item}" for item in paper.daily_watch.items)
        embed.add_field(name=paper.daily_watch.title, value=daily_text, inline=False)

    # footer
    author = paper.author or "Okänd författare"
    date = paper.published_date or "Okänt datum"
    embed.set_footer(
        text=f"{author} — Morgonsvepet {date}"
    )
    return embed