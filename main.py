# Author: Steven Montecinos
import discord
import subprocess
import asyncio
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# initiating bot
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), application_id=1116698756046389300)


async def get_current_branch():
    """gets current working branch"""
    try:
        return subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], universal_newlines=True)
    except subprocess.CalledProcessError:
        return None


async def shutdown_after_delay():
    """shuts down bot after delay"""
    await asyncio.sleep(60)
    await bot.close()


async def load():
    """loads cogs"""
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')


async def main():
    await load()

    @bot.event
    async def on_ready():
        """starts up bot"""
        print("Stubee Bot online, Beep Boop. 🤖")

        current_branch = await get_current_branch()

        if current_branch != "master":
            print("This is a non-master branch, bot will shut down in 1 minute.")
            bot.loop.create_task(shutdown_after_delay())
        else:
            print("You are on a master branch, bot will continue running until user intervention.")

    await bot.start(token)


asyncio.run((main()))
