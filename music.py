from nextcord.ext import commands
import nextcord
from yt_dlp import YoutubeDL
import json




class queue():
    def __init__(self,one,two,three):
        self.one = None
        self.two = None
        self.three = None


class Music(commands.Cog):
    @commands.command()
    async def leave(self,ctx):
        await ctx.voice_client.disconnect()
        await ctx.send("leaving voice channel")
    
    @commands.command(name='play',brief='play a video')
    async def play(self,ctx,url):
        ydl_opts = {'format': 'bestaudio',}
        channel = await ctx.message.author.voice.channel.connect()
        with YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(url,download=False)
        channel.play(nextcord.FFmpegPCMAudio(video_info['url']))

def setup(joeybot):
    joeybot.add_cog(Music(joeybot))