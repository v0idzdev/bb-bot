"""
Contains a cog that handles reaction roles/self roles.
"""

import discord.ext.commands as commands
import discord.ext.tasks as tasks
import discord
import helpers
import start
import json


# |-------------- CONFIG --------------|


FILEPATH = 'files/reactionroles.json' # JSON file containing reaction role data


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

        For each guild:
            Generate a list of reaction roles that were created for that guild.
            Generate a list of reaction roles in that guild that were deleted.

            For each deleted role:
                Delete the role.
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
    async def on_message_delete(message: discord.Message):
        """
        Deletes reaction role messages that correspond to a deleted role. Removes the
        entry for that reaction role in the JSON file.

        Parameters
        ----------

        message (Message):
            The message that was sent.
        """
        with open(FILEPATH) as file:
            data: list = json.load(file)

        for item in data:
            if item['msg_id'] == message.id:
                message.delete()
                data.remove(item)

        with open(FILEPATH, 'w') as file:
            json.dump(data, file, indent=4)


# |--------- USEFUL FUNCTIONS ---------|


async def add_or_remove_role(
    payload: discord.RawReactionActionEvent, client: commands.Bot, type: str
):
    """
    Adds or removes a role from a user.

    Parameters
    ----------

    payload (RawReactionActionEvent):
        The object containing the raw data about the reaction event.

    client (Bot):
        The bot that is listening to the reaction add or reaction remove event.

    type (str):
        Whether to add or remove a role. Accepted values are: 'add' and 'remove'.
    """
    guild: discord.Guild = client.get_guild(payload.guild_id)
    roles = guild.roles

    match type:

        case 'add':
            member = payload.member
            action = member.add_roles

        case 'remove':
            member: discord.Member = guild.get_member(payload.user_id)
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
        role = discord.utils.get(roles, id=item['role_id'])
        await action(role)


# |--- REACTION ROLES EVENT HANDLER ---|


class ReactionEventHandler(commands.Cog):
    """
    Handles raw reaction add and raw reaction remove events.
    """
    def __init__(self, client: discord.Client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """
        Runs when a reaction is added, regardless of the internal message cache.

        Parameters
        ----------

        payload (RawReactionActionEvent):
            The object containing the raw data about the reaction event.
        """
        await add_or_remove_role(payload, self.client, 'add')

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """
        Runs when a reaction is added, regardless of the internal message cache.

        Parameters
        ----------

        payload (RawReactionActionEvent):
            The object containing the raw data about the reaction event.
        """
        await add_or_remove_role(payload, self.client, 'remove')


# |------------- COMMANDS -------------|


@commands.command(aliases=['crr'])
@commands.has_permissions(manage_roles=True)
async def reactrole(
    ctx: commands.Context, emoji, role: discord.Role, *, message: str
):
    """
    Creates and sends an embed that gives users a role when they react to it.

    Parameters
    ----------

    ctx (Context):
        Command invocation context.

    emoji (Emoji | PartialEmoji):
        The emoji to use that gives the user the role, for the embed the bot will create.

    role (Role):
        The role to add to the user. This role must exist in the server already.

    message (str):
        The message to use for the embed the bot will create.
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
async def removereactrole(ctx: commands.Context, role: discord.Role):
    """
    Removes all messages containing a reaction role from the JSON file.

    Also removes all messages containing the reaction role from the server.

    Parameters
    ----------

    ctx (Context):
        Command invocation context:

    role (Role):
        The role on the server to remove.
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


# |-------------- ERRORS --------------|


@reactrole.error
async def reactrole_error(ctx: commands.Context, error):
    """
    Error handler for the reactrole command.

    Parameters
    ----------

    ctx (Context):
        Command invocation context.

    error:
        The error that was raised when the command was invoked.
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

        case discord.HTTPException: # An invalid emoji raises a HTTP exception
            if 'Unknown Emoji' in error.__str__(): # Prevents this handler from catching unrelated errors
                await ctx.channel.purge(limit=1)
                message += 'Sorry, that emoji is invalid. Please use a valid emoji.'

        case _:
            message += 'An unknown error occurred while creating your reaction role.\n' \
                + f'Please try again later.'

    await ctx.send(message)


@removereactrole.error
async def removeractrole_error(ctx: commands.Context, error):
    """
    Error handler for the removeractrole command.

    Parameters
    ----------

    ctx (Context):
        Command invocation context.

    error:
        The error that was raised when the command was invoked.
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


# |-------- REGISTERING MODULE --------|


def setup(client: commands.Bot):
    """
    Registers the reaction roles cog with the bot.

    Parameters
    ----------

    client (Bot):
        The bot to add the commands to.
    """
    helpers.add_commands(client, reactrole, removereactrole)
    client.add_cog(ReactionEventHandler(client))
    client.add_cog(JSONFileCleaner(client))