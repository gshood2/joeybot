from nextcord.ext import commands
import nextcord
import ctypes
import os
import asyncio
from dotenv import load_dotenv
#load .env
load_dotenv()
#sets target
targetMember = int(os.getenv('TARGET')) 
#bot setup + opus lib check
intents = nextcord.Intents.default()
intents.members = True
wbot = commands.Bot(command_prefix='!', intents=intents)
nextcord.opus.load_opus(ctypes.util.find_library("opus"))
print("opus found =", nextcord.opus.is_loaded())

@wbot.event
async def on_ready():
    print(f'Logged in as {wbot.user.name}\n' + 'Connected to:')
    guilds = wbot.guilds
    for server in guilds:
        print(server.name)

@wbot.event
async def on_voice_state_update(member, before, after):

    if before.channel is None and member.id == targetMember:
        #print(member.name + " has joined")
        channel = member.voice.channel
        await asyncio.sleep(1)
        whiteboy = await channel.connect()
        whiteboy.play(nextcord.FFmpegPCMAudio('whiteboy.mp3')) 
        await asyncio.sleep(4)
        await whiteboy.disconnect()

@wbot.command(name='bomb',category= 'malice',description='bomb voice channel')
async def cm(ctx,target,file):
    Guild=ctx.message.guild
    members = await Guild.fetch_members().flatten()
    for member in members:
        if target == member.nick:
            channel = member.voice.channel
            bomb = await channel.connect()
            bomb.play(nextcord.FFmpegOpusAudio(file))
            await asyncio.sleep(10)
            await whiteboy.disconnect()

    
   

wbot.run(os.getenv('TOKEN'))
