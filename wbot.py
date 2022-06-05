from nextcord.ext import commands
import nextcord
import ctypes
import os
import asyncio
from dotenv import load_dotenv
#load .env
load_dotenv()
# bot setup + opus lib check
intents = nextcord.Intents.default()
intents.members = True
joeybot = commands.Bot(command_prefix='!', intents=intents)
nextcord.opus.load_opus(ctypes.util.find_library("opus"))
print("opus found =", nextcord.opus.is_loaded())
# runs when bot starts


@joeybot.event
async def on_ready():
    print(f'Logged in as {joeybot.user.name}\n' + 'Connected to:')
    guilds = joeybot.guilds
    # set default join state
    global Join
    Join = True
    # sets target id's to vars
    global joey, jack
    # for test
    #joey = int(os.getenv('greg-id'))
    ################################
    joey = int(os.getenv('joey-id'))
    jack = int(os.getenv('jack-id'))
    for server in guilds:
        print(server.name)
# commented out used to annoy joey and jack
# @joeybot.event
# async def on_voice_state_update(member, before, after):
#     global joey,jack
#     if Join == True:
#         if before.channel is None:
#             print(member.name + " has joined")
#             await asyncio.sleep(1)
#             if member.id == joey:
#                 pain = await member.voice.channel.connect()
#                 FILE="whiteboy.opus"
#                 pain.play(nextcord.FFmpegOpusAudio(FILE))
#                 await asyncio.sleep(4)
#                 await pain.disconnect()
#             elif member.id == jack:
#                 pain = await member.voice.channel.connect()
#                 FILE="em-ahh.opus"
#                 pain.play(nextcord.FFmpegOpusAudio(FILE))
#                 await asyncio.sleep(4)
#                 await pain.disconnect()
#     else: print("Join not active")
# Main CMD COG


class Main(commands.Cog, name='Main'):
    def __init__(self, bot):
        self.bot = joeybot

    # @commands.command(name='togglejoin', brief='Toggles autojoin bomb')
    # async def togglejoey(self,ctx):
    #     global Join
    #     if Join == False:
    #         Join=True
    #         await ctx.send("Join is now enabled.")
    #     elif Join == True:
    #         Join=False
    #         await ctx.send("Join is now disabled.")

    @commands.command(brief='Makes bot leave the channel')
    async def leave(self, ctx):
        vc = nextcord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if vc is None:
            await ctx.send("I'm not in a voice channel",delete_after=100)
        else:
            await ctx.voice_client.disconnect()
            await ctx.send("Leaving",delete_after=100)
    
    @commands.command(brief='Makes bot join the channel')
    async def join(self,ctx):
        vc = nextcord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if vc is None:
            await ctx.author.voice.channel.connect()    
        else:
            await ctx.send("I'm in a voice channel",delete_after=100)

joeybot.load_extension('music')
joeybot.add_cog(Main(joeybot))
joeybot.run(os.getenv('TOKEN'))
