#!/usr/bin/python3 -u

from sys import stdin
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from queue import Queue
import requests
from time import sleep

def HTMLWriter(filename):
    def write(fut_response):
        print("writing {}".format(filename))
        with open(filename, 'w') as f:
            f.write(fut_response.result().text)
    return write

def get(url):
    print("Submitting job for url {}".format(url))
    sleep(5)
    return requests.get(url)

with ThreadPoolExecutor(max_workers=3) as executor:
    idx=0
    while True:
        try:
            url = stdin.readline()
        except KeyboardInterrupt:
            break
        if not url:
            break
        file = "/tmp/htmlwriter.{:03d}".format(idx)
        idx+=1
        executor.submit(get, url).add_done_callback(HTMLWriter(file))
