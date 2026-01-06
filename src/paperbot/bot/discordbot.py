import logging
import discord
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()


TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    logger.info('%s has connected to Discord!' % client.user)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.lower() == 'ping':
        await message.channel.send("Pong!")

def run_discordbot():
    client.run(TOKEN, log_handler=None)

