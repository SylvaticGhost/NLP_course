import duckdb
from pathlib import Path
from typing import List

from therm import Therm


class TermOccurrenceRepository:
    def __init__(self):
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        self.db_path = data_dir / "news_therms.duckdb"


    def save_therms(self, therms: List[Therm]) -> int:
        if not therms:
            return 0

        records = []
        for therm in therms:
            records.append((
                therm.word,
                therm.source.name,
                therm.date
            ))

        unique_records = list(set(records))

        if not unique_records:
            return 0

        with duckdb.connect(str(self.db_path)) as con:
            inserted = 0
            for record in unique_records:
                result = con.execute(
                    "INSERT INTO term_occurrence (term, source, date) VALUES (?, ?, ?) ON CONFLICT DO NOTHING",
                    record
                )
                if result.fetchall():
                    inserted += 1

            con.commit()

        return inserted



