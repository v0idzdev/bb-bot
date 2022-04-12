"""
Module `__main__` is the main entry point of the application.
This is where the Discord Client is created, setup and run.
"""

__author__ = "Matthew Flegg"
__version__ = "v2.0.0-alpha.1"

import asyncio
import itertools
import json
import os
import discord
import dotenv

from discord.ext import commands
from source import Client

dotenv.load_dotenv(".env")