import discord
from discord import app_commands
from discord.ext import commands


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Help command loaded ✔️")

    @app_commands.command(name="help", description="Displays all commands")
    async def help(self, interaction: discord.Interaction):
        """help command"""
        await interaction.response.defer()
        embed = discord.Embed(title="Commands", color=discord.Colour.teal())
        embed.set_thumbnail(url="https://imgur.com/FSaIt1c")
        embed.set_author(name="stubee bot", url="https://github.com/StevenHimself/Discord-Bot")
        embed.add_field(name="__Music__", value="play, skip, toggle, volume, queue", inline=False)
        embed.add_field(name="__Images/Gifs__", value="dog, cat, imagine", inline=False)
        embed.add_field(name="__Text__", value="quote", inline=False)
        embed.add_field(name="__Games__", value="overwatch", inline=False)
        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
