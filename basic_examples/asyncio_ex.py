import os
import sys
import asyncio

async def open_file(file):
    with open(file) as f:
    	print('successfully...')


async def open_path(path):
    lst = os.listdir(path)
    for f in lst:
        file = os.path.join(path, f)
        if os.path.isfile(file):
            await open_file(file)



loop = asyncio.get_event_loop()
loop.run_until_complete(open_path(r'f:\test'))
loop.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(open_path(r'f:\test'))
loop.close()