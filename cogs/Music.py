import discord
import wavelink
from discord.ext import commands


class MusicCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music commands loaded ✔️")

    # command that plays from YouTube
    @commands.command()
    async def yplay(self, ctx: commands.Context, *, track: str):
        vc = ctx.voice_client  # represents a discord connection
        tracks = await wavelink.YouTubeTrack.search(track)

        if not vc:
            # custom_player = CustomPlayer()
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player, self_deaf=True)

        if not vc.is_playing() and vc.queue.is_empty:
            await vc.play(tracks[0])

            embed = discord.Embed(title=tracks[0].title, color=discord.Colour.red(), url=tracks[0].uri,
                                  description="Playing from YouTube! ▶️")
            embed.set_footer(text=f"Request made by {ctx.author}", icon_url=ctx.author.display_avatar)

            await ctx.send(embed=embed)

        else:
            vc.queue.put(item=tracks[0])

            embed = discord.Embed(title=tracks[0].title, color=discord.Colour.red(), url=tracks[0].uri,
                                  description="Queued from YouTube ▶️")
            embed.set_footer(text=f"Request made by {ctx.author}", icon_url=ctx.author.display_avatar)

            await ctx.send(embed=embed)

    # command that plays from SoundCloud
    @commands.command()
    async def splay(self, ctx: commands.Context, *, track: str):
        vc = ctx.voice_client
        tracks = await wavelink.SoundCloudTrack.search(track)

        if not vc:
            # custom_player = CustomPlayer()
            vc: wavelink.player = await ctx.author.voice.channel.connect(cls=wavelink.Player)

        if not vc.is_playing() and vc.queue.is_empty:
            await vc.play(tracks[0])

            embed = discord.Embed(title=tracks[0].title, color=discord.Colour.orange(), url=tracks[0].uri,
                                      description="Playing from SoundCloud! ☁️")
            embed.set_footer(text=f"Request made by {ctx.author}", icon_url=ctx.author.display_avatar)

            await ctx.send(embed=embed)

        else:
            vc.queue.put(item=tracks[0])

            embed = discord.Embed(title=tracks[0].title, color=discord.Colour.orange(), url=tracks[0].uri,
                                      description="Queued from SoundCloud! ☁️")
            embed.set_footer(text=f"Request made by {ctx.author}", icon_url=ctx.author.display_avatar)

            await ctx.send(embed=embed)

    # skip command
    @commands.command()
    async def skip(self, ctx: commands.Context):
        vc = ctx.voice_client
        if vc:
            if not vc.is_playing():
                return await ctx.send("I am not playing anything to skip.")
            else:
                embed = discord.Embed(title="Track was skipped! ⏩", color=discord.Colour.blurple())
                embed.set_footer(text=f"Skipped by {ctx.author}", icon_url=ctx.author.display_avatar)
                await ctx.send(embed=embed)
                await vc.stop()
        else:
            await ctx.send("I am not connected to a voice channel.")

    # pause command
    @commands.command()
    async def pause(self, ctx: commands.Context):
        vc = ctx.voice_client
        if vc:
            if vc.is_paused():
                return await ctx.send("I am already paused.")
            else:
                embed = discord.Embed(title="Track was paused! ⏸️", color=discord.Colour.blurple())
                embed.set_footer(text=f"Paused by {ctx.author}", icon_url=ctx.author.display_avatar)
                await ctx.send(embed=embed)
                await vc.pause()

        else:
            await ctx.send("I am not connected to a voice channel.")

        # resume command
    @commands.command()
    async def resume(self, ctx: commands.Context):
        vc = ctx.voice_client
        if vc:
            if not vc.is_paused():
                return await ctx.send("I'm already playing music.")
            else:
                embed = discord.Embed(title="Track was resumed! 🎵", color=discord.Colour.blurple())
                embed.set_footer(text=f"Resumed by {ctx.author}", icon_url=ctx.author.display_avatar)
                await ctx.send(embed=embed)
                await vc.resume()

        else:
            await ctx.send("I am not connected to a voice channel.")

    # displays current queue
    @commands.command()
    async def queue(self, ctx: commands.Context):
        vc = ctx.voice_client
        if vc:
            embed = discord.Embed(title="Current Queue", color=discord.Colour.blurple(), description=f'{vc.queue}')
            await ctx.send(embed=embed)

        else:
            await ctx.send("I am not connected to a voice channel.")

    # connect to channel command
    @commands.command()
    async def connect(self, ctx: commands.Context, *, channel: discord.VoiceChannel | None = None):
        vc = ctx.voice_client
        try:
            channel = channel or ctx.author.voice.channel
        except AttributeError:
            return await ctx.send("No voice channel to connect to. Please either provide one or join one.")

        if not vc:
            await channel.connect(cls=wavelink.Player())
            embed = discord.Embed(title=f"Connected to {ctx.author.voice.channel} ✅", color=discord.Colour.green())
            await ctx.send(embed=embed)
        elif vc:
            await ctx.send("I am already connected to a channel.")

    # disconnect from channel command
    @commands.command()
    async def disconnect(self, ctx: commands.Context, *, channel: discord.VoiceChannel | None = None):
        vc = ctx.voice_client
        if vc:
            await vc.disconnect()
            embed = discord.Embed(title=f"Disconnected from {ctx.author.voice.channel} 👋",
                                  color=discord.Colour.dark_red())
            await ctx.send(embed=embed)
        elif not vc:
            await ctx.send("I am not connected to voice channel!")


async def setup(bot):
    await bot.add_cog(MusicCommands(bot))
