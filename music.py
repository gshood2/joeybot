from nextcord.ext import commands
import nextcord
from yt_dlp import YoutubeDL
import json




queue= ('1','2','3')


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
    
    @commands.command(name='pause',brief='pause audio')
    async def pause(self,ctx):
        vc = nextcord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if vc is None:
            await ctx.send('Nothing is playing???')
        else:
            vc.pause()
            await ctx.send('Audio paused')

    @commands.command(name='resume',brief='resume audio')
    async def resume(self,ctx):
        vc = nextcord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if vc is None:
            await ctx.send('Nothing is playing???')
        elif vc.is_playing() is True:
            await ctx.send('Audio is already playing')
        else:
            vc.resume()
            await ctx.send('Resumed Playback')

    @commands.command(name='stop',brief='stop audio')
    async def stop(self,ctx):
        vc = nextcord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if vc is None:
            await ctx.send('Nothing is playing???')
        else:
            vc.stop()
            await ctx.send('Stopped Playback')

def setup(joeybot):
    joeybot.add_cog(Music(joeybot))