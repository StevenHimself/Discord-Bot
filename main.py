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

    # bot goes online
    @bot.event
    async def on_ready():
        print("Bot online, Beep Boop.")
        bot.loop.create_task(connect_nodes())  # continuous attempt to connect to a node

    @bot.event
    async def on_wavelink_node_ready(node: wavelink.Node) -> None:
        print(f"Node <{node.id}> is ready")
        wavelink.Player.autoplay = True

    # @bot.event
    # async def on_wavelink_track_start(interaction: discord.Interaction, player: wavelink.Player,
    #                                   track: wavelink.YouTubeTrack or wavelink.SoundCloudTrack):
    #     await interaction.response.defer()
    #     embed = discord.Embed(title="Current track", color=discord.Colour.blurple(),
    #                           description=f"Currently playing {player.current}")
    #     await interaction.followup.send(embed=embed)

    # bot will disconnect from voice channel if alone
    @bot.event
    async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        voice_state = member.guild.voice_client

        if voice_state is not None and len(voice_state.channel.members) == 1:
            await voice_state.disconnect()

    # connects to lavalink host
    # async def setup_hook(self) -> None:
    #     await bot.wait_until_ready()
    #     nodes = [wavelink.Node(uri='http://n1.ll.darrennathanael.com:2269', password='glasshost1984')]
    #     await wavelink.Pool.connect(nodes=nodes, client=bot, cache_capacity=None)

    async def connect_nodes():
        await bot.wait_until_ready()
        node: wavelink.Node = wavelink.Node(uri='lavalink.oryzen.xyz:80', password='oryzen.xyz')
        await wavelink.NodePool.connect(client=bot, nodes=[node])

    await bot.start(token)

asyncio.run((main()))
