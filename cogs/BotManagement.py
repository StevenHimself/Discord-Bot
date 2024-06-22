import discord
from discord import app_commands
from discord.ext import commands


class BotManagement(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Command Management loaded ✔️")

    @commands.command()
    async def shutdown(self, ctx):
        """shuts down the bot"""
        print("Shutting down. Bot offline.")
        await ctx.send("Stubee is going to sleep 💤")
        await ctx.bot.close()

    @commands.command()
    async def sync(self, ctx) -> None:
        """syncs/updates any commands"""
        fmt = await ctx.bot.tree.sync()
        await ctx.send(f"Synced {len(fmt)} commands.")

    @commands.command()
    async def clear(self, ctx) -> None:
        """clears old commands"""
        fmt = await ctx.bot.tree.clear_commands()
        await ctx.send(f"Cleared {len(fmt)} commands.")

    @commands.command()
    async def load(self, ctx, extension):
        """loads commands"""
        await ctx.bot.load_extension(f'cogs.{extension}')
        await ctx.send(f"Loaded {extension} commands!")

    @commands.command()
    async def unload(self, ctx, extension):
        """unloads commands"""
        await ctx.bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f"Unloaded {extension} commands!")


async def setup(bot):
    await bot.add_cog(BotManagement(bot))
