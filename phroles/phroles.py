import re
import io
import aiohttp
import asyncio

import discord
from .utils import checks
from discord.ext import commands
from random import choice
import itertools
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from .utils.dataIO import dataIO
from cogs.utils.chat_formatting import box
from cogs.utils.chat_formatting import pagify
from __main__ import send_cmd_help

BOTCOMMANDER_ROLE = ["Chief Officer"]

class POWERHAUSRoles:
    def __init__(self, bot):
        self.bot = bot
		
    def grouper(self, n, iterable, fillvalue=None):
        """
        Helper function to split lists
        Example:
        grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
        """
        args = [iter(iterable)] * n
        return ([e for e in t if e != None] for t in itertools.zip_longest(*args))    
		
    @commands.group(pass_context=True, no_pm=True, name='role')
    async def _role(self, context):
        """Shows a list of the teams or games we currently have within the server"""
        if context.invoked_subcommand is None:
            await send_cmd_help(context)

    # @_role.command(pass_context=True, no_pm=True, name='add', aliases=['new'])
    # async def _add(self, context, color, *role_name):
        # """Add a role
        # Example: role add ff0000 Red Role"""
        # server = context.message.server

        # lead_role = "Division Lead"
        # lead_check = lambda r: r.name.lower() == lead_role.lower()
        # test = checks.role_or_permissions(context, lead_check)
				
        # if re.search(r'^(?:[0-9a-fA-F]{3}){1,2}$', color):
            # name = ' '.join(role_name)
            # color = discord.Color(int(color, 16))
            # permissions = discord.Permissions(permissions=0)
            # try:
                # await self.bot.create_role(server, name=name, color=color, permissions=permissions, hoist=False)
                # message = 'New role made'
            # except discord.Forbidden:
                # message = 'I have no permissions to do that. Please give me role managing permissions.'
        # else:
            # message = '`Not a valid heximal color`'
        # await self.bot.say(message)
        # await self.bot.say("context, lead_check  ==" + str(test))

    # @_role.command(pass_context=True, no_pm=True, name='remove', aliases=['delete'])
    # @checks.mod_or_permissions(manage_roles=True)
    # async def _remove(self, context, *role_name):
        # """Remove role"""
        # server = context.message.server
        # name = ' '.join(role_name)
        # roles = [role.name.lower() for role in server.roles]
        # if name.lower() in roles:
            # for role in server.roles:
                # if role.name.lower() == name.lower():
                    # if role.permissions.value < 1:
                        # try:
                            # await self.bot.delete_role(server, role)
                            # message = 'Role {} removed'.format(role.name)
                            # break
                        # except discord.Forbidden:
                            # message = 'I have no permissions to do that. Please give me role managing permissions.'
                    # else:
                        # message = 'Not a Custom Roles role'
                # else:
                    # message = '`No such role on this server`'
        # else:
            # message = 'There is no such role on this server'
        # await self.bot.say(message)

    # @_role.command(pass_context=True, no_pm=True, name='apply')
    # async def _apply(self, context, *role_name):
        # """Apply a role"""
        # server = context.message.server
        # author = context.message.author
        # name = ' '.join(role_name)
        # roles = [role.name.lower() for role in server.roles]
        # if name.lower() in roles:
            # for role in server.roles:
                # if role.name.lower() == name.lower():
                    # if role.permissions.value < 1:
                        # try:
                            # await self.bot.add_roles(author, role)
                            # message = 'Role `{}` applied to {}'.format(role.name, author.display_name)
                            # break
                        # except discord.Forbidden:
                            # message = 'I have no permissions to do that. Please give me role managing permissions.'
                    # else:
                        # message = 'You cannot use this role'
                # else:
                    # message = 'No such role'
        # else:
            # message = 'There is no such role on this server'
        # await self.bot.say(message)

    # @_role.command(pass_context=True, no_pm=True, name='relieve')
    # async def _relieve(self, context, *role_name):
        # """Relieve a role"""
        # server = context.message.server
        # author = context.message.author
        # name = ' '.join(role_name)
        # roles = [role.name.lower() for role in server.roles]
        # if name.lower() in roles:
            # for role in server.roles:
                # if role.name.lower() == name.lower():
                    # try:
                        # await self.bot.remove_roles(author, role)
                        # message = 'Role `{}` removed from {}'.format(role.name, author.display_name)
                        # break
                    # except discord.Forbidden:
                        # message = 'I have no permissions to do that. Please give me role managing permissions.'
                # else:
                    # message = '`Something went wrong...`'
        # else:
            # message = 'There is no such role on this server'
        # await self.bot.say(message)
		
    @_role.command(pass_context=True, no_pm=True, name='chart')
    @checks.mod_or_permissions(manage_roles=True)
    async def _chart(self, context):
    
        server = context.message.server

        facecolor = '#1c202b'
        edgecolor = '#eeeeee'
        spinecolor = '#999999'
        footercolor = '#999999'
        labelcolor = '#eeeeee'
        tickcolor = '#999999'
        titlecolor = '#ffffff'
        linecolor = '#ffc43b'
        
	
        x = [member.joined_at for member in server.members]

        titles = ['New Members Per Week', 'Total Members']
        xaxes = 'x'
        yaxes = ['Frequency','Total Members']
        
               
        plt.switch_backend('Agg')
        
        fig = plt.figure()
        fig.subplots_adjust(top=0.73, hspace=.35)
        fig.suptitle('POWERHAUS Gaming\nMember Chart\n', fontsize=20, color=titlecolor, y=0.95)
        

        
        nbins = math.floor((max(x)-min(x)).days/7)

        (n, bins, patches) = plt.hist(x, bins = nbins, align='left')
        plt.clf
        
        ax1 = plt.subplot(211)
        ax1.set_title(titles[0], fontsize=16, color=titlecolor)
        ax1.set_ylabel(yaxes[0], color=labelcolor)
        ax1.spines['bottom'].set_color(edgecolor)
        ax1.spines['top'].set_color(edgecolor)
        ax1.spines['left'].set_color(edgecolor)
        ax1.spines['right'].set_color(edgecolor)  
        ax1.tick_params(axis='x', colors=spinecolor)
        ax1.tick_params(axis='y', colors=spinecolor)        
             
        
        plt.plot(bins[:-1], n, color=linecolor)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.gcf().autofmt_xdate()
        ax1.tick_params(labelbottom='off')   
        ax1.grid(True, alpha = 0.5)
        
        
        total = np.cumsum(n)
        
        
        ax2 = plt.subplot(212)
        ax2.set_title(titles[1], fontsize=16, color=titlecolor)
        ax2.set_ylabel(yaxes[1], color=labelcolor)
        
        
        
        plt.plot(bins[:-1], total, color=linecolor)
        ax2.grid(True, alpha = 0.5)
        
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.gcf().autofmt_xdate()
        ax2.spines['bottom'].set_color(edgecolor)
        ax2.spines['top'].set_color(edgecolor)
        ax2.spines['left'].set_color(edgecolor)
        ax2.spines['right'].set_color(edgecolor)
        ax2.tick_params(axis='x', colors=spinecolor)
        ax2.tick_params(axis='y', colors=spinecolor)

        plot_filename = 'plot.png'
        plot_name = ""
        
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

        plt.clf()
        plt.cla()
        
        import csv
        data_file_name = 'raw_data.csv'
        
        # with open(data_file_name, 'w') as f:
            # writer = csv.writer(f, delimiter='\t')
            # writer.writerows(zip(bins[:-1], total))
            
        with io.BytesIO() as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(zip(bins[:-1], total))
            f.seek(0)
            await context.bot.send_file(
                context.message.channel,
                f,
                filename=data_file_name,
                content=plot_name)


    @_role.command(pass_context=True, no_pm=True, name='games')
    @checks.mod_or_permissions(manage_roles=True)
    async def _games(self, context):
        """List all available games and their member count"""
        server = context.message.server
		
        message = '\n'
		
        for role in server.roles:
            if role.name == 'Member':
                messagetotal = '\n{} ({})'.format(role.name, len([member for member in server.members if ([r for r in member.roles if r.name == role.name])]))
            if role.permissions.value < 1 and role.name not in ['@everyone', 'Streaming'] and not role.name.startswith( 'Team' ):
                message += '\n{} ({})'.format(role.name, len([member for member in server.members if ([r for r in member.roles if r.name == role.name])]))
		
        embed = discord.Embed(colour=0xdb941a) # Can use discord.Colour() as well
        embed.type = "rich"
        embed.title = "**MEMBER INFORMATION**"
        embed.add_field(name="Total member count (those who typed !accept)", value=messagetotal) # Can add multiple fields.
        embed.add_field(name="People have added the following games:", value=message) # Can add multiple fields.
        await self.bot.say(embed=embed)
		
    @_role.command(pass_context=True, no_pm=True, name='teams')
    @checks.mod_or_permissions(manage_roles=True)
    async def _teams(self, context):
        """List all current team roles and their member count"""
        server = context.message.server
		
        message = '\n'
		
        for role in server.roles:
            if role.name == 'Member':
                messagetotal = '\n{} ({})'.format(role.name, len([member for member in server.members if ([r for r in member.roles if r.name == role.name])]))
            if role.permissions.value < 1 and role.name.startswith( 'Team' ):
                message += '\n{} ({})'.format(role.name, len([member for member in server.members if ([r for r in member.roles if r.name == role.name])]))
		
        embed = discord.Embed(colour=0xdb941a) # Can use discord.Colour() as well
        embed.type = "rich"
        embed.title = "**TEAM INFORMATION**"
        embed.add_field(name="All available team roles are as follows:", value=message) # Can add multiple fields.
        await self.bot.say(embed=embed)

    @commands.group(pass_context=True, no_pm=True, name='team')
    async def _team(self, context):
        """DLs and Team Managers can add teams and apply/relieve teams to/from users."""
        if context.invoked_subcommand is None:
            await send_cmd_help(context)
			
    @_team.command(pass_context=True, no_pm=True, name='add', aliases=['new'])
    async def _add(self, context, *, role_name):
        """Add a team
        Example: !team add Team OW-Black"""
        server = context.message.server

        lead_role = "Division Lead".lower()
        manager_role = "Team Manager".lower()

        # lead_check = checks.role_or_permissions(context, lambda r: r.name.lower() == lead_role.lower())
        # manager_check = checks.role_or_permissions(context, lambda r: r.name.lower() == manager_role.lower())
		
        all_check = checks.role_or_permissions(context, lambda r: r.name.lower() in ("Division Lead".lower(),"Team Manager".lower()), manage_roles=True)
        
        if all_check:

            name = role_name
            color = discord.Color.default()
            permissions = discord.Permissions(permissions=0)
			
            pattern = re.compile('^Team\b')
            m = pattern.match(role_name)
		    
            if re.match(r'^Team\b', role_name):
                try:
                    await self.bot.create_role(server, name=name, color=color, permissions=permissions, hoist=False)
                    message = 'New team role made'
                    await self.bot.say(re.match(r'^Team\b', role_name))
                except discord.Forbidden:
                    message = 'I have no permissions to do that. Please give me role managing permissions.'
            else:
                message = 'You must begin the role name with *Team*. Note that this is *case-sensitive*.\ne.g.: `!team add Team OW-Black`'

        else:
            message = "You don't have proper permissions"

        await self.bot.say(message)
    
    # @_team.command(pass_context=True, no_pm=True, name='apply')
    # async def _apply(self, context, role_name, user):
        # """Adds a role to a user
        # Role name must be in quotes if there are spaces."""
        # author = context.message.author
        # channel = context.message.channel
        # server = context.message.server

        # role = self._role_from_string(server, role_name)

        # if role is None:
            # await self.bot.say('That role cannot be found.')
            # return

        # if not channel.permissions_for(server.me).manage_roles:
            # await self.bot.say('I don\'t have manage_roles.')
            # return

        # await self.bot.add_roles(user, role)
        # await self.bot.say('Added role {} to {}'.format(role.name, user.name))

    # @_team.command(pass_context=True, no_pm=True, name='relieve')
    # async def _relieve(self, context, *role_name):
        # """Remove a user from a specified team"""
        # server = context.message.server
        # author = context.message.author
        # name = ' '.join(role_name)
        # roles = [role.name.lower() for role in server.roles]
        # if name.lower() in roles:
            # for role in server.roles:
                # if role.name.lower() == name.lower():
                    # try:
                        # await self.bot.remove_roles(author, role)
                        # message = 'Role `{}` removed from {}'.format(role.name, author.display_name)
                        # break
                    # except discord.Forbidden:
                        # message = 'I have no permissions to do that. Please give me role managing permissions.'
                # else:
                    # message = '`Something went wrong...`'
        # else:
            # message = 'There is no such role on this server'
        # await self.bot.say(message)

    @commands.command(pass_context=True)
    @commands.has_any_role(*BOTCOMMANDER_ROLE)
    async def mm(self, ctx, *args):
        """
        Member management command.
        Get a list of users that satisfy a list of roles supplied.
        e.g.
        !mm S M -L
        !mm +S +M -L
        fetches a list of users who has the roles S, M but not the role L.
        S is the same as +S. + is an optional prefix for includes.
        Optional arguments
        --output-mentions
            Append a string of user mentions for users displayed.
        --output-id
            Append a string ot user ids for the results.
        --output-mentions-only
            Don’t display the long list and only display the list of member mentions
        --list
            Display as inline list
        --only-role
            Check member has one and exactly one role
        --everyone
            Include everyone
        """

        # Extract optional arguments if exist
        option_output_mentions = "--output-mentions" in args
        option_output_id = "--output-id" in args
        option_output_mentions_only = "--output-mentions-only" in args
        option_sort_join = "--sort-join" in args
        option_everyone = "--everyone" in args
        option_sort_alpha = "--sort-alpha" in args
        option_csv = "--csv" in args
        option_list = "--list" in args
        option_only_role = "--only-role" in args

        server = ctx.message.server
        server_roles_names = [r.name.lower() for r in server.roles]

        # get list of arguments which are valid server role names
        # as dictionary {flag, name}
        out = ["**Member Management**"]

        role_args = []
        flags = ['+', '-']
        if args is not None:
            for arg in args:
                has_flag = arg[0] in flags
                flag = arg[0] if has_flag else '+'
                name = arg[1:] if has_flag else arg

                if name.lower() in server_roles_names:
                    role_args.append({'flag': flag, 'name': name.lower()})

        plus  = set([r['name'] for r in role_args if r['flag'] == '+'])
        minus = set([r['name'] for r in role_args if r['flag'] == '-'])

        # Used for output only, so it won’t mention everyone in chat
        plus_out = plus.copy()

        if option_everyone:
            plus.add('@everyone')
            plus_out.add('everyone')

        help_str = (
            'Syntax Error: You must include at '
            'least one role to display results.')

        if len(plus) < 1:
            out.append(help_str)
        else:
            out.append("Listing members who have these roles: {}".format(
                ', '.join(plus_out)))
        if len(minus):
            out.append("but not these roles: {}".format(
                ', '.join(minus)))

        await self.bot.say('\n'.join(out))

        # only output if argument is supplied
        if len(plus):
            # include roles with '+' flag
            # exclude roles with '-' flag
            out_members = set()
            for m in server.members:
                roles = set([r.name.lower() for r in m.roles])
                if option_everyone:
                    roles.add('@everyone')
                exclude = len(roles & minus)
                if not exclude and roles >= plus:
                    out_members.add(m)

            # only role
            if option_only_role:
                out_members = [m for m in out_members if len(m.roles) == 2]

            suffix = 's' if len(out_members) > 1 else ''
            await self.bot.say("**Found {} member{}.**".format(
                len(out_members), suffix))

            # sort join
            out_members = list(out_members)
            out_members.sort(key=lambda x: x.joined_at)

            # sort alpha
            if option_sort_alpha:
                out_members = list(out_members)
                out_members.sort(key=lambda x: x.display_name)

            # embed output
            if not option_output_mentions_only:
                if option_csv:
                    for page in pagify(
                            self.get_member_csv(out_members), shorten_by=50):
                        await self.bot.say(page)
                elif option_list:
                    for page in pagify(
                            self.get_member_list(out_members), shorten_by=50):
                        await self.bot.say(page)
                else:
                    for data in self.get_member_embeds(ctx, out_members):
                        try:
                            await self.bot.say(embed=data)
                        except discord.HTTPException:
                            await self.bot.say(
                                "I need the `Embed links` permission "
                                "to send this")

            # Display a copy-and-pastable list
            if option_output_mentions | option_output_mentions_only:
                mention_list = [m.mention for m in out_members]
                await self.bot.say(
                    "Copy and paste these in message to mention users listed:")

                out = ' '.join(mention_list)
                for page in pagify(out, shorten_by=24):
                    await self.bot.say(box(page))

            # Display a copy-and-pastable list of ids
            if option_output_id:
                id_list = [m.id for m in out_members]
                await self.bot.say(
                    "Copy and paste these in message to mention users listed:")
                out = ' '.join(id_list)
                for page in pagify(out, shorten_by=24):
                    await self.bot.say(box(page))

    def get_member_csv(self, members):
        """Return members as a list."""
        names = [m.display_name for m in members]
        return ', '.join(names)

    def get_member_list(self, members):
        """Return members as a list."""
        out = []
        for m in members:
            out.append('+ {}'.format(m.display_name))
        return '\n'.join(out)

    def get_member_embeds(self, ctx, members):
        """Discord embed of data display."""
        color = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        color = int(color, 16)
        embeds = []

        # split embed output to multiples of 25
        # because embed only supports 25 max fields
        out_members_group = self.grouper(25, members)

        for out_members_list in out_members_group:
            data = discord.Embed(
                color=discord.Colour(value=color))
            for m in out_members_list:
                value = []
                roles = [r.name for r in m.roles if r.name != "@everyone"]
                value.append(', '.join(roles))

                name = m.display_name
                since_joined = (ctx.message.timestamp - m.joined_at).days

                data.add_field(
                    name=str(name),
                    value=str(
                        ''.join(value) +
                        '\n{} days ago'.format(
                            since_joined)))
            embeds.append(data)
        return embeds

    @commands.command(pass_context=True, no_pm=True)
    async def listroles(self, ctx, *roles):
        """List all the roles on the server."""
        server = ctx.message.server
        if server is None:
            return
        out = []
        out.append("__List of roles on {}__".format(server.name))
        roles_to_list = []
        if len(roles):
            roles_to_list = [
                r for r in server.roles if r.name.lower()
                in [r2.lower() for r2 in roles]]
        else:
            roles_to_list = server.roles

        out_roles = {}
        for role in roles_to_list:
            out_roles[role.id] = {'role': role, 'count': 0}
        for member in server.members:
            for role in member.roles:
                if role in roles_to_list:
                    out_roles[role.id]['count'] += 1
        for role in server.role_hierarchy:
            if role in roles_to_list:
                out.append(
                    "**{}** ({} members)".format(
                        role.name, out_roles[role.id]['count']))
        for page in pagify("\n".join(out), shorten_by=12):
            await self.bot.say(page)

    @commands.command(pass_context=True, no_pm=True)
    @commands.has_any_role(*BOTCOMMANDER_ROLE)
    async def searchmember(self, ctx, name=None):
        """Search member on server by name."""
        if name is None:
            await send_cmd_help(ctx)
            return

        server = ctx.message.server
        results = []
        for member in server.members:
            for member_name in [member.display_name, member.name]:
                if name.lower() in member_name.lower():
                    results.append(member)
                    break

        if not len(results):
            await self.bot.say("Cannot find any users with that name.")
            return

        await self.bot.say('Found {} members.'.format(len(results)))

        for member in results:
            out = [
                '---------------------',
                '**Display name:** {}'.format(member.display_name),
                '**Username:** {}'.format(str(member)),
                '**Join Date:** {} ({} days)'.format(member.joined_at.strftime("%b-%d-%Y"),(ctx.message.timestamp - member.joined_at).days),
                '**Roles:** {}'.format(', '.join([r.name for r in member.roles if not r.is_everyone])),
                '**id:** {}'.format(member.id)
            ]
            await self.bot.say('\n'.join(out))		

def setup(bot):
    n = POWERHAUSRoles(bot)
    bot.add_cog(n)