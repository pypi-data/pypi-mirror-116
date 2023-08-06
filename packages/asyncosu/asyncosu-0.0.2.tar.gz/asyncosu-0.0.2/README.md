<div align="center">

# AsyncOsu

</div>

Asynchronous osu! api wrapper for python using aiohttp. 

## OsuApiV2
This package supports [osu api v2.](https://osu.ppy.sh/docs/index.html)

Basic usage with context manager:

```python
import asyncio
from asyncosu import OsuApiV2


async def main():
    async with OsuApiV2(client_id='client_id', client_secret='client_secret') as osu_api:
        return await osu_api.get_user_from_username(f'heyronii')


if __name__ == "__main__":
    print(asyncio.run(main()))
```

without context_manager:

```python
async def main():
    osu_api = OsuApiV2(client_id='client_id', client_secret='client_secret')
    user_info = await osu_api.get_user_from_username(f'heyronii')
    await osu_api.close()  # Close the connection before creating another instance
    return user_info
```
