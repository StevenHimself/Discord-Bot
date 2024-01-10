import asyncio

import discord
import wavelink
from discord import app_commands
from discord.ext import commands


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music commands loaded ✔️")

    # command that plays from YouTube
    @app_commands.command(name='yplay', description='Plays a song from YouTube!')
    async def yplay(self, interaction: discord.Interaction, *, track: str):
        await interaction.response.defer()
        vc = interaction.guild.voice_client  # represents a discord connection
        tracks = await wavelink.YouTubeTrack.search(track)
        if not vc:
            # custom_player = CustomPlayer()
            vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player, self_deaf=True)

        if not vc.is_playing() and vc.queue.is_empty:
            await vc.play(tracks[0])

            embed = discord.Embed(title=tracks[0].title, color=discord.Colour.red(), url=tracks[0].uri,
                                  description="Playing from YouTube!  <:youtube:1133117120109101106>")
            embed.set_footer(text=f"Request made by {interaction.user}", icon_url=interaction.user.display_avatar)
            await interaction.followup.send(embed=embed)

        else:
            vc.queue.put(item=tracks[0])

            embed = discord.Embed(title=tracks[0].title, color=discord.Colour.red(), url=tracks[0].uri,
                                  description="Queued from YouTube  <:youtube:1133117120109101106>")
            embed.set_footer(text=f"Request made by {interaction.user}", icon_url=interaction.user.display_avatar)

            await interaction.followup.send(embed=embed)

    # command that plays from SoundCloud
    @app_commands.command(name='splay', description='Plays a song from SoundCloud!')
    async def splay(self, interaction: discord.Interaction, *, track: str):
        await interaction.response.defer()
        vc = interaction.guild.voice_client
        tracks = await wavelink.SoundCloudTrack.search(track)

        if not vc:
            # custom_player = CustomPlayer()
            vc: wavelink.player = await interaction.user.voice.channel.connect(cls=wavelink.Player, self_deaf=True)

        if not vc.is_playing() and vc.queue.is_empty:
            await vc.play(tracks[0])

            embed = discord.Embed(title=tracks[0].title, color=discord.Colour.orange(), url=tracks[0].uri,
                                  description="Playing from SoundCloud!  <:soundcloud:1174137028473008209>")
            embed.set_footer(text=f"Request made by {interaction.user}", icon_url=interaction.user.display_avatar)

            await interaction.followup.send(embed=embed)

        else:
            vc.queue.put(item=tracks[0])

            embed = discord.Embed(title=tracks[0].title, color=discord.Colour.orange(), url=tracks[0].uri,
                                  description="Queued from SoundCloud!  <:soundcloud:1174137028473008209>")
            embed.set_footer(text=f"Request made by {interaction.user}", icon_url=interaction.user.display_avatar)
            await interaction.followup.send(embed=embed)

    # skip command
    @app_commands.command(name='skip', description='Skips current track.')
    async def skip(self, interaction: discord.Interaction):
        await interaction.response.defer()
        vc = interaction.guild.voice_client
        if vc:
            if not vc.is_playing():
                embed = discord.Embed(title="I am not playing anything to skip. 🤨", color=discord.Colour.blurple())
                interaction.followup.send(embed=embed)
            else:
                await vc.stop()

                embed = discord.Embed(title="Track was skipped! ⏩", color=discord.Colour.blurple())
                embed.set_footer(text=f"Skipped by {interaction.user}", icon_url=interaction.user.display_avatar)
                await interaction.followup.send(embed=embed)
        else:
            embed = discord.Embed(title="I am not connected to a voice channel. 😔", color=discord.Colour.blurple())
            await interaction.followup.send(embed=embed)

    # pause command
    @app_commands.command(name='pause', description='Pauses the current track.')
    async def pause(self, interaction: discord.Interaction):
        await interaction.response.defer()
        vc = interaction.guild.voice_client
        if vc:
            if vc.is_paused():
                embed = discord.Embed(title="I am already paused. 🤨", color=discord.Colour.blurple())
                interaction.followup.send(embed=embed)
            else:
                await vc.pause()

                embed = discord.Embed(title="Track was paused! ⏸️", color=discord.Colour.blurple())
                embed.set_footer(text=f"Paused by {interaction.user}", icon_url=interaction.user.display_avatar)
                await interaction.followup.send(embed=embed)
        else:
            embed = discord.Embed(title="I am not connected to a voice channel. 😔", color=discord.Colour.blurple())
            await interaction.followup.send(embed=embed)

    # resume command
    @app_commands.command(name='resume', description='Resume the current track.')
    async def resume(self, interaction: discord.Interaction):
        await interaction.response.defer()
        vc = interaction.guild.voice_client
        if vc:
            if not vc.is_paused():
                embed = discord.Embed(title="I am already playing music. 🤨", color=discord.Colour.blurple())
                interaction.followup.send(embed=embed)
            else:
                await vc.resume()

                embed = discord.Embed(title="Track was resumed! 🎵", color=discord.Colour.blurple())
                embed.set_footer(text=f"Resumed by {interaction.user}", icon_url=interaction.user.display_avatar)
                await interaction.followup.send(embed=embed)
        else:
            embed = discord.Embed(title="I am not connected to a voice channel. 😔", color=discord.Colour.blurple())
            await interaction.followup.send(embed=embed)

    # displays current queue
    @app_commands.command(name='queue', description='Displays the current queue.')
    async def queue(self, interaction: discord.Interaction):
        await interaction.response.defer()
        vc = interaction.guild.voice_client
        if vc:
            if not vc.queue.is_empty:
                embed = discord.Embed(title="Current queue", color=discord.Colour.blurple(), description=f'{vc.queue}')
                await interaction.followup.send(embed=embed)

            elif vc.queue.is_empty:
                embed = discord.Embed(title="Queue is empty... 😔", color=discord.Colour.blurple())
                await interaction.followup.send(embed=embed)

        elif not vc:
            embed = discord.Embed(title="I am not connected to a voice channel. 😔", color=discord.Colour.blurple())
            await interaction.followup.send(embed=embed)

    # # clears th queue
    # @app_commands.command(name='clear', description='Clears the queue')
    # async def clear(self, interaction: discord.Interaction):
    #     await interaction.response.defer()
    #     vc = interaction.guild.voice_client
    #     if vc:
    #         if not vc.queue.is_empty:
    #             await vc.stop()
    #             vc.queue.clear()
    #             embed = discord.Embed(title="Queue cleared! ✅", color=discord.Colour.blurple())
    #             await interaction.followup.send(embed=embed)
    #
    #         elif vc.queue.is_empty:
    #             embed = discord.Embed(title="Queue is empty... 😔", color=discord.Colour.blurple())
    #             await interaction.followup.send(embed=embed)
    #
    #     elif not vc:
    #         embed = discord.Embed(title="I am not connected to a voice channel. 😔", color=discord.Colour.blurple())
    #         await interaction.followup.send(embed=embed)

    # connect to channel command
    @app_commands.command(name='connect', description='Connects bot to your current voice channel..')
    async def connect(self, interaction: discord.Interaction, *, channel: discord.VoiceChannel | None = None):
        await interaction.response.defer()
        vc = interaction.guild.voice_client
        try:
            channel = channel or interaction.user.voice.channel
        except AttributeError:
            interaction.followup.send("No voice channel to connect to. Please either provide one or join one.")

        if not vc:
            await channel.connect(cls=wavelink.Player())
            embed = discord.Embed(
                title=f"Connected to {interaction.user.voice.channel} <a:pikawave:956858765330767893>",
                color=discord.Colour.green())
            await interaction.followup.send(embed=embed)
        elif vc:
            embed = discord.Embed(title="I am already connected to a voice channel. 🤨", color=discord.Colour.blurple())
            await interaction.followup.send(embed=embed)

    # disconnect from channel command
    @app_commands.command(name='disconnect', description='Disconnects bot from voice channel.')
    async def disconnect(self, interaction: discord.Interaction):
        await interaction.response.defer()
        vc = interaction.guild.voice_client
        if vc:
            await vc.disconnect()
            embed = discord.Embed(
                title=f"Disconnected from {interaction.user.voice.channel}. <a:pikawave:956858765330767893>",
                color=discord.Colour.dark_red())
            await interaction.followup.send(embed=embed)
        elif not vc:
            embed = discord.Embed(title="I am not connected to a voice channel. 🤨", color=discord.Colour.blurple())
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
