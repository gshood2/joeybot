from nextcord.ext import commands
import nextcord
from yt_dlp import YoutubeDL
import json
from youtube_search import YoutubeSearch


class Music(commands.Cog):
    def __init__(self, ctx):
        self.queue = []
        self.title = []

    @commands.command(name='play', brief='play a video')
    async def play(self, ctx, video=None, *args):
        # adds any futher arguments to video arg
        for x in args:
            video = video + ' ' + x
        vc = nextcord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

        # youtube dl wrapper, returns audio url and title of video in a tuple
        def ytdl(URL):
            ydl_opts = {'format': 'bestaudio', }
            with YoutubeDL(ydl_opts) as ydl:
                video_info = ydl.extract_info(URL, download=False)
                return video_info['url'], video_info['title']

        def queue_loop(queue):
            if vc.is_connected() == True and len(self.queue) > 0:
                source = self.queue[0]
                self.queue.pop(0)
                self.title.pop(0)
                vc.play(nextcord.FFmpegPCMAudio(source),
                        after=lambda e: queue_loop(self.queue))

        if ctx.message.author.voice is None:
            await ctx.send("Please join a voice channel")
        elif video == None:
            vc.resume()
            await ctx.send("Playing", delete_after=100)
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
                Result1 = search[0]
                Result2 = search[1]
                Result3 = search[2]
                Result4 = search[3]
                Result5 = search[4]
                await ctx.send('Please select a video', delete_after=100)
                await ctx.send('1 ' + Result1['title'] + '\n2 ' + Result2['title'] + '\n3 ' + Result3['title'] + '\n4 ' + Result4['title'] + '\n5 ' + Result5['title'], delete_after=100)

                def msgCheck(msg):
                    return msg.channel == ctx.channel
                SUFFIX = None
                while SUFFIX is None:
                    Choice = await ctx.bot.wait_for('message', check=msgCheck, timeout=15)
                    if Choice.content == '1':
                        SUFFIX = Result1
                    elif Choice.content == '2':
                        SUFFIX = Result2
                    elif Choice.content == '3':
                        SUFFIX = Result3
                    elif Choice.content == '4':
                        SUFFIX = Result4
                    elif Choice.content == '5':
                        SUFFIX = Result5
                    else:
                        await ctx.send('Invalid choice')
                URL = 'https://www.youtube.com' + SUFFIX['url_suffix']
            # title has index of 1, audio has index of 0
            video_data = ytdl(URL)
            # add vid data to queue
            self.queue.append(video_data[0])
            self.title.append(video_data[1])
            playTitle = video_data[1]
            await ctx.send(playTitle + " added to queue", delete_after=100)
            if not vc.is_playing():
                queue_loop(self.queue)

    @commands.command(name='pause', brief='pause audio')
    async def pause(self, ctx):
        vc = nextcord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if vc is None:
            await ctx.send('Nothing is playing???', delete_after=100)
        else:
            vc.pause()
            await ctx.send('Audio paused', delete_after=100)

    @commands.command(name='resume', brief='resume audio')
    async def resume(self, ctx):
        vc = nextcord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if vc is None:
            await ctx.send('Nothing is playing???', delete_after=100)
        elif vc.is_playing() is True:
            await ctx.send('Audio is already playing', delete_after=100)
        else:
            vc.resume()
            await ctx.send('Resumed Playback', delete_after=100)

    @commands.command(name='stop', brief='stops audio and clears queue')
    async def stop(self, ctx):
        vc = nextcord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if vc.is_playing is False:
            await ctx.send('Nothing is playing???', delete_after=100)
        else:
            vc.stop()
            self.queue.clear()
            self.title.clear()
            await ctx.send('Stopped Playback', delete_after=100)

    @commands.command(name='skip', brief='skips what is playing')
    async def stop(self, ctx):
        vc = nextcord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if vc.is_playing is False:
            await ctx.send('Nothing is playing???', delete_after=100)
        else:
            vc.stop()
            await ctx.send('Skipped', delete_after=100)

    @commands.command(name='queue', brief='show queue')
    async def queue(self, ctx):
        if len(self.title) > 0:
            queue_num = 0
            queue_list = ''
            for title in self.title:
                queue_num += 1
                number = str(queue_num)
                queue_list = queue_list + number + ' ' + title + ' \n'
            await ctx.send(queue_list, delete_after=100)
        else:
            await ctx.send('Nothing is queued', delete_after=100)


def setup(joeybot):
    joeybot.add_cog(Music(joeybot))
