def session_check(coro):
    async def wrapper(self, *args, **kwargs):
        await self.require_session()
        return await coro(self, *args, **kwargs)

    return wrapper