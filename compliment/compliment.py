import discord
from discord.ext import commands
from .utils.dataIO import fileIO
from random import choice as randchoice
import os


class Compliment:

    """Compliment Cog"""
    def __init__(self, bot):
        self.bot = bot
        self.compliments = fileIO("data/compliment/compliment.json", "load")

    @commands.command(pass_context=True, no_pm=True, aliases=["cpl"])
    async def compliment(self, ctx, user : discord.Member=None):
        """Compliment the user"""

        msg = ' '
        if user != None:

            if user.id == self.bot.user.id:
                user = ctx.message.author
                msg = [" Hey I appreciate the compliment! :smile:", "No ***YOU'RE*** awesome! :smile:"]
                await self.bot.say(user.mention + randchoice(msg))

            else:
                await self.bot.say(user.mention + msg + randchoice(self.compliments))
        else:
            await self.bot.say(ctx.message.author.mention + msg + randchoice(self.compliments))


def check_folders():
    if not os.path.exists("data/compliment"):
        print("Creating data/compliment folder...")
        os.makedirs("data/compliment")


def check_files():

    if not fileIO("data/compliment/compliment.json", "check"):
        print("Creating empty compliment.json...")
        fileIO("data/compliment/compliment.json", "save", [])


def setup(bot):
    check_folders()
    check_files()
    n = Compliment(bot)
    bot.add_cog(n)
