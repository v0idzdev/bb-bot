"""
Contains a cog that handles reaction roles/self roles.
"""

import nextcord
import start
import json

from nextcord.ext import commands, tasks

FILEPATH = 'files/reactionroles.json' # JSON file containing reaction role data


class RoleCog(commands.Cog):
    """🏷️ Contains role commands."""
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(aliases=['crr'])
    @commands.has_permissions(manage_roles=True)
    async def reactrole(
        self, ctx: commands.Context, emoji, role: nextcord.Role, *, message: str
    ):
        """
        🏷️ Creates a reaction role message.

        Usage:
        ```
        ~reactrole | ~rrr <@role>
        ```
        """
        embed = nextcord.Embed(description=message)
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
    async def removereactrole(self, ctx: commands.Context, role: nextcord.Role):
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

        embed = nextcord.Embed(title=f'🔧 Removed the \'{role.name}\' reaction role.')
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
                    + f'Use **{start.prefix}reactrole `emoji` `@role` `message`**.'

            case commands.MissingRequiredArgument:
                message += 'Please enter all the required arguments.\n' \
                    + f'Use **{start.prefix}reactrole `emoji` `@role` `message`**.'

            case nextcord.HTTPException: # An invalid emoji raises a HTTP exception
                if 'Unknown Emoji' in error.__str__(): # Prevents this handler from catching unrelated errors
                    await ctx.channel.purge(limit=1)
                    message += 'Sorry, that emoji is invalid. Please use a valid emoji.'

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
                    + f'Use **{start.prefix}reactrole `emoji` `@role` `message`**.'

            case commands.MissingRequiredArgument:
                message += 'Please enter all the required arguments.\n' \
                    + f'Use **{start.prefix}removereactrole `@role`**.'

            case _:
                message += 'An unknown error occurred while creating your reaction role.\n' \
                    + f'Please try again later.'

        await ctx.send(message)


# |--------- BACKGROUND TASKS ---------|


class JSONFileCleaner(commands.Cog):
    """
    Clears deleted roles from the reaction roles JSON file.
    """
    def __init__(self, client: commands.Bot):
        self.client = client
        self.clean_json_file.start() # Start the loop

    @tasks.loop(seconds=60)
    async def clean_json_file(self):
        """
        Automatically removes deleted roles from the JSON file containing reaction roles.
        """
        with open(FILEPATH) as file:
            data: list = json.load(file)

        for guild in self.client.guilds:
            for item in list(filter(lambda item: item['guild_id'] == guild.id, data)):
                if item['role_id'] not in [role.id for role in guild.roles]:
                    data.remove(item)

        with open(FILEPATH, 'w') as file:
            json.dump(data, file, indent=4)

    @commands.Cog.listener()
    async def on_message_delete(self, message: nextcord.Message):
        """
        Deletes reaction role messages that correspond to a deleted role. Removes the
        entry for that reaction role in the JSON file.
        """
        with open(FILEPATH) as file:
            data: list = json.load(file)

        for item in data:
            if item['msg_id'] == message.id:
                message.delete()
                data.remove(item)

        with open(FILEPATH, 'w') as file:
            json.dump(data, file, indent=4)



class ReactionEventHandler(commands.Cog):
    """
    Handles raw reaction add and raw reaction remove events.
    """
    def __init__(self, client: nextcord.Client):
        self.client = client

    async def _add_or_remove_role(
        self, payload: nextcord.RawReactionActionEvent, client: commands.Bot, type: str
    ):
        """
        Adds or removes a role from a user.
        """
        guild: nextcord.Guild = client.get_guild(payload.guild_id)
        roles = guild.roles

        match type:

            case 'add':
                member = payload.member
                action = member.add_roles

            case 'remove':
                member: nextcord.Member = guild.get_member(payload.user_id)
                action = member.remove_roles

        if member.bot:
            return

        with open(FILEPATH) as file:
            data = json.load(file)

        for item in data:
            # Check if the reaction emoji and message are the ones used to give a user
            # a specific role, or if the role has been deleted
            if item['emoji'] != payload.emoji.name or item['msg_id'] != payload.message_id \
            or item['role_id'] not in [role.id for role in guild.roles]:
                continue

            # If not, either add/remove the role
            role = nextcord.utils.get(roles, id=item['role_id'])
            await action(role)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: nextcord.RawReactionActionEvent):
        """
        Runs when a reaction is added, regardless of the internal message cache.
        """
        await self._add_or_remove_role(payload, self.client, 'add')

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: nextcord.RawReactionActionEvent):
        """
        Runs when a reaction is added, regardless of the internal message cache.
        """
        await self._add_or_remove_role(payload, self.client, 'remove')


def setup(client: commands.Bot):
    """Registers the cog with the client."""
    client.add_cog(RoleCog(client))


def teardown(client: commands.Bot):
    """Un-registers the cog with the client."""
    client.remove_cog(RoleCog(client))