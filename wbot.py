from nextcord.ext import commands
import nextcord
import ctypes
import os
import asyncio
from dotenv import load_dotenv
#load .env
load_dotenv()
#bot setup + opus lib check
intents = nextcord.Intents.default()
intents.members = True
joeybot = commands.Bot(command_prefix='!', intents=intents)
nextcord.opus.load_opus(ctypes.util.find_library("opus"))
print("opus found =", nextcord.opus.is_loaded())
#runs when bot starts
@joeybot.event
async def on_ready():
    print(f'Logged in as {joeybot.user.name}\n' + 'Connected to:')
    guilds = joeybot.guilds
    #set default join state
    global Join
    Join=True
    #sets target id's to vars
    global joey,jack
    #for test 
    #joey = int(os.getenv('greg-id'))
    ################################
    joey = int(os.getenv('joey-id')) 
    jack = int(os.getenv('jack-id')) 
    for server in guilds:
        print(server.name)

@joeybot.event
async def on_voice_state_update(member, before, after):
    global joey,jack
    if Join == True:
        if before.channel is None:
            print(member.name + " has joined")
            await asyncio.sleep(1)
            if member.id == joey:
                pain = await member.voice.channel.connect()
                FILE="whiteboy.opus"
                pain.play(nextcord.FFmpegOpusAudio(FILE))
                await asyncio.sleep(4)
                await pain.disconnect()
            elif member.id == jack:
                pain = await member.voice.channel.connect()
                FILE="em-ahh.opus"
                pain.play(nextcord.FFmpegOpusAudio(FILE))
                await asyncio.sleep(4)
                await pain.disconnect()
    else: print("join not active")

@joeybot.command(name='bomb',description='bomb voice channel')
async def bomb(ctx,target,filename):
        Guild=ctx.message.guild
        tfile = filename + ".opus"
        members = await Guild.fetch_members().flatten()
        for member in members:
            if target == member.nick:
                channel = member.voice.channel
                bomb = await channel.connect()
                bomb.play(nextcord.FFmpegOpusAudio(tfile))
                await asyncio.sleep(10)
                await bomb.disconnect()

@joeybot.command(name='togglejoin')
async def togglejoey(ctx):
    global Join
    if Join == False:
        Join=True
        await  ctx.send("Join is now enabled")
    elif Join == True:
        Join=False
        await  ctx.send("Join is now disabled")
    
   

joeybot.run(os.getenv('TOKEN'))
