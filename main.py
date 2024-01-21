# Author: Steven Montecinos
import discord
import asyncio
import logging
import os
import wavelink
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# initiating bot
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), application_id=1116698756046389300)


# load/unload cog functions
async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')


async def main():
    await load()

    # bot goes online
    @bot.event
    async def on_ready():
        print("Stubee Bot online, Beep Boop.")
        # bot.loop.create_task(setup_hook())  # continuous attempt to connect to a node

    async def on_wavelink_node_ready(self, payload: wavelink.NodeReadyEventPayload) -> None:
        print(f'{payload.node}')
        logging.info(f"Successfully connected Wavelink Node: {payload.node!r} | Resumed: {payload.resumed}")

    async def setup_hook(self) -> None:
        """connects to lavalink host"""
        await bot.wait_until_ready()
        nodes = [wavelink.Node(uri='http://nyc1.guardiancloud.xyz:10002', password='GuardianCloudServices')]
        await wavelink.Pool.connect(nodes=nodes, client=self.bot, cache_capacity=100)

    # @bot.=event
    # async def on_wavelink_track_start(interaction: discord.Interaction, player: wavelink.Player,
    #                                   track: wavelink.YouTubeTrack or wavelink.SoundCloudTrack):
    #     await interaction.response.defer()
    #     embed = discord.Embed(title="Current track", color=discord.Colour.blurple(),
    #                           description=f"Currently playing {player.current}")
    #     await interaction.followup.send(embed=embed)

    @bot.event
    async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """bot will automatically disconnect if alone in voice channel"""
        voice_state = member.guild.voice_client

        if voice_state is not None and len(voice_state.channel.members) == 1:
            await voice_state.disconnect()

    await bot.start(token)


asyncio.run((main()))
