#!/usr/bin/env python3
# encoding: utf-8

import requests
import asyncio
import aiohttp
import time


Website = ["http://www.google.fr",
            "http://www.google.com",
            "http://www.lemonde.fr",
            "http://www.huffingtonpost.fr",
            "http://www.hardware.fr",
            "http://www.igbmc.fr"]

# Website = ["http://www.google.com"]

def BenchRequests(WebList):
    for site in WebList:
        print("Requests begin : {}".format(site))
        r = requests.get(site)
        assert r.status_code == 200
        print("Requests end : {}".format(site))

@asyncio.coroutine
def fetch_page(url):
    print("Aiohtpp begin : {}".format(url))
    response = yield from aiohttp.request('GET', url)
    assert response.status == 200
    response.close()
    print("Aiohtpp end : {}".format(url))

def BenchAiohttp(WebList):
    loop = asyncio.get_event_loop()
    tasks = [fetch_page(site) for site in WebList]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

if __name__ == "__main__":
    start = time.time()
    BenchRequests(Website)
    print('Time taken Requests :', time.time()-start)
    start = time.time()
    BenchAiohttp(Website)
    print('Time taken aiohttp  :', time.time()-start)
