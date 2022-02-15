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
wbot = commands.Bot(command_prefix='!')
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

wbot.run(os.getenv('TOKEN'))
