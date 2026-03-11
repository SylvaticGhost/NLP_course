from datetime import datetime
from typing import List

from bs4 import BeautifulSoup

from scrapper import Scrapper, Source, TitlePayload

class CensorScrapper(Scrapper):
    def _scrap_article(self, element: BeautifulSoup, date: datetime) -> TitlePayload:
        # Extract time with fallback
        time = date
        time_component = element.find('span', class_='main-items-text__time')
        if time_component:
            time_elem = time_component.find('time', class_='g-time')
            if time_elem:
                time_str = time_elem.get('datetime')
                if time_str:
                    try:
                        time = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
                    except (ValueError, AttributeError):
                        time = date

        # Extract title with fallback
        title = ""
        title_component = element.find('h2')
        if title_component:
            link = title_component.find('a', class_='news-list-item__link')
            if link:
                title = link.get("title", "")

        # Extract description with fallback
        description = ""
        description_component = element.find('a', class_='news-list-item__excerpt')
        if description_component:
            description = description_component.text.strip()

        full_text = (title + " " + description).strip()
        return TitlePayload(text=full_text, date=time)

    def _path_to_content(self) -> List[str]:
        return ["col-12 items-list"]

    def _url_for_date(self, date: datetime, page: int) -> str:
        date_str = date.strftime("%Y-%m-%d")
        return f"https://censor.net/ua/news/all/page/{page}/archive/{date_str}/category/0/sortby/date"

    @property
    def source(self) -> Source:
        return Source.CensorNet

    def _get_max_pages(self, page_soup: BeautifulSoup) -> int:
        pagination_count_element = page_soup.find('div', class_='pagination-count-page')
        pagination_text = pagination_count_element.get_text(strip=True)
        max_pages = int(pagination_text.split()[-1])
        return max_pages

    def _additional_cookies(self) -> dict:
        return {
            "user_session": "velq3mlvlseg1qrpct7sabc99a"
        }

    def _call_delay(self):
        return 2