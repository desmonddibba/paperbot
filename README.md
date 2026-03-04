# Paperbot

A Discord bot that automatically fetches and shares the latest **Morgonsvepet** (Morning Letter) posts to configured Discord channels.

## Overview

Paperbot is a Python-based Discord bot that:
- Fetches the latest Morgonsvepet posts at scheduled times (default: 6 AM Stockholm time)
- Parses the HTML content to extract articles, news links, and daily insights
- Posts formatted embeds to Discord channels
- Tracks seen URLs to avoid duplicate postings
- Respects `robots.txt` rules for ethical web scraping

## Features

- **Scheduled Posting**: Automatically posts the morning letter at a configurable time
- **Intelligent Caching**: Tracks previously posted URLs to prevent duplicates
- **Rich Formatting**: Creates visually appealing Discord embeds with article summaries
- **Robots.txt Compliance**: Checks and respects website crawling rules
- **Multi-Channel Support**: Posts to multiple Discord channels simultaneously
- **Error Handling**: Graceful error handling and comprehensive logging

## Requirements

- Python 3.8+
- Discord.py 2.6.4+
- BeautifulSoup4 for HTML parsing
- python-dotenv for environment configuration

See `requirements.txt` for the complete dependency list.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/desmonddibba/paperbot.git
cd paperbot
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
DISCORD_TOKEN=your_discord_bot_token_here
DISCORD_CHANNEL_IDS=channel_id_1,channel_id_2,channel_id_3
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `DISCORD_TOKEN` | Your Discord bot token from the Developer Portal |
| `DISCORD_CHANNEL_IDS` | Comma-separated list of Discord channel IDs where the bot should post |

## Usage

Run the bot with:

```bash
python -m paperbot
```

The bot will:
1. Connect to Discord
2. Start a scheduled loop that checks for new posts every 5 minutes
3. When a new post is found, post it to all configured channels
4. Continue running until stopped

## Architecture

### Project Structure

```
src/paperbot/
├── __main__.py           # Entry point
├── bot/
│   ├── discordbot.py    # Discord bot client and main loop
│   └── embed.py         # Discord embed formatting
├── fetching/
│   ├── omni.py          # Fetches latest post URLs
│   └── robots.py        # Robots.txt compliance checker
├── models/
│   └── morgonsvepet.py  # Data models for parsed content
├── parser/
│   └── html_parser.py   # HTML parsing logic
├── services/
│   └── paperbotservice.py # Core business logic
└── storage/
    └── file_storage.py  # URL tracking and caching
```

### Key Components

- **PaperBotService**: Core service that orchestrates fetching, parsing, and deduplication
- **FileStorage**: Tracks seen URLs in JSON to prevent duplicate posts
- **DiscordBot**: Manages Discord client and scheduled posting loop
- **HTML Parser**: Extracts articles, news links, and daily insights from Morgonsvepet pages
- **RobotsChecker**: Ensures compliance with website robots.txt rules

## Data Models

The bot uses the following main data structures:

- **Morgonsvepet**: The main morning letter containing title, articles, news links, and daily watch
- **Article**: Individual article with title, content, and read more link
- **NewsLink**: News section with title and linked items
- **DailyWatch**: Daily watch section with title and listed items

## Logging

The bot logs all activities to the console with timestamps. Log levels include:
- `DEBUG`: Detailed information for debugging
- `INFO`: General informational messages
- `WARNING`: Warning messages for potential issues
- `ERROR`: Error messages for failures

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available on GitHub.
