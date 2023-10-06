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

    @bot.event
    async def on_wavelink_track_start(interaction: discord.Interaction, player: wavelink.Player,
                                      track: wavelink.YouTubeTrack or wavelink.SoundCloudTrack):
        await interaction.response.defer()
        embed = discord.Embed(title="Current track", color=discord.Colour.blurple(),
                              description=f"Currently playing {player.current}")
        await interaction.followup.send(embed=embed)

    # @bot.event
    # async def on_wavelink_track_end(interaction: discord.Interaction, player: wavelink.Player,
    #                                 track: wavelink.YouTubeTrack or wavelink.SoundCloudTrack)
    #     await interaction.response.defer()
    #     if player.queue.is_empty:
    #         embed = discord.Embed(title="Queue is empty!", color=discord.Colour.blurple(),
    #                               description="Queue another song to continue playing!")
    #         await interaction.followup.send(embed=embed)
    #
    #     elif not player.queue.is_empty:


    # bot will disconnect from voice channel if alone
    @bot.event
    async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        voice_state = member.guild.voice_client

        if voice_state is not None and len(voice_state.channel.members) == 1:
            await voice_state.disconnect()

    # connects to lavalink host
    async def connect_nodes():
        await bot.wait_until_ready()
        node: wavelink.Node = wavelink.Node(uri='lava.horizxon.tech:80', password='horizxon.tech')
        await wavelink.NodePool.connect(client=bot, nodes=[node])

    await bot.start(token)


asyncio.run((main()))
