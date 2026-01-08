import logging
import discord
import os
from dotenv import load_dotenv
from paperbot.fetching.omni import fetch_latest_post_url
from paperbot.models.morgonsvepet import Morgonsvepet
from paperbot.parser.html_parser import parse_morning_letter
from paperbot.storage.file_storage import FileStorage
from paperbot.services.paperbotservice import PaperBotService

logger = logging.getLogger(__name__)
bullet = "◦"
arrow = "→"
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)

storage = FileStorage("data/urls.json")

paper_service = PaperBotService(
    storage=storage,
    fetcher=fetch_latest_post_url,
    parser=parse_morning_letter
)

def format_article_content(paragraphs: list[str]) -> str:
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    if not paragraphs:
        return " "
    
    if len(paragraphs) == 1:
        return paragraphs[0]

    mid = len(paragraphs) // 2

    first = " ".join(paragraphs[:mid])
    second = " ".join(paragraphs[mid:])

    return f"{first}\n\n{second}"

def create_embed(paper: Morgonsvepet) -> discord.Embed:
    embed = discord.Embed(
        title=paper.title,
        url=paper.url,
        description=f"\n",
        color=0x78a295,
    )

    embed.set_image(url=paper.image_url)

    for article in paper.articles:
        content = format_article_content(article.content)

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
            embed.add_field(name="Fler nyheter i korthet", value=links_text, inline=False)

    if paper.daily_watch:
        daily_text = "\n".join(f"{bullet} {item}" for item in paper.daily_watch.items)
        embed.add_field(name=paper.daily_watch.title, value=daily_text, inline=False)

    # footer
    author = paper.author or "Okänd författare"
    date = paper.published_date or "Okänt datum"

    embed.set_footer(
        text=f"{author} — Morgonsvepet {date} "
    )

    return embed

@client.event
async def on_ready():
    logger.info('%s has connected to Discord!' % client.user)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.lower() == 'ping':
        paper = paper_service.fetch_paper()
        if paper:
            embed = create_embed(paper)
            await message.channel.send(embed=embed)

def run_discordbot():
    client.run(TOKEN, log_handler=None)

