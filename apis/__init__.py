"""
Module `apis` contains classes that are used to interact with
external applications more easily. This includes a Twitch API
wrapper, and a MongoDB document API.

This module is separate from module `source` because `apis` is
not dependent on any functionality from discord.py.
"""
from .mongo import Collection
from .twitch import TwitchClient, TwitchBroadcast