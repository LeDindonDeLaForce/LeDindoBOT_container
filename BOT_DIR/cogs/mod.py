import logging
import os

from twitchio import Channel, Game, User
from twitchio.ext import commands


class Mod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.author.is_mod

    async def cog_command_error(self, ctx, error):
        """
        Not functional yet. Waiting for a twitchio fix.
        """
        logging.info(
            'User not moderator'
        )

    @commands.command(name="ban")
    async def ban(self, ctx: commands.Context, user: User = None, *reason):
        logging.info(f'User {user.name} has been banned')
        if not reason:
            reason = 'Rise of the machines'
        else:
            reason = ' '.join(reason)
        await ctx.send(f"/ban {user.name} {reason}")
        await ctx.send(f"Au revoir {user.name} HeyGuys")

    @commands.command(name="unban")
    async def unban(self, ctx: commands.Context, user: User = None):
        logging.info(f'User {user.name} has been unbanned')
        await ctx.send(f"/unban {user.name}")
        await ctx.send(f"Bon retour parmi nous {user.name} HeyGuys !")

    @commands.command(name="title")
    async def title(self, ctx: commands.Context, *title):
        user = await ctx.author.channel.user()
        success = await modify_stream(title=' '.join(title), user=user)
        if success:
            await ctx.send('Title updated SeemsGood')
        else:
            await ctx.send('Error MrDestructoid')

    @commands.command(name="game")
    async def game(self, ctx: commands.Context, *game_name):
        g: List["Games"] = await self.bot.fetch_games(names=[' '.join(game_name)])
        game: Game = g[0]
        user = await ctx.author.channel.user()

        success = await modify_stream(game_id=game.id, user=user)
        if success:
            await ctx.send('Game updated SeemsGood')
        else:
            await ctx.send('Error MrDestructoid')


def prepare(bot: commands.Bot):
    bot.add_cog(Mod(bot))
