import discord

import io
import aiohttp
import asyncio


from .utils import checks
from discord.ext import commands
from .utils.dataIO import dataIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class plottest:
    def __init__(self, bot):
        self.bot = bot
		
    @commands.command(pass_context=True, no_pm=True, name='chart')
    async def chart(self, context):
        plt.switch_backend('Agg')
        plt.plot([1,2,3])

        plot_filename = 'plot.png'
        plot_name = ""
        
        facecolor = '#32363b'
        edgecolor = '#eeeeee'
        spinecolor = '#999999'
        footercolor = '#999999'
        labelcolor = '#cccccc'
        tickcolor = '#999999'
        titlecolor = '#ffffff'

        with io.BytesIO() as f:
            plt.savefig(
                f, format="png", facecolor=facecolor,
                edgecolor=edgecolor, transparent=True)
            f.seek(0)
            await context.bot.send_file(
                context.message.channel,
                f,
                filename=plot_filename,
                content=plot_name)

        fig.clf()
        plt.clf()
        plt.cla()


def setup(bot):
    n = plottest(bot)
    bot.add_cog(n)