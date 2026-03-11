from bs4 import BeautifulSoup

from lab2.webScrapper import WebScrapper
from lab1.scrappers.scrapper import PageTracker

class DjinniTitleScrapper(WebScrapper):
    _CALL_DELAY = 0.05
    @property
    def _call_delay(self) -> float:
        return self._CALL_DELAY

    _CATEGORY = "Data+Science"
    _MAX_PAGES = 7

    async def scrap_async(self):
        page_tracker = PageTracker()
        page_tracker.assign_max_pages(self._MAX_PAGES)
        titles = []

        next = True
        while next:
            html = await self._load_html(page_tracker.current_page)
            if not html:
                print(f"Failed to load page {page_tracker.current_page}")
                break

            soup = BeautifulSoup(html, 'html.parser')
            container = soup.find('ul', class_='list-unstyled list-jobs mb-4')
            if container:
                for content in container.find_all('li'):
                    a = content.find('a', class_="job-item__title-link")
                    if a:
                        title = a.text.strip()
                        href = a.get("href")
                        titles.append((title, href))

            next = page_tracker.try_next()

        return titles

    def _url_for_page(self, page: int):
        return f"https://djinni.co/jobs/?search_type=basic-search&primary_keyword={self._CATEGORY}&page={page}"


    async def _load_html(self, page):
        url = self._url_for_page(page)
        return await self._load_html_by_url(url)

