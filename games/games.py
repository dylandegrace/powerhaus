import discord
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.dataIO import dataIO
from .utils.dataIO import fileIO
from cogs.utils.chat_formatting import box, pagify
from copy import deepcopy
import asyncio
import logging
import os


log = logging.getLogger("red.games")


class Games:

    def __init__(self, bot):
        self.bot = bot
        self._settings = dataIO.load_json('data/games/settings.json')
        self._settable_roles = self._settings.get("ROLES", {})

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

    @commands.group(no_pm=True, pass_context=True, invoke_without_command=True)
    async def addgame(self, ctx, *, rolename):
        """Allows users to set their own role.

        Configurable using `gameset`"""
        server = ctx.message.server
        author = ctx.message.author
        role_names = self._get_addgame_names(server)
        if role_names is None:
            await self.bot.say("I have no user settable game roles for this"
                               " server.")
            return

        f = self._role_from_string
        roles = [f(server, r) for r in role_names if r is not None]

        role_to_add = self._role_from_string(server, rolename, roles=roles)

        try:
            await self.bot.add_roles(author, role_to_add)
        except discord.errors.Forbidden:
            log.debug("{} just tried to add a game but I was forbidden".format(
                author.name))
            await self.bot.say("I don't have permissions to do that.")
        except AttributeError:  # role_to_add is NoneType
            log.debug("{} not found as settable on {}".format(rolename,
                                                              server.id))
            await self.bot.say("That game isn't one that is supported. Please see `!games` for the full list.")
        else:
            log.debug("Role {} added to {} on {}".format(rolename, author.name,
                                                         server.id))
            gameSuccess = "Game **{}** successfully added. You now have access to new channels.".format(rolename)											 
            await self.bot.say(gameSuccess)

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
    async def embedtest(self, ctx):
        
        server = ctx.message.server
		
        author_name = ctx.message.author
        description = ("Short little description with a link to google "
                   "(https://www.google.com")
        footer_text = "i am tiny text";
		
        role_names = str(self._get_addgame_names(server))

        for ch in ['[',']',"'"]:
            if ch in role_names:
                role_names = role_names.replace(ch,"")
		
        for ch in [", "]:
            if ch in role_names:
                role_names = role_names.replace(ch, "\n")

        embed = discord.Embed(colour=0xdb941a, description=description) # Can use discord.Colour() as well
        embed.title = "i am the title"
        embed.set_author(name="test", icon_url="https://www.powerhaus.gg/wp-content/uploads/2017/01/overwatchgame.png")
        embed.add_field(name="We support the following games in our Discord server with private channels:\n", value=[``` role_names ```]) # Can add multiple fields.
        embed.set_footer(text=footer_text)
        await self.bot.say(embed=embed)		


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