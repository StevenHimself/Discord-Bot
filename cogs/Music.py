import discord
import wavelink
from discord import app_commands
from discord.ext import commands
from typing import cast
import logging


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music commands loaded ✔️")
        self.bot.loop.create_task(self.setup_hook())

    async def setup_hook(self) -> None:
        """connects to lavalink host"""
        print("Attempting to connect to Lavalink node...")
        nodes = [wavelink.Node(uri='http://us1.lavalink.creavite.co:20080', password='auto.creavite.co')]
        try:
            await wavelink.Pool.connect(nodes=nodes, client=self.bot, cache_capacity=100)
        except Exception as e:
            logging.error(f"Exception occurred: {e}")

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, payload: wavelink.NodeReadyEventPayload) -> None:
        """Confirms a successful connection to a lavalink node"""
        logging.info(f"Successfully connected Wavelink Node: {payload.node!r} | Resumed: {payload.resumed}")
        print("Successfully connected to Lavalink Node! ✔️")

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload: wavelink.TrackStartEventPayload) -> None:
        player: wavelink.Player | None = payload.player
        if not player:
            return

        original: wavelink.Playable | None = payload.original
        song: wavelink.Playable = payload.track

        embed: discord.Embed = discord.Embed(title="Now Playing 🎵", color=discord.Colour.teal())
        embed.description = f"**{song.title}** by `{song.author}`"
        embed.set_footer(text=f"Request made by {song.source}")

        if song.artwork:
            embed.set_image(url=song.artwork)
        if song.album.name:
            embed.add_field(name="Album", value=song.album.name)
        if song.length:
            embed.add_field(name="Length", value=song.length)

        await player.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState,
                                    after: discord.VoiceState):
        """bot will automatically disconnect if alone in voice channel"""
        voice_state = member.guild.voice_client

        if voice_state is not None and len(voice_state.channel.members) == 1:
            await voice_state.disconnect()

    @app_commands.command(name='play', description='Plays a song from YouTube/SoundCloud (defaults to YouTube without '
                                                   'platform-specific URL).')
    async def play(self, interaction: discord.Interaction, *, song: str) -> None:
        """plays a song"""
        await interaction.response.defer()
        if not interaction.guild:
            return

        player: wavelink.Player
        player = cast(wavelink.Player, interaction.guild.voice_client)  # type: ignore

        if not player:
            try:
                player = await interaction.user.voice.channel.connect(cls=wavelink.Player)  # type: ignore
            except AttributeError:
                embed = discord.Embed(title="I am not connected to a voice channel. 🤨", color=discord.Colour.red())
                await interaction.followup.send(embed=embed)
                return
            except discord.ClientException:
                embed = discord.Embed(title="Could not join voice channel. Please try again! ⛔",
                                      color=discord.Colour.red())
                await interaction.followup.send(embed=embed)
                return

        player.autoplay = wavelink.AutoPlayMode.partial
        songs: wavelink.Search = await wavelink.Playable.search(song)

        if not songs:
            embed = discord.Embed(title="Could not find any songs with that name. Please try again ⛔",
                                  color=discord.Colour.red())
            await interaction.followup.send(embed=embed)
            return
        if isinstance(songs, wavelink.Playlist):
            # if passed argument is a playlist
            added: int = await player.queue.put_wait(songs)
            embed = discord.Embed(title=f"Added ({added} songs) to the queue! ✅", color=discord.Colour.teal())
            await interaction.followup.send(embed=embed)
        else:
            song: wavelink.Playable = songs[0]
            await player.queue.put_wait(song)
            embed = discord.Embed(title=f"Added {song} to the queue! ✅", color=discord.Colour.teal())
            embed.set_footer(text=f"Request made by {interaction.user}", icon_url=interaction.user.display_avatar)
            await interaction.followup.send(embed=embed)

        if not player.playing:
            # if not playing, then play song immediately
            await player.play(player.queue.get(), volume=30)
            embed = discord.Embed(title=f"Now playing ({song}) 🎵", color=discord.Colour.teal())
            embed.set_footer(text=f"Request made by {interaction.user}", icon_url=interaction.user.display_avatar)
            await interaction.followup.send(embed=embed)

    @app_commands.command(name='skip', description='Skips current song.')
    async def skip(self, interaction: discord.Interaction) -> None:
        """skips current song"""
        await interaction.response.defer()
        player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player:
            embed = discord.Embed(title="I am not connected to a voice channel. ⛔", color=discord.Colour.red())
            await interaction.followup.send(embed=embed)
            return

        if player.paused:
            embed = discord.Embed(title="I am not playing anything to skip. ⛔", color=discord.Colour.red())
            await interaction.followup.send(embed=embed)
            return
        if not player.queue:
            embed = discord.Embed(title="Queue is empty, no more tracks to skip to. ⛔", color=discord.Colour.red())
            await interaction.followup.send(embed=embed)
            return
        else:
            await player.skip(force=True)
            embed = discord.Embed(title="Track was skipped! ⏩", color=discord.Colour.teal())
            embed.set_footer(text=f"Skipped by {interaction.user}", icon_url=interaction.user.display_avatar)
            await interaction.followup.send(embed=embed)

    @app_commands.command(name='toggle', description='Resumes/Pauses the current song depending on state.')
    async def pause_resume(self, interaction: discord.Interaction) -> None:
        """pauses or resumes current song depending on state"""
        await interaction.response.defer()
        player = cast(wavelink.Player, interaction.guild.voice_client)

        if not player:
            embed = discord.Embed(title="I am not connected to a voice channel. ⛔", color=discord.Colour.red())
            await interaction.followup.send(embed=embed)
            return

        if player.playing:
            await player.pause(not player.paused)
            embed = discord.Embed(title="Track was paused! ⏸️", color=discord.Colour.teal())
            embed.set_footer(text=f"Resumed by {interaction.user}", icon_url=interaction.user.display_avatar)
            await interaction.followup.send(embed=embed)
        else:
            await player.pause(player.paused)
            embed = discord.Embed(title="Track was resumed! 🎵", color=discord.Colour.teal())
            embed.set_footer(text=f"Resumed by {interaction.user}", icon_url=interaction.user.display_avatar)
            await interaction.followup.send(embed=embed)

    @app_commands.command(name='queue', description='Displays the current queue.')
    async def queue(self, interaction: discord.Interaction) -> None:
        """displays current queue"""
        await interaction.response.defer()
        player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player:
            embed = discord.Embed(title="I am not connected to a voice channel. ⛔", color=discord.Colour.red())
            await interaction.followup.send(embed=embed)
            return

        if not player.queue:
            embed = discord.Embed(title="Queue is empty ⛔", color=discord.Colour.red())
            await interaction.followup.send(embed=embed)
            return
        else:
            embed = discord.Embed(title="Current queue", color=discord.Colour.teal(), description=f'{player.queue}')
            await interaction.followup.send(embed=embed)

    @app_commands.command(name='connect', description='Connects bot to your current voice channel.')
    async def connect(self, interaction: discord.Interaction) -> None:
        """connects bot to voice channel"""
        await interaction.response.defer()
        player: wavelink.Player
        player = cast(wavelink.Player, interaction.guild.voice_client)  # type: ignore

        if not player:
            try:
                player = await interaction.user.voice.channel.connect(cls=wavelink.Player())
                embed = discord.Embed(
                    title=f"Connected to {interaction.user.voice.channel} <a:pikawave:956858765330767893>",
                    color=discord.Colour.teal())
                await interaction.followup.send(embed=embed)
            except AttributeError:
                embed = discord.Embed(title="Please join a voice channel so I can connect. 🤨",
                                      color=discord.Colour.red())
                await interaction.followup.send(embed=embed)
            except discord.ClientException:
                embed = discord.Embed(title="Could not join the voice channel. Please try again! ⛔",
                                      color=discord.Colour.red())
                await interaction.followup.send(embed=embed)
                return

    @app_commands.command(name='disconnect', description='Disconnects bot from voice channel.')
    async def disconnect(self, interaction: discord.Interaction) -> None:
        """disconnects bot from voice channel"""
        await interaction.response.defer()
        player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player:
            embed = discord.Embed(title="I am not connected to a voice channel. ⛔", color=discord.Colour.red())
            await interaction.followup.send(embed=embed)
            return

        await player.disconnect()
        embed = discord.Embed(
            title=f"Disconnected from {interaction.user.voice.channel}. <a:pikawave:956858765330767893>",
            color=discord.Colour.teal())

        await interaction.followup.send(embed=embed)

    # @commands.Cog.listener()
    # async def on_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    #     if isinstance(error, commands.CommandOnCooldown):
    #         await interaction.response.send_message(f"Slow down there {interaction.user.mention}!"
    #                                                 f"\n wait for {error.retry_after} seconds!", ephemeral=True)
    #     else:
    #         raise error


async def setup(bot):
    await bot.add_cog(Music(bot))
