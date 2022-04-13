"""
Module `ui.abc` contains abstract base classes for UI components that
the bot uses. This stops certain methods from being repeated.

Classes within this module should not be used directly, and must
be inherited from in order to create a new UI component.
"""
from .view import View
from .blacklist_view import BlacklistView