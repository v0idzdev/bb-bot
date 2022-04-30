"""
Module `exceptions` contains music-related errors to
be used in the music extension.
"""
from discord.ext import commands


class VCError(commands.CommandError):
    """
    Exception class for voice channel connection errors.
    """


class InvalidVC(VCError):
    """
    Exception class for invalid voice channel errors.
    """