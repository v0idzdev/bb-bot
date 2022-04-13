import abc
import discord
import bot

from typing import Awaitable


class BlacklistView(bot.abc.View):
    """
    Class `BlacklistView` defines an abstract class that inherits from ui.abc.View,
    and defines abstract send_modal, submit, and abort methods for common button callbacks.
    """
    @abc.abstractmethod
    async def send_modal(self, interaction: discord.Interaction, button: discord.Button) -> Awaitable:
        """
        Abstract method for a blacklist enter word button callback. This must be decorated
        using the `@discord.ui.button` decorator.
        """
        ...

    @abc.abstractmethod
    async def submit(self, interaction: discord.Interaction, button: discord.Button) -> Awaitable:
        """
        Abstract method for a blacklist submit button callback. This must be decorated
        using the `@discord.ui.button` decorator.
        """
        ...

    @abc.abstractmethod
    async def abort(self, interaction: discord.Interaction, button: discord.Button) -> Awaitable:
        """
        Abstract method for a blacklist abort button callback. This must be decorated
        using the `@discord.ui.button` decorator.
        """
        ...