import duckdb
from pathlib import Path

data_dir = Path("../data")
data_dir.mkdir(exist_ok=True)

DB_NAME = data_dir / "news_therms.duckdb"
con = duckdb.connect(str(DB_NAME))

con.execute("""
    CREATE TABLE IF NOT EXISTS term_occurrence (
        term TEXT,
        source TEXT,
        date TIMESTAMP,
        PRIMARY KEY (term, source, date)
    )
""")

con.close()
