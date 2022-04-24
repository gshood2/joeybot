from nextcord.ext import commands
import nextcord
import yt_dlp

class Music(commands.Cog):
    @commands.command()
    async def leave(self,ctx):
        await ctx.voice_client.disconnect

def setup(joeybot):
    joeybot.add_cog(Music(joeybot))