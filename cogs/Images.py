import discord
import aiohttp
import json
from discord import app_commands
from discord.ext import commands


class Images(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Images cog loaded ✔️")

    # Generates random cat images/gifs from API
    @app_commands.command(name="cat", description="Generates a random cat image/gif")
    @app_commands.checks.cooldown(1, 5, key=lambda i: i.user.id)
    async def cat_pic(self, interaction: discord.Interaction):
        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.thecatapi.com/v1/images/search') as response:
                raw = await response.text()
                cat = json.loads(raw)[0]
                embed = discord.Embed(title="meow! 😺", color=discord.Colour.purple())
                embed.set_image(url=cat['url'])
                await interaction.followup.send(embed=embed)

    # Generates random dog images/gifs from API
    @app_commands.command(name="dog", description="Generates a random dog image/gif")
    @app_commands.checks.cooldown(1, 5, key=lambda i: i.user.id)
    async def dog_pic(self, interaction: discord.Interaction):
        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get('https://dog.ceo/api/breeds/image/random') as response:
                raw = await response.text()
                dog = json.loads(raw)
                embed = discord.Embed(title="woof! 🐶", color=discord.Colour.green())
                embed.set_image(url=dog['message'])
                await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Images(bot))
