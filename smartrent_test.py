import asyncio

from smartrent import async_login

async def main():
    api = await async_login('sainath.mcs@gmail.com', 'sainathniz@SP20')
    
    lock = api.get_locks()[0]
    locked = lock.get_locked()

    if not locked:
        await lock.async_set_locked(True)

asyncio.run(main())

asyncio.run(main())