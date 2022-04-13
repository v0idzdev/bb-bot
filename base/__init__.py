"""
Module `base` contains base classes for UI components that
the bot uses. This stops certain methods from being repeated.

Classes within this module should not be used directly, and should
be inherited from in order to create a new UI component. This module
is not named `abc` to avoid conflicts with `abc` imports.
"""
from .view import View
from .blacklist_view import BlacklistView