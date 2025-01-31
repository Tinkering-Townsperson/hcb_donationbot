#################
# SETUP/IMPORTS #
#################

import asyncio  # noqa
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from hcb_donationbot import DEFAULT_HOURS, DEFAULT_ORG, __version__, check_donations


###############
# ENVIRONMENT #
###############
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

###########
# DISCORD #
###########
intents = discord.Intents.default()
intents.typing = False

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
	print(f'{bot.user} has connected to Discord!')

	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for donations"))


@bot.command(name="donations")
async def manually_check_donations(ctx, hcb_id: str = DEFAULT_ORG, hours: int = DEFAULT_HOURS, *args, **kwargs):
	await check_donations(ctx, org_id=hcb_id, hours=hours)


if __name__ == "__main__":
	print(f"hcb-donationbot v{__version__}")
	bot.run(BOT_TOKEN)
