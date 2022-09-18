from ast import Global
from secrets import choice
from nextcord.ext import commands
import nextcord
from yt_dlp import YoutubeDL
import json
from youtube_search import YoutubeSearch


class Music(commands.Cog):
    def __init__(self, wbot: commands.Bot):
        self.bot = wbot
        self.queue_list = []
        self.title = []

    @nextcord.slash_command(name='play', description='play a video')
    async def play(self, ctx, video=None):
        vc = nextcord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        #dropdown menu
        class search_select(nextcord.ui.Select):
            def __init__(self, search):
                options=[  
                    nextcord.SelectOption(label=search[0]['title'],emoji="📹",description="Channel: " + search[0]['channel'] 
                    + ' Duration: ' + search[0]['duration'] + ' Published: ' + search[0]['publish_time']),
                    nextcord.SelectOption(label=search[1]['title'],emoji="📹",description="Channel: " + search[1]['channel'] 
                    + ' Duration: ' + search[1]['duration'] + ' Published: ' + search[1]['publish_time']),
                     nextcord.SelectOption(label=search[2]['title'],emoji="📹",description="Channel: " + search[2]['channel'] 
                    + ' Duration: ' + search[2]['duration'] + ' Published: ' + search[2]['publish_time']),
                     nextcord.SelectOption(label=search[3]['title'],emoji="📹",description="Channel: " + search[3]['channel'] 
                    + ' Duration: ' + search[3]['duration'] + ' Published: ' + search[3]['publish_time']), 
                    nextcord.SelectOption(label=search[4]['title'],emoji="📹",description="Channel: " + search[4]['channel'] 
                    + ' Duration: ' + search[4]['duration'] + ' Published: ' + search[4]['publish_time']),
                    ]
                super().__init__(placeholder="Select an option",max_values=1,min_values=1,options=options)
            async def callback(self, interaction: nextcord.Interaction):
                if self.values[0] == search[0]['title']:
                    SUFFIX = search[0]['url_suffix']
                elif self.values[0] == search[1]['title']:
                    SUFFIX = search[1]['url_suffix']
                elif self.values[0] == search[2]['title']:
                    SUFFIX = search[2]['url_suffix']
                elif self.values[0] == search[3]['title']:
                    SUFFIX = search[3]['url_suffix']
                elif self.values[0] == search[4]['title']:
                    SUFFIX = search[4]['url_suffix']
                URL = 'https://www.youtube.com' + SUFFIX
                print(URL)
                add(URL)
                await interaction.response.send_message(content=f"Adding to queue {URL}!",ephemeral=False)

                

        #view for dropdown menu
        class search_view(nextcord.ui.View):
            def __init__(self, search, *, timeout = 15):
                super().__init__(timeout=timeout)
                self.dropdown = search_select(search)
                self.add_item(self.dropdown)

        # youtube dl wrapper, returns audio url and title of video in a tuple
        def ytdl(URL):
            ydl_opts = {'format': 'bestaudio', }
            with YoutubeDL(ydl_opts) as ydl:
                video_info = ydl.extract_info(URL, download=False)
                print(video_info)
                return video_info['url'], video_info['title']

        def queue_loop(queue_list):
            if vc.is_connected() == True and len(self.queue_list) > 0:
                source = self.queue_list[0]
                print(source)
                self.queue_list.pop(0)
                self.title.pop(0)
                vc.play(nextcord.FFmpegPCMAudio(source),
                        after=lambda e: queue_loop(self.queue_list))
           
        if ctx.user.voice is None:
            await ctx.send("Please join a voice channel")
        elif video == None:
            vc.resume()
            await ctx.send("Playing", delete_after=100)
        else:
            channel = ctx.user.voice.channel
            global URL
            if vc is None:
                vc = await channel.connect()
            else:
                await vc.move_to(channel)
            if "https:" in video:
                 URL = video 

            else:
                search = YoutubeSearch(video, max_results=5).to_dict()
                search_dropdown = search_view(search)
                await ctx.send('Please select a video', view = search_dropdown)
        def add(URL):
            video_data = ytdl(URL)
            self.queue_list.append(video_data[0])
            self.title.append(video_data[1])
            #print(self.queue_list)
            if not vc.is_playing():
                queue_loop(self.queue_list)

    @nextcord.slash_command(name='pause', description='pause audio')
    async def pause(self, ctx):
        vc = nextcord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if vc is None:
            await ctx.send('Nothing is playing???', delete_after=100)
        else:
            vc.pause()
            await ctx.send('Audio paused', delete_after=100)

    @nextcord.slash_command(name='resume', description='resume audio')
    async def resume(self, ctx):
        vc = nextcord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if vc is None:
            await ctx.send('Nothing is playing???', delete_after=100)
        elif vc.is_playing() is True:
            await ctx.send('Audio is already playing', delete_after=100)
        else:
            vc.resume()
            await ctx.send('Resumed Playback', delete_after=100)

    @nextcord.slash_command(name='stop', description='stops audio and clears queue')
    async def stop(self, ctx):
        vc = nextcord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if vc.is_playing is False:
            await ctx.send('Nothing is playing???', delete_after=100)
        else:
            vc.stop()
            self.queue_list.clear()
            self.title.clear()
            await ctx.send('Stopped Playback', delete_after=100)

    @nextcord.slash_command(name='skip', description='skips what is playing')
    async def stop(self, ctx):
        vc = nextcord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if vc.is_playing is False:
            await ctx.send('Nothing is playing???', delete_after=100)
        else:
            vc.stop()
            await ctx.send('Skipped', delete_after=100)

    @nextcord.slash_command(name='queue', description='show queue')
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


def setup(wbot):
    wbot.add_cog(Music(wbot))
