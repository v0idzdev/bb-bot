import asyncio
import datetime
import functools


def session_check(coro):
    async def wrapper(self, *args, **kwargs):
        await self.require_session()
        return await coro(self, *args, **kwargs)
    return wrapper

def authorization_check(coro):
    async def wrapper(self, *args, **kwargs):
        if self.authorized and self.authorized['datetime'] < datetime.datetime.utcnow():
            await self.authorize()
        elif not self.authorized:
            await self.authorize()
        return await coro(self, *args, **kwargs) 
    return wrapper

def executor(func):
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        partial = functools.partial(func, *args, **kwargs)
        return loop.run_in_executor(None, partial)
    return wrapper
