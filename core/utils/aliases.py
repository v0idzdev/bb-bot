"""
Module `aliases` contains typing aliases used throughout
the project.
"""
import motor.motor_asyncio
import collections.abc
import discord

from itertools import cycle
from typing import (
    Union,
    TypeAlias,
)

# MongoDB aliases
MongoClient: TypeAlias = motor.motor_asyncio.AsyncIOMotorClient
MongoDatabase: TypeAlias = motor.motor_asyncio.AsyncIOMotorDatabase
MongoCollection: TypeAlias = motor.motor_asyncio.AsyncIOMotorCollection
JSONCompatible: TypeAlias = collections.abc.Mapping
MongoCollectionID: TypeAlias = Union[int, str]

# Discord.py aliases
MemberOrUser: TypeAlias = Union[discord.Member, discord.User]

