import discord
import wavelink
from discord import app_commands
from discord.ext import commands
from typing import cast


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music commands loaded ✔️")

    @app_commands.command(name='play', description='Plays a song')
    async def play(self, interaction: discord.Interaction, *, song: str) -> None:
        """plays a song"""
        await interaction.response.defer()
        if not interaction.guild:
            return

        player: wavelink.Player
        player = cast(wavelink.Player, interaction.guild.voice_client)  # type: ignore

        if not player:
            try:
                player = await interaction.user.voice.channel(cls=wavelink.Player)  # type: ignore
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
            embed = discord.Embed(title=f"Added ({added} songs) to the queue ✅",
                                  color=discord.Colour.teal())
        else:
            song: wavelink.Playable = songs[0]
            await player.queue.put_wait(song)
            embed = discord.Embed(title=f"Added {song} to the queue!")

        if not player.playing:
            # if not playing, then play song immediately
            await player.play(player.queue.get(), volume=30)

    @app_commands.command(name='skip', description='Skips current song.')
    async def skip(self, interaction: discord.Interaction) -> None:
        """skips current song"""
        await interaction.response.defer()
        player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player:
            embed = discord.Embed(title="I am not connected to a voice channel. ⛔", color=discord.Colour.red())
            await interaction.followup.send(embed=embed)
            return

        if not player.is_playing():
            embed = discord.Embed(title="I am not playing anything to skip. ⛔", color=discord.Colour.red())
            interaction.followup.send(embed=embed)
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

        if player.queue.is_empty:
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
