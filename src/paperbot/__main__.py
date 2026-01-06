import logging
from .bot.discordbot import run_discordbot



def main():
	logging.basicConfig(
		level=logging.INFO,
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
	)
	logging.getLogger("discord").setLevel(logging.INFO)

	logging.info("Paperbot is starting...")
	run_discordbot()


if __name__ == "__main__":
	main()

