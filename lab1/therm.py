from dataclasses import dataclass
from datetime import datetime

from lab1.scrappers.scrapper import Source


@dataclass
class Therm:
    word: str
    source: Source
    date: datetime
