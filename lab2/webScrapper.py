import asyncio
from abc import ABC, abstractmethod
import aiohttp


class WebScrapper(ABC):
    @property
    @abstractmethod
    def _call_delay(self) -> float:
        pass

    async def _load_html_by_url(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        html = None
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    html = await response.text()
                else:
                    html = None

        await asyncio.sleep(self._call_delay)
        return html