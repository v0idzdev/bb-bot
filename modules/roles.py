"""
Contains a cog that handles reaction roles/self roles.
"""

import discord.ext.commands as commands
import discord
import json


# |-------- REACTION ROLES --------|


@commands.command()
@commands.has_permissions(manage_roles=True)
async def reactrole(ctx: commands.Context, emoji, role: discord.Role, *, message: str):
    """
    Creates and sends an embed that gives users a role when they react to it.
    """
    filepath = 'files/reactionroles.json' # JSON file containing reaction roles

    embed = discord.Embed(description=message)
    msg = await ctx.channel.send(embed=embed)

    await msg.add_reaction(emoji)

    with open(filepath) as file:
        data: list = json.load(file)

        react_role = {
            'name': role.name,
            'role_id': role.id,
            'emoji': emoji,
            'msg_id': msg.id
        }

        data.append(react_role)

    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)


# |---- REGISTERING MODULE ----|


def setup(client: commands.Bot):
    """
    Registers the reaction roles cog with the bot.

    Parameters
    ----------

    client (Bot):
        The bot to add the commands to.
    """