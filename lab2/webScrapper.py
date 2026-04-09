import asyncio
from abc import ABC, abstractmethod
from random import random
import numpy as np
from curl_cffi import requests, AsyncSession


class WebScrapper(ABC):
    @property
    @abstractmethod
    def _call_delay(self) -> float:
        pass

    async def _load_html_by_url(self, url, headers = None):
        if not headers:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Language": "en-US,en;q=0.9,uk;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": "\"Windows\"",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1"
            }

        async with AsyncSession(impersonate="chrome110") as session:
            try:
                response = await session.get(url, timeout=15)

                if response.status_code == 200:
                    html = response.text
                else:
                    print(f'Failed to load HTML for url: {url}')
                    print(f'Status code: {response.status_code}')
                    html = None
            except Exception as e:
                print(f'Request exception for url {url}: {e}')
                html = None

        actual_delay = self._call_delay * np.random.uniform(0.8, 1.2)
        await asyncio.sleep(actual_delay)

        return html