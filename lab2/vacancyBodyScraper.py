from bs4 import BeautifulSoup
from lab2.webScrapper import WebScrapper


class VacancyBodyScraper(WebScrapper):
    @property
    def _call_delay(self) -> float:
        return 0.05

    async def scrap_async(self, job_url: str) -> str | None:
        url = f'https://djinni.co{job_url}'
        html = await self._load_html_by_url(url)
        soup = BeautifulSoup(html, 'html.parser')
        description = soup.find('div', class_='mb-4 job-post__description')
        if description is None:
            print(f'No description found for url: {url}')
            return None

        text = description.get_text(separator=' ').strip()
        return text
