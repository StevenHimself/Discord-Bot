# Author: Steven Montecinos
import discord
import asyncio
import json
import os
import wavelink
from discord.ext import commands

# creating json.config and securing token
if not os.path.exists(os.getcwd() + "/config.json"):
    configTemplate = {"TOKEN": "", "PREFIX": "!"}
    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)
else:
    with open("./config.json") as f:
        configData = json.load(f)

# assigning external variables from config.json
token = configData["TOKEN"]
prefix = configData["PREFIX"]

# initiating bot
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), application_id=1116698756046389300)


# load/unload cog functions
async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')


async def unload():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.unload_extension(f'cogs.{filename[:-3]}')


async def main():
    await load()

    # Player class
    class CustomPlayer(wavelink.Player):
        def __init__(self):
            super().__init__()
            self.queue = wavelink.Queue()

    # bot goes online
    @bot.event
    async def on_ready():
        print("Bot online, Beep Boop.")
        bot.loop.create_task(connect_nodes())  # continuous attempt to connect to a node

    @bot.event
    async def on_wavelink_node_ready(node: wavelink.Node) -> None:
        print(f"Node <{node.id}> is ready")
        wavelink.Player.autoplay = True

    # connects to lavalink host
    async def connect_nodes():
        await bot.wait_until_ready()
        node: wavelink.Node = wavelink.Node(uri='us.lavalink.alexanderof.xyz:2333', password='lavalink')
        await wavelink.NodePool.connect(client=bot, nodes=[node])

    # MUSIC BASED COMMANDS

    # command that plays from YouTube
    @bot.command()
    async def ytplay(ctx: commands.Context, *, search: wavelink.YouTubeTrack):
        vc = ctx.voice_client  # represents a discord connection

        if not vc:
            custom_player = CustomPlayer()
            vc: CustomPlayer = await ctx.author.voice.channel.connect(cls=custom_player, self_deaf=True)

        if not vc.is_playing() and vc.queue.is_empty:
            await vc.play(search)

            embed = discord.Embed(title=search.title, color=discord.Colour.red(), url=search.uri,
                                  description="Playing from YouTube! ▶️")
            embed.set_footer(text=f"Request made by {ctx.author}", icon_url=ctx.author.display_avatar)

            await ctx.send(embed=embed)

        else:
            vc.queue.put(item=search)

            embed = discord.Embed(title=search.title, color=discord.Colour.red(), url=search.uri,
                                  description="Queued from YouTube ▶️")
            embed.set_footer(text=f"Request made by {ctx.author}", icon_url=ctx.author.display_avatar)

            await ctx.send(embed=embed)

    # command that plays from SoundCloud
    @bot.command()
    async def scplay(ctx: commands.Context, *, search: wavelink.SoundCloudTrack):
        vc = ctx.voice_client

        if not vc:
            custom_player = CustomPlayer()
            vc: CustomPlayer = await ctx.author.voice.channel.connect(cls=custom_player)

        if not vc.is_playing() and vc.queue.is_empty:
            await vc.play(search)

            embed = discord.Embed(title=search.title, color=discord.Colour.orange(), url=search.uri,
                                  description="Playing from SoundCloud! ☁️")
            embed.set_footer(text=f"Request made by {ctx.author}", icon_url=ctx.author.display_avatar)

            await ctx.send(embed=embed)

        else:
            vc.queue.put(item=search)

            embed = discord.Embed(title=search.title, color=discord.Colour.orange(), url=search.uri,
                                  description="Queued from SoundCloud! ☁️")
            embed.set_footer(text=f"Request made by {ctx.author}", icon_url=ctx.author.display_avatar)

            await ctx.send(embed=embed)

    # skip command
    @bot.command()
    async def skip(ctx: commands.Context):
        vc = ctx.voice_client
        if vc:
            if not vc.is_playing():
                return await ctx.send("I am not playing anything to skip.")
            else:
                return await vc.stop()
        else:
            await ctx.send("I am not connected to a voice channel.")

    # pause command
    @bot.command()
    async def pause(ctx: commands.Context):
        vc = ctx.voice_client
        if vc:
            if vc.is_paused():
                return await ctx.send("I am already paused.")
            else:
                return await vc.pause()

        else:
            await ctx.send("I am not connected to a voice channel.")

    # resume command
    @bot.command()
    async def resume(ctx: commands.Context):
        vc = ctx.voice_client
        if vc:
            if not vc.is_paused():
                return await ctx.send("I'm already playing music.")
            else:
                return await vc.resume()

        else:
            await ctx.send("I am not connected to a voice channel.")

    # displays current queue
    @bot.command()
    async def queue(ctx: commands.Context):
        vc = ctx.voice_client
        if vc:
            await ctx.send(f"{vc.queue}")

        else:
            await ctx.send("I am not connected to a voice channel.")

    # connect to channel command
    @bot.command()
    async def connect(ctx: commands.Context, *, channel: discord.VoiceChannel | None = None):
        vc = ctx.voice_client
        try:
            channel = channel or ctx.author.voice.channel
        except AttributeError:
            return await ctx.send("No voice channel to connect to. Please either provide one or join one.")

        if not vc:
            await channel.connect(cls=CustomPlayer())
        elif vc:
            await ctx.send("I am already connected to a channel.")

    # disconnect from channel command
    @bot.command()
    async def disconnect(ctx: commands.Context, *, channel: discord.VoiceChannel | None = None):
        vc = ctx.voice_client
        if vc:
            await vc.disconnect()
        elif not vc:
            await ctx.send("I am not connected to voice channel!")

    await bot.start(token)


asyncio.run(main())
