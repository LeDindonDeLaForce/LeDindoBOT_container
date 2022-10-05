import asyncio
import datetime
import logging
import os
import wikiquote
import humanize
import random
import pyjokes
from blagues_api import BlaguesAPI, BlagueType ##GIT https://github.com/Blagues-API/blagues-api-py

from twitchio import User
from twitchio.ext import commands

# Sets humanize to French language
humanize.i18n.activate("fr_FR")


class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.game_id = {}
        random.seed(datetime.datetime.now())
        #joketoken=os.environ['JOKE_TOKEN']i

    @commands.command(name="dindoban")
    async def leixban(self, ctx: commands.Context, user):
        await ctx.send(f"Non t'abuses {ctx.author.name}, on va pas ban {user} quand meme BibleThump")

    @commands.command(name="salut", aliases=['slt'])
    async def salut(self, ctx: commands.Context, user: User = None):
        if not user:
            user = ctx.author
        await ctx.send(f'Salut, comment ça va @{user.name} ? <3')

    @commands.command(name="bn")
    async def bn(self, ctx: commands.Context, user: User = None):
        if not user:
            user = ctx.author
        await ctx.send(f'Fais de beaux rêves @{user.name} <3')

    @commands.command(name="uptime")
    async def uptime(self, ctx: commands.bot.Context):
        stream = await self.bot.fetch_streams(
            user_logins=[
                ctx.author.channel.name
            ])

        if len(stream) == 0:
            return await ctx.send("Il n'y a pas de live en cours :(")

        uptime = datetime.datetime.now(
            datetime.timezone.utc) - stream[0].started_at
        await ctx.send(f"Ton streamer préféré est en live depuis {humanize.precisedelta(uptime, minimum_unit='seconds')}")

    @commands.command(name="cursed")
    async def cursed(self, ctx: commands.Context):
        await ctx.send("C'est non")

    @commands.command(name="lurk")
    async def lurk(self, ctx: commands.Context):
        await ctx.send(f'{ctx.author.name} passe en lurk! TakeNRG ')

    @commands.command(name='shoutout', aliases=['so'])
    async def shoutout(self, ctx: commands.Context, broadcaster: User):
        await ctx.send('yapadeso')
        if 'vip' in ctx.author.badges or ctx.author.is_mod:
            channel_info = await self.bot.fetch_channel(broadcaster.name)
            await asyncio.sleep(5)
            if channel_info.game_name:
                await ctx.send(
                    f'Je plaisante haha, allez voir @{broadcaster.name} sur www.twitch.tv/{broadcaster.name} pour du gaming de qualitay sur {channel_info.game_name}'
                )
            else:
                await ctx.send(
                    f"Je plaisante haha, @{broadcaster.name} ne stream pas mais c'est quelqu'un de super cool SeemsGood"
                )

    @commands.command(name="porte")
    async def porte(self, ctx: commands.Context):
        await ctx.send("Vision d'artiste")

    @commands.command(name="ref")
    async def ref(self, ctx: commands.Context):
        await ctx.send('glaref MrDestructoid')

    @commands.command(name="cam")
    async def cam(self, ctx: commands.Context):
        await ctx.send('MET LA CAM')
        



    @commands.command()
    async def id(self, ctx: commands.Context):
        if ctx.author.channel.name not in self.game_id:
            await ctx.send("Il n'y a pas d'id :(")
        else:
            await ctx.send(self.game_id[ctx.author.channel.name])

    @commands.command(name="setId")
    async def setId(self, ctx: commands.Context, *id):
        if ctx.author.is_mod:
            self.game_id[ctx.author.channel.name] = ' '.join(id)
            await ctx.send('id set SeemsGood')

    @commands.command(name="joke")
    async def joke(self, ctx: commands.Context):
        joke=pyjokes.get_joke(language='en', category= 'all')
        await ctx.send(joke)

    @commands.command(name="blague")
    async def blagueapi(self, ctx: commands.Context):
        blagues=BlaguesAPI("TOKEN") #token a récupérer sur https://www.blagues-api.fr/
        rep = await blagues.random(disallow=[BlagueType.DARK,BlagueType.LIMIT,BlagueType.BEAUF])
        await ctx.send("[" + rep.type.capitalize() + "] : " + rep.joke)
        await asyncio.sleep(3)
        await ctx.send(rep.answer + " Kappa")

def prepare(bot: commands.Bot):
    bot.add_cog(Misc(bot))
