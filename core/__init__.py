"""
Module `core` contains the base code used to run a Discord
bot with MongoDB, and a Twitch API client.

This module can be used as a standalone library to serve as
a base for adding your own cogs to.
"""
from .discord_client import DiscordClient
from .discord_client_factory import DiscordClientFactory