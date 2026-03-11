from datetime import datetime
from typing import List

from bs4 import BeautifulSoup

from lab1.scrappers.scrapper import Scrapper, Source, TitlePayload


class RbcScrapper(Scrapper):
    def _scrap_article(self, element: BeautifulSoup, date: datetime) -> TitlePayload:
        time = element.find("span", class_="time").text.strip()
        date_time = self._date_with_time(date, time)

        text = element.find("a").text.strip()
        return TitlePayload(text=text, date=date_time)

    def _path_to_content(self) -> List[str]:
        return ["newsline"]

    def _url_for_date(self, date: datetime, page: int) -> str:
        date = date.strftime("%Y/%m/%d")
        return f"https://www.rbc.ua/rus/archive/{date}"

    @property
    def source(self) -> Source:
        return Source.RBC