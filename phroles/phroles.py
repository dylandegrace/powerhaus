import re
import discord
from .utils import checks
from discord.ext import commands
from __main__ import send_cmd_help


class CustomRoles:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, no_pm=True, name='role')
    async def _role(self, context):
        """DLs can add roles, users can apply or relieve roles. Roles created with this cog have no permissions."""
        if context.invoked_subcommand is None:
            await send_cmd_help(context)

    @_role.command(pass_context=True, no_pm=True, name='add', aliases=['new'])
    async def _add(self, context, color, *role_name):
        """Add a role
        Example: role add ff0000 Red Role"""
        server = context.message.server

        lead_role = "Division Lead"
        lead_check = lambda r: r.name.lower() == lead_role.lower()
        test = checks.role_or_permissions(context, lead_check)
				
        if re.search(r'^(?:[0-9a-fA-F]{3}){1,2}$', color):
            name = ' '.join(role_name)
            color = discord.Color(int(color, 16))
            permissions = discord.Permissions(permissions=0)
            try:
                await self.bot.create_role(server, name=name, color=color, permissions=permissions, hoist=False)
                message = 'New role made'
            except discord.Forbidden:
                message = 'I have no permissions to do that. Please give me role managing permissions.'
        else:
            message = '`Not a valid heximal color`'
        await self.bot.say(message)
        await self.bot.say("context, lead_check  ==" + str(test))

    @_role.command(pass_context=True, no_pm=True, name='remove', aliases=['delete'])
    @checks.mod_or_permissions(manage_roles=True)
    async def _remove(self, context, *role_name):
        """Remove role"""
        server = context.message.server
        name = ' '.join(role_name)
        roles = [role.name.lower() for role in server.roles]
        if name.lower() in roles:
            for role in server.roles:
                if role.name.lower() == name.lower():
                    if role.permissions.value < 1:
                        try:
                            await self.bot.delete_role(server, role)
                            message = 'Role {} removed'.format(role.name)
                            break
                        except discord.Forbidden:
                            message = 'I have no permissions to do that. Please give me role managing permissions.'
                    else:
                        message = 'Not a Custom Roles role'
                else:
                    message = '`No such role on this server`'
        else:
            message = 'There is no such role on this server'
        await self.bot.say(message)

    @_role.command(pass_context=True, no_pm=True, name='apply')
    async def _apply(self, context, *role_name):
        """Apply a role"""
        server = context.message.server
        author = context.message.author
        name = ' '.join(role_name)
        roles = [role.name.lower() for role in server.roles]
        if name.lower() in roles:
            for role in server.roles:
                if role.name.lower() == name.lower():
                    if role.permissions.value < 1:
                        try:
                            await self.bot.add_roles(author, role)
                            message = 'Role `{}` applied to {}'.format(role.name, author.display_name)
                            break
                        except discord.Forbidden:
                            message = 'I have no permissions to do that. Please give me role managing permissions.'
                    else:
                        message = 'You cannot use this role'
                else:
                    message = 'No such role'
        else:
            message = 'There is no such role on this server'
        await self.bot.say(message)

    @_role.command(pass_context=True, no_pm=True, name='relieve')
    async def _relieve(self, context, *role_name):
        """Relieve a role"""
        server = context.message.server
        author = context.message.author
        name = ' '.join(role_name)
        roles = [role.name.lower() for role in server.roles]
        if name.lower() in roles:
            for role in server.roles:
                if role.name.lower() == name.lower():
                    try:
                        await self.bot.remove_roles(author, role)
                        message = 'Role `{}` removed from {}'.format(role.name, author.display_name)
                        break
                    except discord.Forbidden:
                        message = 'I have no permissions to do that. Please give me role managing permissions.'
                else:
                    message = '`Something went wrong...`'
        else:
            message = 'There is no such role on this server'
        await self.bot.say(message)

    @_role.command(pass_context=True, no_pm=True, name='list')
    @checks.mod_or_permissions(manage_roles=True)
    async def _list(self, context):
        """List all available roles"""
        server = context.message.server
		
        message = '\n'
		
        for role in server.roles:
            if role.name = 'Member':
                messagetotal = '\n{} ({})'.format(role.name, len([member for member in server.members if ([r for r in member.roles if r.name == role.name])]))
            if role.permissions.value < 1 and role.name != '@everyone':
                message += '\n{} ({})'.format(role.name, len([member for member in server.members if ([r for r in member.roles if r.name == role.name])]))
		
        embed = discord.Embed(colour=0xdb941a) # Can use discord.Colour() as well
        embed.type = "rich"
        embed.title = "**MEMBER INFORMATION**"
        embed.add_field(name="Total member count (those who typed !accept)", value=messagetotal) # Can add multiple fields.
        embed.add_field(name="People have added the following games:", value=message) # Can add multiple fields.
        await self.bot.say(embed=embed)


def setup(bot):
    n = CustomRoles(bot)
    bot.add_cog(n)