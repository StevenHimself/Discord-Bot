# Author: Steven Montecinos
import discord
import asyncio
import logging
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# initiating bot
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), application_id=1116698756046389300)
discord.utils.setup_logging(level=logging.INFO)


async def shutdown_after_delay():
    """shuts down bot after delay"""
    await asyncio.sleep(7)
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
        # bot.loop.create_task(shutdown_after_delay()) # for workflow testing only.

    await bot.start(token)


asyncio.run((main()))
