import duckdb
import pandas as pd
from pathlib import Path

data_dir = Path("../data")
db_path = data_dir / "news_therms.duckdb"
con = duckdb.connect(db_path)

query = """
SELECT * FROM term_occurrence
    WHERE source in ('UP', 'RBC')
"""

df_raw = con.execute(query).df()

df_raw.to_csv(data_dir / "news_therms.csv", index=False)