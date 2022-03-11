"""
Contains utility functions to assist command modules.
"""

import discord.ext.commands as commands

# |-------- UTILITY FUNCTIONS --------|

def add_commands(*cmds: function, client: commands.Bot):
    """Loops through each command passed in and adds them to a bot.

    :param: *cmds (tuple(function)): The functions to add to the bot.
    :param: client (Bot): Client instance, to add the commands to.
    """
    for cmd in cmds:
        client.add_command(cmd)