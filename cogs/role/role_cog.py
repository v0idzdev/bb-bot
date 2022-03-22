"""
Contains a cog that handles reaction roles/self roles.
"""

import discord

import json

from discord.ext import commands, tasks

FILEPATH = 'files/reactionroles.json' # JSON file containing reaction role data


class RoleCog(commands.Cog, name='Roles'):
    """🏷️ Contains role commands."""
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(aliases=['crr'])
    @commands.has_permissions(manage_roles=True)
    async def reactrole(
        self, ctx: commands.Context, emoji, role: discord.Role, *, message: str
    ):
        """
        🏷️ Creates a reaction role message.

        Usage:
        ```
        ~reactrole | ~rrr <@role>
        ```
        """
        embed = discord.Embed(description=message)
        msg = await ctx.channel.send(embed=embed)
        await msg.add_reaction(emoji)

        with open(FILEPATH) as file:
            data: list = json.load(file) # Contains a dictionary for each reaction role

            react_role = { # Create a dictionary to store in the JSON file
                'guild_id': ctx.guild.id,
                'name': role.name,
                'role_id': role.id,
                'emoji': emoji,
                'msg_id': msg.id
            }

            data.append(react_role)

        with open(FILEPATH, 'w') as file:
            json.dump(data, file, indent=4)

    @commands.command(aliases=['rrr'])
    @commands.has_permissions(manage_roles=True)
    async def removereactrole(self, ctx: commands.Context, role: discord.Role):
        """
        🏷️ Removes a reaction role message.

        Usage:
        ```
        ~removereactrole | ~rrr <@role>
        ```
        """

        with open(FILEPATH) as file:
            data: list = json.load(file) # Contains a dictionary for each reaction role

        instances = [item for item in data if item['role_id'] == role.id]

        if len(instances) == 0:
            raise commands.RoleNotFound(role.__str__())

        for instance in instances:
            msg = await ctx.fetch_message(instance['msg_id'])
            await msg.delete()
            data.remove(instance)

        with open(FILEPATH, 'w') as file:
            json.dump(data, file, indent=4)

        embed = discord.Embed(title=f'🔧 Removed the \'{role.name}\' reaction role.')
        await ctx.send(embed=embed)

    @reactrole.error
    async def reactrole_error(self, ctx: commands.Context, error):
        """
        Error handler for the reactrole command.
        """
        error = getattr(error, 'original', error)
        message = f':x: {ctx.author.mention}: '

        match error.__class__:

            case commands.RoleNotFound:
                message += 'That role does not exist. Please create the role first.'

            case commands.EmojiNotFound:
                message += 'Sorry, that emoji was not found. Please try again.'

            case commands.UserInputError:
                message += 'Invalid input, please try again.\n' \
                    + f'Use **{ctx.prefix}reactrole `emoji` `@role` `message`**.'

            case commands.MissingRequiredArgument:
                message += 'Please enter all the required arguments.\n' \
                    + f'Use **{ctx.prefix}reactrole `emoji` `@role` `message`**.'

            case discord.HTTPException: # An invalid emoji raises a HTTP exception
                if 'Unknown Emoji' in error.__str__(): # Prevents this handler from catching unrelated errors
                    await ctx.channel.purge(limit=1)
                    message += 'Sorry, that emoji is invalid. Please use a valid emoji.'

            case discord.Forbidden:
                message += 'BB.Bot is forbidden from assigning/removing this role.\n' \
                    + f'Try moving this role above the reaction role.'

            case _:
                message += 'An unknown error occurred while creating your reaction role.\n' \
                    + f'Please try again later.'

        await ctx.send(message)

    @removereactrole.error
    async def removeractrole_error(self, ctx: commands.Context, error):
        """
        Error handler for the removeractrole command.
        """
        error = getattr(error, 'original', error)
        message = f':x: {ctx.author.mention}: '

        match error.__class__:

            case commands.RoleNotFound:
                role = error.__str__().removeprefix('Role "').removesuffix('" not found.') # Role "Test" not found, => Test
                message += f'**{role}** either doesn\'t exist, or isn\'t a reaction role on this server.'

            case commands.UserInputError:
                message += 'Invalid input, please try again.\n' \
                    + f'Use **{ctx.prefix}reactrole `emoji` `@role` `message`**.'

            case commands.MissingRequiredArgument:
                message += 'Please enter all the required arguments.\n' \
                    + f'Use **{ctx.prefix}removereactrole `@role`**.'

            case _:
                message += 'An unknown error occurred while creating your reaction role.\n' \
                    + f'Please try again later.'

        await ctx.send(message)


async def setup(client: commands.Bot):
    """Registers the cog with the client."""
    await client.add_cog(RoleCog(client))


async def teardown(client: commands.Bot):
    """Un-registers the cog with the client."""
    await client.remove_cog(RoleCog(client))