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
wbot = commands.Bot(command_prefix='!', intents=intents)
nextcord.opus.load_opus(ctypes.util.find_library("opus"))
print("opus found =", nextcord.opus.is_loaded())

# runs when bot starts
@wbot.event
async def on_ready():
    print(f'Logged in as {wbot.user.name}\n' + 'Connected to:')
    guilds = wbot.guilds
    for server in guilds:
        print(server.name)

# Main CMD COG
class Main(commands.Cog, name='Main'):
    def __init__(self, bot):
        self.bot = wbot

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

wbot.load_extension('music')
wbot.load_extension('servers')
wbot.add_cog(Main(wbot))
wbot.run(os.getenv('TOKEN'))
