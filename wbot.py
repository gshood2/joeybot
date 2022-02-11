from nextcord.ext import commands
import nextcord
import ctypes

# joey id = 416567736739823619
# my id = 308698142428364812
wbot = commands.Bot(command_prefix='!')
nextcord.opus.load_opus(ctypes.util.find_library("opus"))
print("opus found = ", nextcord.opus.is_loaded())

@wbot.event
async def on_ready():
    print(f'Logged in as {wbot.user}')


@wbot.event
async def on_voice_state_update(member, before, after):
    if member.id == 416567736739823619:
        print(member.name)
        channel = member.voice.channel
        whiteboy = await channel.connect()
        whiteboy.play(nextcord.FFmpegPCMAudio('whiteboy.mp3')) 
          

wbot.run('OTQxMzg4NTQ2NjI1OTEyOTcy.YgVOZw.9rzxm8zzL3nAw9MMnWPH81mXZpk')
