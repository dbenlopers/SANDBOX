#!/usr/bin/env python3
# encoding: utf-8

import asyncio
import aiohttp
 
@asyncio.coroutine
def do_work(task_name, work_queue):
    while not work_queue.empty():
        queue_item = yield from work_queue.get()
        print('{0} grabbed item: {1}'.format(task_name, queue_item))
        yield from asyncio.sleep(0.5)
 
if __name__ == "__main__":
    q = asyncio.Queue()
 
    for x in range(20):
        q.put_nowait(x)
 
    print(q)
 
    loop = asyncio.get_event_loop()
 
    tasks = [
        asyncio.async(do_work('task1', q)),
        asyncio.async(do_work('task2', q)),
        asyncio.async(do_work('task3', q))]
 
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

"""
@asyncio.coroutine
def fetch_page(url, pause=False):
    if pause:
        yield from asyncio.sleep(2)
 
    response = yield from aiohttp.request('GET', url)
    assert response.status == 200
    content = yield from response.read()
    print('URL: {0}:  Content: {1}'.format(url, content))

loop = asyncio.get_event_loop()
tasks = [
    fetch_page('http://google.com'),
    fetch_page('http://cnn.com', True),
    fetch_page('http://twitter.com')]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
 
for task in tasks:
    print(task)
"""
