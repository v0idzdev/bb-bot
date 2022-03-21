"""
Contains a embedded help command.
"""

from nextcord.ext import commands
from .help_command import HelpCommand


class HelpCommandCog(commands.Cog, name='Help'):
    """❓ Shows help information about commands."""
    def __init__(self, client: commands.Bot):
        self._current_help_command = client.help_command

        client.help_command = HelpCommand()
        client.help_command.cog = self

    def cog_unload(self):
        """Called when the cog is removed."""
        self.client.help_command = self._current_help_command


def setup(client: commands.Bot):
    """Registers the cog with the client."""
    client.add_cog(HelpCommandCog(client))


def teardown(client: commands.Bot):
    """Un-registers the cog with the client."""
    client.remove_cog(HelpCommandCog(client))

