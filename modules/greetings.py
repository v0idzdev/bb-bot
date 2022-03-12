import discord.ext.commands as commands
import discord
import helpers

# |----- USEFUL FUNCTIONS -----|

async def send_message(member: discord.Member, message: str):
    """Sends a welcome or goodbye message when a member joins/leaves a server.

    :param: member (Member): The member that joined or left the server
    :param: message (str): Either 'Welcome' or 'Goodbye' depending on whether the user
        joined or left the server.
    """
    channel = member.guild.system_channel

    if channel is not None:
        await channel.send(f':wave: {message}, {member.mention}!')

# |---------- EVENTS ----------|

async def on_member_join(member: discord.Member):
    """Sends a welcome message when a member joins a server.

    :param: member (Member): The member that joined the server.
    """
    await send_message(member, 'Welcome')


async def on_member_remove(member: discord.Member):
    """Sends a welcome message when a member leaves a server.

    :param: member (Member): The member that left the server.
    """
    await send_message(member, 'Goodbye')

# |---- REGISTERING MODULE ----|

def setup(client: commands.Bot):
    """Registers the functions in this module with the client.

    :param: client (Bot): Client instance, to add the commands to.
    """
    helpers.add_listeners(
        client,
        (on_member_join, on_member_join.__name__),
        (on_member_remove, on_member_remove.__name__)
    )