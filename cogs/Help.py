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
        embed = discord.Embed(title="Stubee Commands", color=discord.Colour.teal())
        embed.set_author(url=interaction.user.avatar)
        embed.set_field_at(name="MUSIC", value="```play```, ```skip```, ```toggle```, ```queue```", inline=False)
        embed.set_field_at(name="IMAGES/GIFS", value="```cat```, ```dog```", inline=False)
        embed.set_field_at(name="TEXT", value="```quote```",inline=False)
        embed.set_field_at(name="GAMES", value="```overwatch```",inline=False)
        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
