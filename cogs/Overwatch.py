import discord
import aiohttp
import json
from discord import app_commands
from discord.ext import commands


class Overwatch(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Overwatch commands loaded ✔️")

    @app_commands.command(name='overwatch', description='Pulls various information from your Overwatch account')
    async def overwatch(self, interaction: discord.Interaction, battletag: str) -> None:
        """Pulls overwatch statistics"""
        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://overfast-api.tekrop.fr/players/{battletag}/stats/summary") as response:
                raw = await response.text()
                summary_map = json.loads(raw)
                general_stats_map = summary_map["general"]
                win_rate = general_stats_map["winrate"]
                kda = general_stats_map["kda"]
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://overfast-api.tekrop.fr/players/{battletag}/summary") as response:
                raw = await response.text()
                player_map = json.loads(raw)
                username = player_map["username"]
                # avatar = player_map["avatar"]
                title = player_map["title"]
                # rank = player_map["competitive"]

        embed = discord.Embed(title=f'{username} - {title}', color=discord.Colour.teal())
        embed.set_author(name="Overwatch 2")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1199901578421882930/1199902275615871026"
                                "/overwatch-logo-white-15.png?ex=65c43b13&is=65b1c613&hm"
                                "=ec1a59333d61afa74fbc1a06851b79e30537f75b03df44849febbc720e9ba1e8&")
        embed.add_field(name='WINRATE', value=f"{win_rate}%")
        embed.add_field(name='KDA', value=kda)
        embed.set_footer(text=f"Request made by {interaction.user}", icon_url=interaction.user.display_avatar)
        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Overwatch(bot))
