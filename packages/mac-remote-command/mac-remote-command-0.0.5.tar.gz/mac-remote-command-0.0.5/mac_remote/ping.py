import time

import httpx

from . import get_summary

class EndlessPing():
    '''Ping MAC Commander every 30 seconds'''
    def __init__(self, commander_url: str) -> None:
        self.target = commander_url + 'ping'
        while True:
            try:
                payload = get_summary()
                httpx.post(self.target, json=payload)
            except Exception:
                pass
            time.sleep(30)