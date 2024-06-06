import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

database = sqlite3.connect('clan.db')
cursor = database.cursor()
database.execute("CREATE TABLE IF NOT EXISTS clan(discord_name STRING, game_name STRING, clan_points INT")


class MemberManagement(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Member Management loaded ✔️")

    @app_commands.command(name="enlist", description="Adds member to clan database - FORMAT:Discord user,RSN")
    @app_commands.checks.cooldown(1, 5, key=lambda i: i.user.id)
    async def enlist(self, interaction: discord.Interaction, *, member: str) -> None:
        """adds member to database"""
        member_info = member.split(",")
        discord_name = member_info[0]
        game_name = member_info[1]
        clan_points = 0
        query = "INSERT INTO clan VALUES(?, ?, ?)"
        cursor.execute(query, (discord_name, game_name, clan_points))
        database.commit()
        await interaction.followup.send("Member added to clan database.")

    @app_commands.command(name="discharge", description="Removes member from clan database (RSN)")
    @app_commands.checks.cooldown(1, 5, key=lambda i: i.user.id)
    async def delete(self, interaction: discord.Interaction, *, member: str) -> None:
        """removes member from database"""
        query = "DELETE FROM clan WHERE game_name = ?"
        cursor.execute(query, (member,))
        database.commit()
        await interaction.followup.send("Member removed from the clan database.")

    @app_commands.command(name="add_points", description="Adds points for member FORMAT:(RSN,points)")
    @app_commands.checks.cooldown(1, 5, key=lambda i: i.user.id)
    async def add_points(self, interaction: discord.Interaction, *, points: str) -> None:
        """adds points to member in database"""
        member_info = points.split(",")
        game_name = member_info[0]
        new_points = int(member_info[1])
        query = "SELECT * FROM clan WHERE game_name = ?"
        cursor.execute(query, (game_name,))
        existing_user = cursor.fetchone()

        if existing_user:
            query = "UPDATE clan SET clan_points = clan_points + ? WHERE game_name = ?"
            cursor.execute(query, (new_points, game_name))
            database.commit()


async def setup(bot):
    await bot.add_cog(MemberManagement(bot))
