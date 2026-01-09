import asyncio
import datetime
import logging
import discord
import os
from discord.ext import tasks
from dotenv import load_dotenv
from paperbot.bot.embed import create_morgonsvepet_embed
from paperbot.fetching.omni import fetch_latest_post_url
from paperbot.parser.html_parser import parse_morning_letter
from paperbot.storage.file_storage import FileStorage
from paperbot.services.paperbotservice import PaperBotService
from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_IDS = [int(cid.strip()) for cid in os.getenv("DISCORD_CHANNEL_IDS").split(",")]

intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)

storage = FileStorage("data/urls.json")
paper_service = PaperBotService(
    storage=storage,
    fetcher=fetch_latest_post_url,
    parser=parse_morning_letter
)

TIMEZONE = ZoneInfo("Europe/Stockholm")
RETRY_INTERVAL = 5 # minutes
TARGET_HOUR = 7 # 07:00

@tasks.loop(minutes=RETRY_INTERVAL)
async def morning_news_loop():
    try:
        paper = paper_service.fetch_paper()
        if paper is None:
            logger.info("No new post. Retrying in 10 minutes.")
            return
        
        # Post embed to discord
        embed = create_morgonsvepet_embed(paper)
        for channel_id in CHANNEL_IDS:
            channel = client.get_channel(channel_id) or await client.fetch_channel(channel_id)
            await channel.send(embed=embed)
            logger.info(f"Posted news: Morgonsvepet {paper.published_date} to channel {channel_id}")
        morning_news_loop.stop()

    except discord.Forbidden:
        logger.warning("Missing permission to post in one of the channels")
    except Exception as e:
        logger.warning(f"Unexpected error in morning_news_loop: {e}")

@tasks.loop(hours=24)
async def daily_restart_loop():
    morning_news_loop.start()

@daily_restart_loop.before_loop
async def before_daily_restart():
    await client.wait_until_ready()
    now = datetime.datetime.now(TIMEZONE)
    target = now.replace(hour=TARGET_HOUR, minute=0, second=0, microsecond=0)
    if now >= target:
        target += datetime.timedelta(days=1)
        logger.info(f"Sleeping until {target}")
    await asyncio.sleep((target - now).total_seconds())

@client.event
async def on_ready():
    logger.info('%s has connected to Discord!' % client.user)
    for channel_id in CHANNEL_IDS:
        channel = client.get_channel(channel_id)
        logger.info(f"Channel {channel_id}: {channel}")
    morning_news_loop.start()
    daily_restart_loop.start()

def run_discordbot():
    client.run(TOKEN, log_handler=None)

