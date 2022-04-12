"""
Module `decorators` contains wrapper functions to be used on
methods in the `Twitch` class, that assist its functionality.
"""

import asyncio
import functools
from io import BytesIO

from typing import Coroutine, Callable


def session_check(coroutine) -> Coroutine:
    """
    Decorator function for `Twitch` methods that ensures that
    Twitch.require_session has been called before calling the method.
    """
    async def __inner(self, *args, **kwargs) -> Coroutine:
        """
        Internal wrapper function for the `Twitch` method
        decorated by @session_check.
        """
        await self.__require_session()
        return await coroutine(self, *args, **kwargs)

    return __inner


def authorization_check(coroutine) -> Coroutine:
    """
    Decorator function for `Twitch` methods that ensures that
    Twitch.authorize has been called before calling the method.
    """
    async def __inner(self, *args, **kwargs) -> Coroutine:
        """
        Internal wrapper function for the `Twitch` method
        decorated by @authorization_check.
        """
        await self.__authorize()
        return await coroutine(self, *args, **kwargs)

    return __inner


def executor(function) -> Callable:
    """
    Decorator function for `Twitch` methods that ensures that
    the method is called using loop.run_in_executor.
    """
    def __inner(*args, **kwargs) -> Callable:
        """
        Internal wrapper function for the `Twitch` method
        decorated by @executor.
        """
        loop = asyncio.get_event_loop()
        partial = functools.partial(function, *args, **kwargs)

        return loop.run_in_executor(None, partial)

    return __inner

