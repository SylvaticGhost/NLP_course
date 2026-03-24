import duckdb
from pathlib import Path

data_dir = Path("../data")
data_dir.mkdir(exist_ok=True)

DB_NAME = data_dir / "products.duckdb"
con = duckdb.connect(str(DB_NAME))

product_table = """
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        product_category VARCHAR,
        review_count INTEGER,
        question_count INTEGER,
        recommended_count INTEGER,
        not_recommended_count INTEGER,
        recommended_percentage FLOAT,
        reviews_with_images_count INTEGER,
        reviews_with_videos_count INTEGER,
        average_rating FLOAT,
        positive_percentage FLOAT,
    )
"""

review_table = """
    CREATE TABLE IF NOT EXISTS reviews (
    id uuid PRIMARY KEY,
    product_id INTEGER,
    rating FLOAT,
    title VARCHAR,
    text VARCHAR,
    is_verified BOOLEAN,
    submitted_at TIMESTAMP
)
    """

con.execute(product_table)
con.execute(review_table)
con.close()

