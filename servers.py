from nextcord.ext import commands
import nextcord
import os

from dotenv import load_dotenv


class servers(commands.Cog):
    def __init__(self, ctx):
        self.ph = 1
    
    @commands.command(name="ip", brief="get ip for a game server" )
    async def ip(self, ctx, game):
        ip = os.getenv('MY-IP')
        if game.casefold() == "rust":
            port = '28015'
        elif game.casefold == "minecraft" or "mc":
            port = '25565'
        server_address = ip + ":" + port
        member = ctx.author
        await member.send( server_address, delete_after=100)




def setup(wbot):
    wbot.add_cog(servers(wbot))