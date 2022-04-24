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
    
    @commands.command(name='play',brief='play a video')
    async def play(self,ctx,url): 
        if ctx.message.author.voice is None:
            await ctx.send("Please join a voice channel")
        else:
            ydl_opts = {'format': 'bestaudio',}
            channel = ctx.message.author.voice.channel 
            vc = nextcord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
            if vc is None:
                voice = await channel.connect()
            else:
                await ctx.voice_client.disconnect()
                voice = await channel.connect()
            with YoutubeDL(ydl_opts) as ydl:
                video_info = ydl.extract_info(url,download=False)
            voice.play(nextcord.FFmpegPCMAudio(video_info['url']))

def setup(joeybot):
    joeybot.add_cog(Music(joeybot))