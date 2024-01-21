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
    async def load(self, ctx, extension):
        """loads commands"""
        ctx.bot.load_extension(f'cogs.{extension}')

    @commands.command()
    async def unload(self, ctx, extension):
        """unloads commands"""
        ctx.bot.unload_extension(f'cogs.{extension}')


async def setup(bot):
    await bot.add_cog(BotManagement(bot))
