import time

import httpx

from . import get_summary

class EndlessPing():
    '''Ping MAC Commander every 30 seconds'''
    def __init__(self, commander_url: str) -> None:
        self.target = commander_url + 'ping'
        while True:
            payload = get_summary()
            httpx.post(self.target, json=payload)
            time.sleep(30)