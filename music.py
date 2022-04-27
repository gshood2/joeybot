from nextcord.ext import commands
import nextcord
from yt_dlp import YoutubeDL
import json
from youtube_search import YoutubeSearch




queue= ('1','2','3')


class Music(commands.Cog):
    
    @commands.command(name='play',brief='play a video')
    async def play(self,ctx,video): 
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
            if "https:" in video:
                with YoutubeDL(ydl_opts) as ydl:
                    video_info = ydl.extract_info(video,download=False)
                voice.play(nextcord.FFmpegPCMAudio(video_info['url']))
            else:
                search = YoutubeSearch(video, max_results=5).to_dict()
                Result1=search[0]
                Result2=search[1]
                Result3=search[2]
                Result4=search[3]
                Result5=search[4]
                await ctx.send('Please select a video')
                await ctx.send('1 ' + Result1['title'] + '\n2 ' + Result2['title'] + '\n3 ' + Result3['title']+ '\n4 ' + Result4['title'] + '\n5 ' + Result5['title'])
                def msgCheck(msg):
                    return msg.channel == ctx.channel
                SUFFIX = None
                while SUFFIX is None:
                    Choice = await ctx.bot.wait_for('message', check=msgCheck, timeout=30)
                    if Choice.content == '1':
                        SUFFIX=Result1
                    elif Choice.content == '2':
                        SUFFIX=Result2
                    elif Choice.content == '3':
                        SUFFIX=Result3 
                    elif Choice.content == '4':
                        SUFFIX=Result4 
                    elif Choice.content == '5':
                        SUFFIX=Result5
                    else:
                        await ctx.send('Invalid choice') 
                URL = 'https://www.youtube.com' + SUFFIX['url_suffix']
                with YoutubeDL(ydl_opts) as ydl:
                    video_info = ydl.extract_info(URL,download=False)
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