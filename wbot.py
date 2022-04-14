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
wbot = commands.Bot(command_prefix='!', intents=intents)
nextcord.opus.load_opus(ctypes.util.find_library("opus"))
print("opus found =", nextcord.opus.is_loaded())
# set up cmd privelages
@wbot.event
async def on_ready():
    print(f'Logged in as {wbot.user.name}\n' + 'Connected to:')
    guilds = wbot.guilds
    #set join state
    global Join
    Join=True
    #sets target id's
    global joey,jack
    joey = int(os.getenv('joey-id')) 
    jack = int(os.getenv('jack-id')) 
    for server in guilds:
        print(server.name)

@wbot.event
async def on_voice_state_update(member, before, after):
    if Join == True:
        if before.channel is None and member.id == joey or jack:
            #print(member.name + " has joined")
            channel = member.voice.channel
            await asyncio.sleep(1)
            pain = await channel.connect()
            if member.id == joey:
                pain.play(nextcord.FFmpegPCMAudio('whiteboy.mp3'))
            elif member.id == jack:
                 pain.play(nextcord.FFmpegOpusAudio('em-ahh.'))
            await asyncio.sleep(4)
            await pain.disconnect()
    else: print("join not active")

@wbot.command(name='bomb',description='bomb voice channel')
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

@wbot.command(name='togglejoey')
async def togglejoey(ctx):
    global Join
    if Join == False:
        Join=True
        await  ctx.send("white boy clip on Joey join is now enabled")
    elif Join == True:
        Join=False
        await  ctx.send("white boy clip on Joey join is now disabled")
    
   

wbot.run(os.getenv('TOKEN'))
