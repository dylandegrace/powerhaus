import discord
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.dataIO import dataIO
from .utils.dataIO import fileIO
from cogs.utils.chat_formatting import box, pagify
from cogs.utils.chat_formatting import *
from copy import deepcopy
import asyncio
import logging
import os
import time




log = logging.getLogger("red.games")


class Games:

    def __init__(self, bot):
        self.bot = bot
        self._settings = dataIO.load_json('data/games/settings.json')
        self._settable_roles = self._settings.get("ROLES", {})
        self.twitch_streams = fileIO("data/streams/twitch.json", "load")
        self.hitbox_streams = fileIO("data/streams/hitbox.json", "load")
        self.beam_streams = fileIO("data/streams/beam.json", "load")

    def _get_addgame_names(self, server):
        if server.id not in self._settable_roles:
            return None
        else:
            return self._settable_roles[server.id]

    def _role_from_string(self, server, rolename, roles=None):
        if roles is None:
            roles = server.roles

        roles = [r for r in roles if r is not None]
        role = discord.utils.find(lambda r: r.name.lower() == rolename.lower(),
                                  roles)
        try:
            log.debug("Role {} found from rolename {}".format(
                role.name, rolename))
        except:
            log.debug("Role not found for rolename {}".format(rolename))
        return role

    def _save_settings(self):
        dataIO.save_json('data/games/settings.json', self._settings)

    def _set_addgames(self, server, rolelist):
        self._settable_roles[server.id] = rolelist
        self._settings["ROLES"] = self._settable_roles
        self._save_settings()

   
    @commands.group(pass_context=True, no_pm=True)
    async def gameset(self, ctx):
        """Manage game settings"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @gameset.command(pass_context=True, name="addgames")
    @checks.admin_or_permissions(manage_roles=True)
    async def gameset_addgames(self, ctx, *, rolelist=None):
        """Set which games users can add to their account.

        COMMA SEPARATED LIST (e.g. csgo, rainbow 6, diablo 3)"""
        server = ctx.message.server
        if rolelist is None:
            await self.bot.say("addgame list cleared.")
            self._set_addgames(server, [])
            return
        unparsed_roles = list(map(lambda r: r.strip(), rolelist.split(',')))
        parsed_roles = list(map(lambda r: self._role_from_string(server, r),
                                unparsed_roles))
        if len(unparsed_roles) != len(parsed_roles):
            not_found = set(unparsed_roles) - {r.name for r in parsed_roles}
            await self.bot.say(
                "These roles were not found: {}\n\nPlease"
                " try again.".format(not_found))
        parsed_role_set = list({r.name for r in parsed_roles})
        self._set_addgames(server, parsed_role_set)
        await self.bot.say(
            "Self roles successfully set to: {}".format(parsed_role_set))
			
    @commands.command(no_pm=True, pass_context=True)
    async def accept(self, ctx):
        author = ctx.message.author
        channel = ctx.message.channel
        server = author.server
        acceptmsg = ctx.message
        recruit = [x for x in author.roles if x.name == "Recruit"]
        memberRole = discord.utils.get(ctx.message.server.roles, name="Member")
        recruitRole = discord.utils.get(ctx.message.server.roles, name="Recruit")
        if (recruit and recruit[0].name == "Recruit"):
            await self.bot.add_roles(author, memberRole)
            await asyncio.sleep(0.5)
            await self.bot.remove_roles(author, recruitRole)
			
            await self.bot.whisper("Thank you for accepting the rules.")
        else:
                await self.bot.whisper("You already accepted the rules!")
        await self.bot.delete_message(acceptmsg)
		
    @commands.group(no_pm=True, pass_context=True, invoke_without_command=True)
    async def addgame(self, ctx, *, rolename):
        """Whoa there partner, you forgot to add a game at the end of the command.
        Review the list with !games and append them (individually) to your !addgame command

        For Admins: you can add additional games using !gameset"""
        server = ctx.message.server
        author = ctx.message.author
        role_names = self._get_addgame_names(server)
        if role_names is None:
            await self.bot.say("I have no user settable game roles for this"
                               " server.")
            return

        member_role = "Member"
        member_check = lambda r: r.name.lower() == member_role.lower()
        member_check = checks.role_or_permissions(ctx, member_check)
		
		
        if member_check is False:
            await self.bot.whisper("You must first be a **Member** to use this command. Make sure you've accepted the rules in the #welcome channel. If you have questions, PM a Chief Officer or Admin.")
            return

        f = self._role_from_string
        roles = [f(server, r) for r in role_names if r is not None]

        role_to_add = self._role_from_string(server, rolename, roles=roles)

        if role_to_add in author.roles:
            await self.bot.say("Woah there buckaroo. You already added that game <:redpants:290215309443465216>. Check your channels on the left and they'll be there.")    
            return
		
        try:
            await self.bot.add_roles(author, role_to_add)
        except discord.errors.Forbidden:
            log.debug("{} just tried to add a game but I was forbidden".format(author.name))
            await self.bot.say("I don't have permissions to do that.")
        except AttributeError:  # role_to_add is NoneType
            log.debug("{} not found as settable on {}".format(rolename,server.id))
            await self.bot.say("That game isn't one that is supported. Please see `!games` for the full list.")
        else:
            log.debug("Role {} added to {} on {}".format(rolename, author.name,server.id))
            gameSuccess = "Game **{}** successfully added. You now have access to new channels.".format(rolename)											 
            await self.bot.say(gameSuccess)
            """await self.bot.whisper('hey it worked')"""

    @addgame.command(no_pm=True, pass_context=True, name="remove")
    async def addgame_remove(self, ctx, *, rolename):
        """Allows users to remove their own roles

        Configurable using `gameset`"""
        server = ctx.message.server
        author = ctx.message.author
        role_names = self._get_addgame_names(server)
        if role_names is None:
            await self.bot.say("I have no user settable roles for this"
                               " server.")
            return

        f = self._role_from_string
        roles = [f(server, r) for r in role_names if r is not None]

        role_to_remove = self._role_from_string(server, rolename, roles=roles)

        try:
            await self.bot.remove_roles(author, role_to_remove)
        except discord.errors.Forbidden:
            log.debug("{} just tried to remove a role but I was"
                      " forbidden".format(author.name))
            await self.bot.say("I don't have permissions to do that.")
        except AttributeError:  # role_to_remove is NoneType
            log.debug("{} not found as removeable on {}".format(rolename,
                                                                server.id))
            await self.bot.say("That role isn't user removeable.")
        else:
            log.debug("Role {} removed from {} on {}".format(rolename,
                                                             author.name,
                                                             server.id))
            gameRemoveSuccess = "Game **{}** successfully removed. You have lost access to those channels.".format(rolename)
            await self.bot.say(gameRemoveSuccess)
			
    @commands.command(no_pm=True, pass_context=True)
    async def games(self, ctx):
        
        server = ctx.message.server
		
        role_names = str(sorted(self._get_addgame_names(server)))
		
        member_role = "Member"
        member_check = lambda r: r.name.lower() == member_role.lower()
        member_check = checks.role_or_permissions(ctx, member_check)
		
		
        if member_check is False:
            await self.bot.whisper("You must first be a **Member** to use this command. Make sure you've accepted the rules in the #welcome channel. If you have questions, PM a Chief Officer or Admin.")
            return

        for ch in ['[',']',"'"]:
            if ch in role_names:
                role_names = role_names.replace(ch,"")
		
        for ch in [", "]:
            if ch in role_names:
                role_names = role_names.replace(ch, "\n")
        
        field_value = ("```\n"+role_names+"``` \nTo gain access to a game's channel please type `!addgame` followed by the game name. "
        "To remove yourself type `!removegame` followed by the game name.")
		
        embed = discord.Embed(colour=0xdb941a) # Can use discord.Colour() as well
        embed.type = "rich"
        embed.title = "**GAMES LIST**"
        embed.add_field(name="We support the following games in our Discord server with private channels:\n", value=field_value) # Can add multiple fields.
        embed.add_field(name="Example:", value="To add **Overwatch** type, `!addgame overwatch`.\n\nView our game pages on [our website](https://www.powerhaus.gg/games)")
        await self.bot.say(embed=embed)
      
    @commands.group(name = "slist", pass_context=True)  
    async def slist(self, ctx):
        """List function to display streams that are enabled with Stream Alerts"""
        self.twitch_streams = fileIO("data/streams/twitch.json", "load")
        self.hitbox_streams = fileIO("data/streams/hitbox.json", "load")
        self.beam_streams = fileIO("data/streams/beam.json", "load")
        pass

    @slist.command(name = "twitch", pass_context=True)
    async def twitchlist(self):
        """Lists StreamAlerts turned on for Twitch"""
        await self.bot.say("Twitch Streams set up for Alerts:")
        twitempty = 1
        message = ""
        for item in self.twitch_streams:
            message += str(item["NAME"] +"\nChannel(s): " + "".join(item["CHANNELS"]) + "\n\n")
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


def check_files():
    if not os.path.exists('data/games/settings.json'):
        try:
            os.mkdir('data/games')
        except FileExistsError:
            pass
        else:
            dataIO.save_json('data/games/settings.json', {})


def setup(bot):
    check_files()
    n = Games(bot)
    bot.add_cog(n)