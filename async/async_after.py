import asyncio
import time

async def async_task(task_number, duration):
    print(f'started {task_number}')
    await asyncio.sleep(duration)
    print(f'ended {task_number}')
    
async def main():
    task1 = asyncio.create_task(\
        async_task(1, 3))
    task2 = asyncio.create_task(\
        async_task(2, 2))
    task3 = asyncio.create_task(\
        async_task(3, 1))
    
    await task1
    await task2
    await task3
    
async def gather_main():
    await asyncio.gather(async_task(1, 3)
                         , async_task(2, 2)
                         , async_task(3, 1)
                         )
    
begin = time.time()
asyncio.run(gather_main())
end = time.time()

print(end - begin)