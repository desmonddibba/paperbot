import logging
import discord
import os
from dotenv import load_dotenv
from paperbot.fetching.omni import fetch_latest_post_url
from paperbot.models.morgonsvepet import Morgonsvepet
from paperbot.parser.html_parser import parse_morning_letter
from paperbot.storage.file_storage import FileStorage
from paperbot.services.paperbotservice import PaperBotService
from discord.ext import commands

logger = logging.getLogger(__name__)
bullet = "•"
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)

storage = FileStorage("data/urls.json")

paper_service = PaperBotService(
    storage=storage,
    fetcher= fetch_latest_post_url,
    parser=parse_morning_letter
)

def create_embed(paper: Morgonsvepet) -> discord.Embed:
    embed = discord.Embed(
        title=paper.title,
        url=paper.url,
        description=f"By {paper.author or 'Unknown'} | Published: {paper.published_date or 'Unknown'}",
        color=0x1abc9c
    )

    for article in paper.articles:
        content = "\n".join(article.content)

        if article.read_more_link:
            content += f"\n[Läs mer]({article.read_more_link})"
        
        embed.add_field(name=article.title, value=content or "No content", inline=False)

    # Add news links
    for news_link in paper.news_links:
        links_text = "\n".join(f"{bullet} [{title}]({url})" for title, url in news_link.items.items())
        if links_text:
            embed.add_field(name="Fler nyheter i korthet", value=links_text, inline=False)

    if paper.daily_watch:
        daily_text = "\n".join(f"{bullet} {item}" for item in paper.daily_watch.items)
        embed.add_field(name=paper.daily_watch.title, value=daily_text, inline=False)

    # footer
    embed.set_footer(text="Morgonsvepet")

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

