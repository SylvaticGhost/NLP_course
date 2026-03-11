import asyncio
from abc import abstractmethod, ABC
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import List

import aiohttp
from bs4 import BeautifulSoup


class Source(Enum):
    CensorNet = 1
    UP = 2
    RBC = 3

class PageTracker:
    def __init__(self):
        self.current_page = 1
        self._max_pages = None

    @property
    def max_pages(self) -> int:
        return self._max_pages if self._max_pages is not None else 1

    def is_max_page_assigned(self) -> bool:
        return self._max_pages is not None

    def assign_max_pages(self, pages: int) -> None:
        if self._max_pages is None:
            self._max_pages = pages

    def reach_end(self) -> bool:
        return self.current_page >= self.max_pages

    def next(self) -> None:
        if self.reach_end():
            raise StopIteration("No more pages to load")
        self.current_page += 1

    def try_next(self) -> bool:
        if self.reach_end():
            return False
        self.current_page += 1
        return True

@dataclass
class TitlePayload:
    text: str
    date: datetime

class Scrapper(ABC):

    @property
    @abstractmethod
    def source(self) -> Source:
        pass

    def _call_delay(self):
        return 0.05

    async def scrap_async(self, start_date: datetime, end_date: datetime) -> List[TitlePayload]:
        current_date = start_date
        contents = []
        page_tracker = PageTracker()
        while current_date <= end_date:
            html = await self._load_html_for_date_async(current_date, page_tracker.current_page)
            soup = BeautifulSoup(html, 'html.parser')

            if not page_tracker.is_max_page_assigned():
                max_pages = self._get_max_pages(soup)
                page_tracker.assign_max_pages(max_pages)

            content_container = self._find_content_container(soup)

            for content in content_container.find_all(recursive=False):
                soup_c = BeautifulSoup(str(content), 'html.parser')
                payload = self._scrap_article(soup_c, current_date)
                contents.append(payload)

            if page_tracker.reach_end():
                current_date += timedelta(days=1)
                page_tracker = PageTracker()
            else:
                page_tracker.next()
        return contents

    def _find_content_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        container = soup
        for class_name in self._path_to_content():
            container = container.find('div', class_=class_name)
            if not container:
                raise ValueError(f"Could not find container with class '{class_name}'")
        return container

    @abstractmethod
    def _scrap_article(self, element: BeautifulSoup, date: datetime) -> TitlePayload:
        pass

    @abstractmethod
    def _url_for_date(self, date: datetime, page: int) -> str:
        pass

    @abstractmethod
    def _path_to_content(self) -> List[str]:
        pass

    def _get_max_pages(self, page_soup: BeautifulSoup) -> int:
        return 1


    _HTML_DIR = Path('../html_cache')

    async def _load_html_for_date_async(self, date: datetime, page: int) -> str:
        date_str = date.strftime("%Y%m%d")
        file_path = self._HTML_DIR / f"{self.source.name}_{date_str}_{page}.html"

        today = datetime.now().date()
        is_today = date.date() == today

        if not is_today and file_path.exists():
            return file_path.read_text(encoding='utf-8')

        url = self._url_for_date(date, page)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        html = None
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                html = await response.text()

                self._HTML_DIR.mkdir(exist_ok=True)
                file_path.write_text(html, encoding='utf-8')

        await asyncio.sleep(self._call_delay())
        return html

    @staticmethod
    def _date_with_time(date: datetime, time_str: str) -> datetime:
        time_parts = time_str.split(':')
        return date.replace(hour=int(time_parts[0]), minute=int(time_parts[1]))



