from discord import ApplicationContext, AutocompleteContext, FFmpegPCMAudio, Option
from discord.ext import commands
from discord.utils import get
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL

from zorak.utilities.cog_helpers._validators import is_youtube_link


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

    async def youtube_video_autocompletion(self, ctx: AutocompleteContext):
        current = ctx.options["video"]
        data = []

        # Check if the current input is a link
        is_link = is_youtube_link(current)
        if is_link:
            return [current]  # Return the link as the only option

        # Otherwise, search YouTube for videos with the current string
        videos_search = VideosSearch(current, limit=5)
        results = videos_search.result()

        for video in results["result"]:
            video_title = video["title"]
            data.append(video_title)

        return data

    @commands.slash_command()
    async def play(
        self,
        ctx: ApplicationContext,
        video: Option(str, autocomplete=youtube_video_autocompletion),
    ):
        YDL_OPTIONS = {"format": "bestaudio/best[height<=480]", "noplaylist": "True"}
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if is_youtube_link(video):
            url = video
        else:
            videos_search = VideosSearch(video, limit=5)
            results = videos_search.result()
            url = results["result"][0]["link"]

        if not voice.is_playing():
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
            voice.play(
                FFmpegPCMAudio(
                    info["url"], **{"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}
                )
            )
            voice.is_playing()
            await ctx.send(f"Playing! {url}")

        # check if the bot is already playing
        else:
            await ctx.send("Bot is already playing! Please Stop it first with /stop")
            return

    # command to resume voice if it is paused
    @commands.command()
    async def resume(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if not voice.is_playing():
            voice.resume()
            await ctx.send("Resuming stream")

    # command to pause voice if it is playing
    @commands.command()
    async def pause(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.pause()
            await ctx.send("Paused stream")

    # command to stop voice
    @commands.command()
    async def stop(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.stop()
            await ctx.send("Stopping stream...")


def setup(bot):
    bot.add_cog(Music(bot))
