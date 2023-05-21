from discord.ext import commands
import discord
import ctypes
import os
import asyncio
from dotenv import load_dotenv
#load .env
load_dotenv()
# bot setup + opus lib check
intents = discord.Intents.default()
intents.members = True
intents.messages = True
#intents.message_content = True
wbot = commands.Bot()
discord.opus.load_opus(ctypes.util.find_library("opus"))
print("opus found =", discord.opus.is_loaded())

# runs when bot starts
@wbot.event
async def on_ready():
    print(f'Logged in as {wbot.user.name}\n' + 'Connected to:')
    guilds = wbot.guilds
    for server in guilds:
        print(server.name)

# Main CMD COG
class Main(commands.Cog, name='Main'):
    def __init__(self, bot: commands.Bot):
        self.bot = wbot

    @discord.slash_command(description='Makes bot leave the channel')
    async def leave(self, ctx):
        vc = discord.utils.get(wbot.voice_clients, guild=ctx.guild)
        if vc is None:
            await ctx.respond("I'm not in a voice channel",delete_after=100)
        else:
            await ctx.guild.voice_client.disconnect()
            await ctx.respond("Leaving",delete_after=100)
    
    @discord.slash_command(description='Makes bot join the channel')
    async def join(self,ctx):
        vc = discord.utils.get(wbot.voice_clients, guild=ctx.guild)
        if vc is None:
            await ctx.user.voice.channel.connect()
            await ctx.respond("Joining",delete_after=100)    
        else:
            await ctx.respond("I'm in a voice channel",delete_after=100)

wbot.load_extension('music')
wbot.add_cog(Main(wbot))
wbot.run(os.getenv('TOKEN'))
