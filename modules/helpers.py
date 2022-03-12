"""
Contains utility functions to assist command modules.
"""

import discord.ext.commands as commands

# |-------- UTILITY FUNCTIONS --------|

def add_commands(client: commands.Bot, *cmds: tuple[function]):
    """Loops through each command passed in and adds them to a bot.

    :param: *cmds (tuple(function)): The functions to add to the bot.
    :param: client (Bot): Client instance, to add the commands to.
    """
    for cmd in cmds:
        client.add_command(cmd)


def add_listeners(client: commands.Bot, *listeners: tuple[function, str]):
    """Loops through each event listener passed in and adds them to a bot.

    You must pass in the list of listeners as a tuple, consisting of the function's
    name and the name of the event.

    :param: *cmds (tuple(function, str)): The functions to add to the bot.
    :param: client (Bot): Client instance, to add the event listeners to.
    """
    for function, event in listeners:
        client.add_listener(function, name=event)