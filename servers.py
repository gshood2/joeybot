from nextcord.ext import commands
import nextcord
import os
from dotenv import load_dotenv
import subprocess


class servers(commands.Cog):
    def __init__(self, ctx):
        self.ph = 1

    @commands.command(name="ip", brief="get ip for a game server")
    async def ip(self, ctx, game):
        ip = os.getenv('MY-IP')
        game = game.casefold()
        if game == "rust":
            port = '28015'
        elif game == "minecraft" or "mc":
            port = '25565'
        else:
            ctx.send('invalid game', delete_after=5)
        server_address = ip + ":" + port
        member = ctx.author
        await ctx.send('check your dm\'s', delete_after=3)
        await member.send(server_address, delete_after=300)

    @commands.command(name="status", brief="see the status of a server")
    async def status(self, ctx, game):
        local_ip = os.getenv('local-ip')
        game = game.casefold()
        if game == "rust":
            port = '28015'
        elif game == 'minecraft' or 'mc':
            port = '25565'

        test = subprocess.run(
            ['nc', '-uzv', local_ip, port], capture_output=True)
        output = test.stderr.decode('utf-8')
        if output == '':
            await ctx.send(game + ' server is not active', delete_after=30)
        else:
            await ctx.send(output, delete_after=30)
            await ctx.send(game + ' server is active', delete_after=30)


def setup(wbot):
    wbot.add_cog(servers(wbot))
