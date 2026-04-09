from abc import ABC, abstractmethod

from lab2.webScrapper import WebScrapper


class ShopScrapper(WebScrapper, ABC):
    @property
    def _call_delay(self) -> float:
        return 0.07

    @abstractmethod
    async def scrap_async(self, item_url: str) -> str | None:
        pass