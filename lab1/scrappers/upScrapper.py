from datetime import datetime
from typing import List
from bs4 import BeautifulSoup

from lab1.scrappers.scrapper import NewsScrapper, Source, TitlePayload


class UpScrapper(NewsScrapper):
    def _scrap_article(self, element: BeautifulSoup, date: datetime) -> TitlePayload:
        tag = element.find('div', class_='article_time')
        time_str = tag.text.strip()
        time = UpScrapper._date_with_time(date, time_str)
        text = element.find('div', class_='article_title').text.strip()
        return TitlePayload(text=text, date=time)

    def _path_to_content(self) -> List[str]:
        return ['section_news_list_wrapper']

    def _url_for_date(self, date: datetime, page: int) -> str:
        date_str = date.strftime("%d%m%Y")
        return f"https://www.pravda.com.ua/news/date_{date_str}/"

    @property
    def source(self) -> Source:
        return Source.UP

