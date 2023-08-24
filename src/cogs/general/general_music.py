"""
A youtube music-bot functionality
"""
import logging
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from pathlib import Path
from yt_dlp import YoutubeDL

logger = logging.getLogger(__name__)


class Music(commands.Cog):
    """
    # Hits the catfact API and returns the response.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def join(self, ctx):
        """
        command for bot to join the channel of the user, if
        the bot has already joined and is in a different
        channel, it will move to the channel the user is in

        """
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

    @commands.slash_command()
    async def play(self, ctx, url):
        """
        command to play sound from a youtube URL
        """
        executable = Path(__file__).parent / 'ffmpeg' / 'bin' / 'ffmpeg.exe'
        YDL_OPTIONS = {'format': 'bestaudio/best[height<=480]', 'noplaylist': 'True'}
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
            , 'options': '-vn'
            , 'executable': executable}
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if not voice.is_playing():
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
            URL = info['url']
            voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            voice.is_playing()
            await ctx.send(f'Playing.')

        # check if the bot is already playing
        else:
            await ctx.send("Bot is already playing")
            return

    @commands.slash_command()
    async def resume(self, ctx):
        """
        command to resume voice if it is paused
        """
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if not voice.is_playing():
            voice.resume()
            await ctx.send('Resuming')

    @commands.slash_command()
    async def pause(self, ctx):
        """
        command to pause voice if it is playing
        """
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.pause()
            await ctx.send('Paused')

    @commands.slash_command()
    async def stop(self, ctx):
        """
        command to stop voice
        """
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.stop()
            await ctx.send('Stopping...')


def setup(bot):
    """
    Required.
    """
    bot.add_cog(Music(bot))
