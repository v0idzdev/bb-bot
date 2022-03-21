"""
Sends an embedded, custom, help command.
"""

import nextcord

from nextcord.ext import commands
from typing import Optional


class HelpCommand(commands.MinimalHelpCommand):
    """Implementation of a help command with minimal output."""
    def get_command_signature(self, command: commands.Command):
        return f'{self.context.clean_prefix}{command.qualified_name} {command.signature}'

    async def help_embed(
        self, title: str, description: Optional[str]=None, mapping: Optional[dict]=None,
        command_set: Optional[set[commands.Command]]=None
    ):
        """Sends a help embed to the channel the help command was used in."""
        embed = nextcord.Embed(title=title)

        if description: # Only give the embed a description if there is one
            embed.description = description

        avatar = self.context.bot.user.avatar or self.context.bot.user.default_avatar
        embed.set_author(name=self.context.bot.user.name, icon_url=avatar.url)

        if command_set: # Show help about all commands in the set
            filtered = await self.filter_commands(command_set, sort=True)

            for command in filtered:
                embed.add_field(name=self.get_command_signature(command), value=command.short_doc or '...', inline=False)

        if mapping: # Add a short description
            for cog, command_set in mapping.items():
                filtered = await self.filter_commands(command_set, sort=True)

                if not filtered:
                    continue

                name = cog.qualified_name if cog else 'No category'
                command_list = '\u2002'.join(f'{self.context.clean_prefix}{command.name}' for command in filtered)
                value = (f'{cog.description}\n{command_list}' if cog and cog.description else command_list)

                embed.add_field(name=name, value=value, inline=False)

        return embed

    async def send_bot_help(self, mapping: dict):
        """Sends a bot help command."""
        embed = await self.help_embed(
            title='Bot Commands',
            description='BB.Bot commands. See our GitHub repository for more information.'
                + f'\n\nUse **~help <command name>** for more information about a command.'
                + f'\n\nUse **~help <cog name>** for more information about a cog.',
            mapping=mapping
        )

        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command: commands.Command | commands.Group):
        embed = await self.help_embed(
            title=command.qualified_name,
            description=command.help,
            command_set=command.commands if isinstance(command, commands.Group) else None
        )

        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog: commands.Cog):
        embed = await self.help_embed(
            title=cog.qualified_name,
            description=f'{cog.description}\n\nUse **~help <command name>** for more information about a command.',
            command_set=cog.get_commands()
        )

        await self.get_destination().send(embed=embed)

    send_group_help = send_command_help