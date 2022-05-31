from nextcord.ext import commands
import nextcord
from yt_dlp import YoutubeDL
import json
from youtube_search import YoutubeSearch
from queue import Queue
import time








class Music(commands.Cog):

    @commands.command(name='play',brief='play a video')
    async def play(self,ctx,video=None):
        #youtube dl wrapper and player
        def ytdl(URL):
                    ydl_opts = {'format': 'bestaudio',}
                    with YoutubeDL(ydl_opts) as ydl:
                        video_info = ydl.extract_info(URL,download=False)
                        return video_info['url'] 

        
        vc = nextcord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        queue = Queue(maxsize=100)
        def queue_loop(queue):
            if vc is not None and vc.is_connected() == True:
                while not queue.empty():
                    if vc.is_playing() == False:
                        print('test')
                        vc.play(nextcord.FFmpegPCMAudio(queue.get()))
                    else:
                        time.sleep(5)

        if ctx.message.author.voice is None:
            await ctx.send("Please join a voice channel")
        elif video==None:
            await ctx.send('Playing')
            await vc.resume()
        else:
            channel = ctx.message.author.voice.channel 
            if vc is None:
                vc = await channel.connect()
            else:
                await vc.move_to(channel)
            if "https:" in video:
                URL = video
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
                    Choice = await ctx.bot.wait_for('message', check=msgCheck, timeout=15)
                    if Choice.content == '1':
                        SUFFIX=Result1
                        TITLE=Result1['title']
                    elif Choice.content == '2':
                        SUFFIX=Result2
                        TITLE=Result2['title']
                    elif Choice.content == '3':
                        SUFFIX=Result3
                        TITLE=Result3['title']
                    elif Choice.content == '4':
                        SUFFIX=Result4 
                        TITLE=Result4['title']
                    elif Choice.content == '5':
                        SUFFIX=Result5
                        TITLE=Result5['title']
                    else:
                        await ctx.send('Invalid choice') 
                URL = 'https://www.youtube.com' + SUFFIX['url_suffix']
            #call queue
            queue.put(ytdl(URL))
            await ctx.send(TITLE + " added to queue")
            queue_loop(queue)
                

    
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