import discord
from discord.ext import commands
from .utils.dataIO import fileIO
from .utils import checks
from cogs.utils.chat_formatting import *
import os
import time
import aiohttp
import asyncio
from copy import deepcopy
import logging

class phStreams:
    """Streams

    Twitch, Hitbox and Beam alerts"""

    def __init__(self, bot):
        self.bot = bot
        self.twitch_streams = fileIO("data/streams/twitch.json", "load")
        self.hitbox_streams = fileIO("data/streams/hitbox.json", "load")
        self.beam_streams = fileIO("data/streams/beam.json", "load")

    @commands.command()
    async def hitbox(self, stream : str):
        """Checks if hitbox stream is online"""
        online = await self.hitbox_online(stream)
        if online is True:
            await self.bot.say("http://www.hitbox.tv/{}/ is online!".format(stream))
        elif online == False:
            await self.bot.say(stream + " is offline.")
        elif online == None:
            await self.bot.say("That stream doesn't exist.")
        else:
            await self.bot.say("Error.")

    @commands.command()
    async def twitch(self, stream : str):
        """Checks if twitch stream is online"""
        online = await self.twitch_online(stream)
        if online is True:
            await self.bot.say("http://www.twitch.tv/{} is online!".format(stream))
        elif online == False:
            await self.bot.say(stream + " is offline.")
        elif online == None:
            await self.bot.say("That stream doesn't exist.")
        else:
            await self.bot.say("Error.")

    @commands.command()
    async def beam(self, stream : str):
        """Checks if beam stream is online"""
        online = await self.beam_online(stream)
        if online is True:
            await self.bot.say("https://beam.pro/{} is online!".format(stream))
        elif online == False:
            await self.bot.say(stream + " is offline.")
        elif online == None:
            await self.bot.say("That stream doesn't exist.")
        else:
            await self.bot.say("Error.")

    @commands.group(pass_context=True)
    @checks.mod_or_permissions(manage_server=True)
    async def streamalert(self, ctx):
        """Adds/removes stream alerts from the current channel"""
        if ctx.invoked_subcommand is None:
            await self.bot.say("Type help streamalert for info.")

    @streamalert.command(name="twitch", pass_context=True)
    async def twitch_alert(self, ctx, stream : str):
        """Adds/removes twitch alerts from the current channel"""
        channel = ctx.message.channel
        check = await self.twitch_exists(stream)
        if check is False:
            await self.bot.say("That stream doesn't exist.")
            return
        elif check == "error":
            await self.bot.say("Couldn't contact Twitch API. Try again later.")
            return
        
        done = False

        for i, s in enumerate(self.twitch_streams):
            if s["NAME"] == stream:
                if channel.id in s["CHANNELS"]:
                    if len(s["CHANNELS"]) == 1:
                        self.twitch_streams.remove(s)
                        await self.bot.say("Alert has been removed from this channel.")
                        done = True
                    else:
                        self.twitch_streams[i]["CHANNELS"].remove(channel.id)
                        await self.bot.say("Alert has been removed from this channel.")
                        done = True
                else:
                    self.twitch_streams[i]["CHANNELS"].append(channel.id)
                    await self.bot.say("Alert activated. I will notify this channel everytime {} is live.".format(stream))
                    done = True

        if not done:
            self.twitch_streams.append({"CHANNELS" : [channel.id], "NAME" : stream, "ALREADY_ONLINE" : False})
            await self.bot.say("Alert activated. I will notify this channel everytime {} is live.".format(stream))

        fileIO("data/streams/twitch.json", "save", self.twitch_streams)

    @streamalert.command(name="hitbox", pass_context=True)
    async def hitbox_alert(self, ctx, stream : str):
        """Adds/removes hitbox alerts from the current channel"""
        channel = ctx.message.channel
        check = await self.hitbox_online(stream)
        if check == None:
            await self.bot.say("That stream doesn't exist.")
            return
        elif check == "error":
            await self.bot.say("Error.")
            return
        
        done = False

        for i, s in enumerate(self.hitbox_streams):
            if s["NAME"] == stream:
                if channel.id in s["CHANNELS"]:
                    if len(s["CHANNELS"]) == 1:
                        self.hitbox_streams.remove(s)
                        await self.bot.say("Alert has been removed from this channel.")
                        done = True
                    else:
                        self.hitbox_streams[i]["CHANNELS"].remove(channel.id)
                        await self.bot.say("Alert has been removed from this channel.")
                        done = True
                else:
                    self.hitbox_streams[i]["CHANNELS"].append(channel.id)
                    await self.bot.say("Alert activated. I will notify this channel everytime {} is live.".format(stream))
                    done = True

        if not done:
            self.hitbox_streams.append({"CHANNELS" : [channel.id], "NAME" : stream, "ALREADY_ONLINE" : False})
            await self.bot.say("Alert activated. I will notify this channel everytime {} is live.".format(stream))

        fileIO("data/streams/hitbox.json", "save", self.hitbox_streams)

    @streamalert.command(name="beam", pass_context=True)
    async def beam_alert(self, ctx, stream : str):
        """Adds/removes beam alerts from the current channel"""
        channel = ctx.message.channel
        check = await self.beam_online(stream)
        if check == None:
            await self.bot.say("That stream doesn't exist.")
            return
        elif check == "error":
            await self.bot.say("Error.")
            return
        
        done = False

        for i, s in enumerate(self.beam_streams):
            if s["NAME"] == stream:
                if channel.id in s["CHANNELS"]:
                    if len(s["CHANNELS"]) == 1:
                        self.beam_streams.remove(s)
                        await self.bot.say("Alert has been removed from this channel.")
                        done = True
                    else:
                        self.beam_streams[i]["CHANNELS"].remove(channel.id)
                        await self.bot.say("Alert has been removed from this channel.")
                        done = True
                else:
                    self.beam_streams[i]["CHANNELS"].append(channel.id)
                    await self.bot.say("Alert activated. I will notify this channel everytime {} is live.".format(stream))
                    done = True

        if not done:
            self.beam_streams.append({"CHANNELS" : [channel.id], "NAME" : stream, "ALREADY_ONLINE" : False})
            await self.bot.say("Alert activated. I will notify this channel everytime {} is live.".format(stream))

        fileIO("data/streams/beam.json", "save", self.beam_streams)

    @streamalert.command(name="stop", pass_context=True)
    async def stop_alert(self, ctx):
        """Stops all streams alerts in the current channel"""
        channel = ctx.message.channel

        to_delete = []

        for s in self.hitbox_streams:
            if channel.id in s["CHANNELS"]:
                if len(s["CHANNELS"]) == 1:
                    to_delete.append(s)
                else:
                    s["CHANNELS"].remove(channel.id)

        for s in to_delete:
            self.hitbox_streams.remove(s)

        to_delete = []

        for s in self.twitch_streams:
            if channel.id in s["CHANNELS"]:
                if len(s["CHANNELS"]) == 1:
                    to_delete.append(s)
                else:
                    s["CHANNELS"].remove(channel.id)

        for s in to_delete:
            self.twitch_streams.remove(s)

        to_delete = []

        for s in self.beam_streams:
            if channel.id in s["CHANNELS"]:
                if len(s["CHANNELS"]) == 1:
                    to_delete.append(s)
                else:
                    s["CHANNELS"].remove(channel.id)

        for s in to_delete:
            self.beam_streams.remove(s)

        fileIO("data/streams/twitch.json", "save", self.twitch_streams)
        fileIO("data/streams/hitbox.json", "save", self.hitbox_streams)
        fileIO("data/streams/beam.json", "save", self.beam_streams)

        await self.bot.say("There will be no more stream alerts in this channel.")


    async def hitbox_online(self, stream):
        url = "https://api.hitbox.tv/user/" + stream
        try:
            async with aiohttp.get(url) as r:
                data = await r.json()
            if data["is_live"] == "0":
                return False
            elif data["is_live"] == "1":
                return True
            elif data["is_live"] == None:
                return None
        except:
            return "error"

    async def twitch_online(self, stream):
        url =  "https://api.twitch.tv/kraken/streams?channel=" + stream
        try:
            async with aiohttp.get(url) as r:
                data = await r.json()
            if len(data["streams"]) > 0:
                return True
            else:
                return False
        except:
            return "error"
        return "error"

    async def beam_online(self, stream):
        url =  "https://beam.pro/api/v1/channels/" + stream
        try:
            async with aiohttp.get(url) as r:
                data = await r.json()
            if "online" in data:
                if data["online"] == True:
                    return True
                else:
                    return False
            elif "error" in data:
                return None
        except:
            return "error"
        return "error"

    async def twitch_exists(self, stream):
        url =  "https://api.twitch.tv/channels/" + stream
        try:
            async with aiohttp.get(url) as r:
                data = await r.json()
            if "error" in data:
                return False
            else:
                return True
        except:
            return "error"

    async def stream_checker(self):
        CHECK_DELAY = 60
        
        while self == self.bot.get_cog("Streams"):
            
            old = (deepcopy(self.twitch_streams), deepcopy(self.hitbox_streams), deepcopy(self.beam_streams))

            for stream in self.twitch_streams:
                online = await self.twitch_online(stream["NAME"])
                if online is True and not stream["ALREADY_ONLINE"]:
                    stream["ALREADY_ONLINE"] = True
                    for channel in stream["CHANNELS"]:
                        if self.bot.get_channel(channel):
                            await self.bot.send_message(self.bot.get_channel(channel), "http://www.twitch.tv/{} is online!".format(stream["NAME"]))
                else:
                    if stream["ALREADY_ONLINE"] and not online: stream["ALREADY_ONLINE"] = False
                await asyncio.sleep(0.5)
            
            for stream in self.hitbox_streams:
                online = await self.hitbox_online(stream["NAME"])
                if online is True and not stream["ALREADY_ONLINE"]:
                    stream["ALREADY_ONLINE"] = True
                    for channel in stream["CHANNELS"]:
                        if self.bot.get_channel(channel):
                            await self.bot.send_message(self.bot.get_channel(channel), "http://www.hitbox.tv/{} is online!".format(stream["NAME"]))
                else:
                    if stream["ALREADY_ONLINE"] and not online: stream["ALREADY_ONLINE"] = False
                await asyncio.sleep(0.5)

            for stream in self.beam_streams:
                online = await self.beam_online(stream["NAME"])
                if online is True and not stream["ALREADY_ONLINE"]:
                    stream["ALREADY_ONLINE"] = True
                    for channel in stream["CHANNELS"]:
                        if self.bot.get_channel(channel):
                            await self.bot.send_message(self.bot.get_channel(channel), "https://beam.pro/{} is online!".format(stream["NAME"]))
                else:
                    if stream["ALREADY_ONLINE"] and not online: stream["ALREADY_ONLINE"] = False
                await asyncio.sleep(0.5)

            if old != (self.twitch_streams, self.hitbox_streams, self.beam_streams):
                fileIO("data/streams/twitch.json", "save", self.twitch_streams)
                fileIO("data/streams/hitbox.json", "save", self.hitbox_streams)
                fileIO("data/streams/beam.json", "save", self.beam_streams)
      
            await asyncio.sleep(CHECK_DELAY)

    @commands.group(name = "slist", pass_context=True)
    async def slist(self, ctx):
        """List function to display streams that are enabled with Stream Alerts"""
        pass

    @slist.command(name = "twitch", pass_context=True)
    async def twitchlist(self):
        """Lists StreamAlerts turned on for Twitch"""
        await self.bot.say("Twitch Streams set up for Alerts:")
        twitempty = 1
        message = ""
        for item in self.twitch_streams:
            message += str(item["NAME"] + "\n")
            twitempty = 0
        await self.bot.say(box(message))

        if twitempty == True:
            await self.bot.say("No Twitch streams are set to Alert in this channel.")

    @slist.command(name = "hitbox", pass_context=True)
    async def hitboxlist(self):
        """Lists StreamAlerts turned on for Hitbox"""
        await self.bot.say("Hitbox Streams set up for Alerts:")
        hitempty = 1
        message = ""
        for item in self.hitbox_streams:
            await self.bot.say(item["NAME"])
            hitempty = 0

        if hitempty == True:
            await self.bot.say("No Hitbox streams are set to Alert in this channel.")

    @slist.command(name = "beam", pass_context=True)
    async def beamlist(self):
        """Lists StreamAlerts turned on for Beam"""
        await self.bot.say("Beam Streams set up for Alerts:")
        beamempty = 1
        for item in self.beam_streams:
            await self.bot.say(item["NAME"])
            beamempty = 0

        if beamempty == True:
            await self.bot.say("No Beam streams are set to Alert in this channel.")

def check_folders():
    if not os.path.exists("data/streams"):
        print("Creating data/streams folder...")
        os.makedirs("data/streams")

def check_files():
    f = "data/streams/twitch.json"
    if not fileIO(f, "check"):
        print("Creating empty twitch.json...")
        fileIO(f, "save", [])

    f = "data/streams/hitbox.json"
    if not fileIO(f, "check"):
        print("Creating empty hitbox.json...")
        fileIO(f, "save", [])

    f = "data/streams/beam.json"
    if not fileIO(f, "check"):
        print("Creating empty beam.json...")
        fileIO(f, "save", [])

def setup(bot):
    logger = logging.getLogger('aiohttp.client')
    logger.setLevel(50) #Stops warning spam
    check_folders()
    check_files()
    n = phStreams(bot)
    loop = asyncio.get_event_loop()
    loop.create_task(n.stream_checker())
    bot.add_cog(n)
