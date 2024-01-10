import random

import discord
import aiohttp
import json
from discord import app_commands
from discord.ext import commands


class Text(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Text commands loaded ✔️")

    # TODO
    # lists all bot commands
    # async def help(self, interaction: discord.Interaction):

    @app_commands.command(name="quote", description="Generates a random quote from different categories")
    @app_commands.checks.cooldown(1, 5, key=lambda i: i.user.id)
    @app_commands.choices(categories=[app_commands.Choice(name="anger", value="anger"),
                                      app_commands.Choice(name="art", value="art"),
                                      app_commands.Choice(name="change", value="change"),
                                      app_commands.Choice(name="courage", value="courage"),
                                      app_commands.Choice(name="experience", value="experience"),
                                      app_commands.Choice(name="failure", value="failure"),
                                      app_commands.Choice(name="family", value="family"),
                                      app_commands.Choice(name="fear", value="fear"),
                                      app_commands.Choice(name="food", value="food"),
                                      app_commands.Choice(name="forgiveness", value="forgiveness"),
                                      app_commands.Choice(name="friendship", value="friendship"),
                                      app_commands.Choice(name="funny", value="funny"),
                                      app_commands.Choice(name="god", value="god"),
                                      app_commands.Choice(name="graduation", value="graduation"),
                                      app_commands.Choice(name="happiness", value="happiness"),
                                      app_commands.Choice(name="health", value="health"),
                                      app_commands.Choice(name="hope", value="hope"),
                                      app_commands.Choice(name="humor", value="humor"),
                                      app_commands.Choice(name="inspirational", value="inspirational"),
                                      app_commands.Choice(name="intelligence", value="intelligence"),
                                      app_commands.Choice(name="knowledge", value="knowledge"),
                                      app_commands.Choice(name="life", value="life"),
                                      app_commands.Choice(name="love", value="love"),
                                      app_commands.Choice(name="success", value="success"),
                                      ])
    async def quote(self, interaction: discord.Interaction, categories: app_commands.Choice[str]):
        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.api-ninjas.com/v1/quotes?category={categories.value}',
                                   headers={'X-Api-Key': '26hgo+xM8kjRhaavCUsEgQ==dsGnrqp1zdGqwDYS'}) as response:
                raw = await response.text()
                quote_map = json.loads(raw)[0]
                quote = quote_map["quote"]
                author = quote_map["author"]
                category = quote_map["category"]
                match category:
                    case "inspirational":
                        category += " ✊"
                    case "intelligence":
                        category += " 🤓"
                    case "failure":
                        category += " 😔"
                    case "knowledge":
                        category += " 📚"
                    case "anger":
                        category += " 😠"
                    case "health":
                        category += " 🏥"
                    case "humor":
                        category += " 😂"
                    case "funny":
                        category += " 🤣"
                    case "art":
                        category += " 🎨"
                    case "love":
                        category += " 💗"
                    case "family":
                        category += " 👪"
                    case "fear":
                        category += " 😱"
                    case "graduation":
                        category += " 🎓"
                    case "hope":
                        category += " 🥺"
                    case "success":
                        category += " ✔️"
                    case "change":
                        category += " ⁉️"
                    case "friendship":
                        category += " 🤝"
                    case "forgiveness":
                        category += " 🙇"
                    case "food":
                        category += " 🍴"
                    case "life":
                        category += " 🌱"
                    case "courage":
                        category += " 🤺"
                    case "experience":
                        category += " 👴"
                embed = discord.Embed(title=f'{category.upper()}',
                                      color=discord.Colour.random(),
                                      description=f'*"{quote}"*')
                embed.set_footer(text=f'{author} 💬')
                await interaction.followup.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, commands.CommandOnCooldown):
            await interaction.response.send_message(f"Slow down there {interaction.user.mention}!"
                                                    f"\n wait for {error.retry_after} seconds!", ephemeral=True)
        else:
            raise error


async def setup(bot):
    await bot.add_cog(Text(bot))
