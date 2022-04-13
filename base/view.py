"""
Module `utils.views.abc.view` contains the view class, which is inherited by
view subclasses that BB.Bot uses.
"""
import discord

from typing import Union


class View(discord.ui.View):
    """
    Class `View` is a subclass of `discord.ui.View` that implements methods
    to disable all buttons, and to prevent any users who were not the original
    command invoker from interacting with the view.

    This class also requires that the original command user is passed in, so
    that interaction_check can be implemented.
    """
    def __init__(self, command_author: Union[discord.User, discord.Member], *args, **kwargs) -> None:
        """
        Creates a `utils.views.abc.View` object that is a subclass of `discord.ui.View`.
        This class overrides discord.ui.View by implementing interaction_check differently,
        and implementing a disable_all_buttons method.

        Params:
         - command_author (discord.User): The user who invoked the command.
         - *args (tuple): Any positional arguments that are to be passed into super().__init__.
         - **kwargs (tuple): Any keyword arguments that are to be passed into super().__init__.

        Returns:
         - A `utils.views.abc.View` instance.
        """
        super().__init__(*args, **kwargs)

        self.message = None
        self._command_author = command_author

    @property
    def command_author(self) -> Union[discord.User, discord.Member]:
        """
        The original author of the command that this view was initialized in. This
        attribute is read-only and cannot be changed.
        """
        return self._command_author

    async def on_timeout(self) -> None:
        """
        This method is called when the view times out. By default, this will call
        `utils.views.abc.View.disable_all_buttons`.
        """
        await self.disable_all_buttons()

    async def disable_all_buttons(self, interaction: discord.Interaction) -> None:
        """
        This method disables all buttons in a `discord.ui.View` instance. This
        is used to disable input when the view has stopped being used.

        Params:
         - interaction (discord.Interaction): Slash command invocation context.
        """
        interaction = interaction or self

        for child in self.children:
            child.disabled = True

        await interaction.message.edit(view=self)
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """
        This method prevents users who weren't the original command user from
        interacting with the view.

        Params:
         - interaction (discord.Interaction): Slash command invocation context.
        """
        if interaction.user.id == self._command_author.id:
            return True

        await interaction.response.send_message("❌ This isn't your interaction!", ephemeral=True)
        return False