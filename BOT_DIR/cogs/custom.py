import datetime
import logging
import os

from twitchio.ext import commands

import custom_commands


class CustomCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.author.is_mod

    @commands.command(name="cmdadd")
    async def cmdadd(self, ctx: commands.Context, command, *text):
        channel = ctx.author.channel.name.lower()
        text = ' '.join(text)

        custom_commands.add_command(command, channel, text)

        await ctx.send(f"Commande {command} ajoutée avec succès MrDestructoid")

    @commands.command(name="cmdedit")
    async def cmdedit(self, ctx: commands.Context, command, *text):
        channel = ctx.author.channel.name.lower()
        text = ' '.join(text)

        custom_commands.edit_command(command, channel, text)

        await ctx.send(f"Commande {command} editée avec succès MrDestructoid")

    @commands.command(name="cmdremove")
    async def cmdremove(self, ctx: commands.Context, command):
        channel = ctx.author.channel.name.lower()

        custom_commands.remove_command(command, channel)

        await ctx.send(f"Commande {command} retirée avec succès MrDestructoid")



def prepare(bot: commands.Bot):
    bot.add_cog(CustomCommand(bot))
