import asyncio
import functools


def executor(func):
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        partial = functools.partial(func, *args, **kwargs)
        return loop.run_in_executor(None, partial)

    return wrapper