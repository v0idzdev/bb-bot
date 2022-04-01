import datetime


def authorization_check(coro):
    async def wrapper(self, *args, **kwargs):
        if self.authorized and self.authorized["datetime"] < datetime.datetime.utcnow():
            await self.authorize()
        elif not self.authorized:
            await self.authorize()
        return await coro(self, *args, **kwargs)

    return wrapper