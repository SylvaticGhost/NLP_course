import requests
import duckdb
import time
from pathlib import Path

# product 1
# TCin = 92038440
# Category = "electronics"

# product 2
# TCin = 91466170
# Category = "electronics"

# product 3
# TCin = 53737584
# Category = "electronics"

# product 4
# TCin = 94682574
# Category = "electronics"

# product 5
TCin = 79390423
Category = "electronics"

API_KEY="c6b68aaef0eac4df4931aae70500b7056531cb37"

DATA_DIR = Path("./data")
DATA_DIR.mkdir(exist_ok=True)
DB_NAME = DATA_DIR / "products.duckdb"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

def get_api_url(tcin: str, page: int, size: int = 50) -> str:
    return (
        f"https://r2d2.target.com/ratings_reviews_api/v1/summary?"
        f"key={API_KEY}&hasOnlyPhotos=false&"
        f"includes=reviews,statistics&page={page}&"
        f"reviewedId={tcin}&reviewType=PRODUCT&"
        f"size={size}&sortBy=most_recent&verifiedOnly=false"
    )


def fetch_and_store_reviews(tcin: str, category: str):
    con = duckdb.connect(str(DB_NAME))

    page = 1
    total_pages = 1
    session = requests.Session()
    session.headers.update(HEADERS)

    print(f"Розпочато збір даних для товару TCIN: {tcin} (Категорія: {category})")

    while page <= total_pages:
        url = get_api_url(tcin, page)
        response = session.get(url)

        if response.status_code != 200:
            print(f"Помилка API на сторінці {page}: {response.status_code}")
            print(f"Error details: {response.text}")
            break

        data = response.json()

        # Обробка статистики товару (робимо лише на першій сторінці)
        if page == 1 and "statistics" in data:
            stats = data["statistics"]
            rating_stats = stats.get("rating", {})

            product_data = (
                int(tcin),
                category,
                stats.get("review_count", 0),
                stats.get("question_count", 0),
                stats.get("recommended_count", 0),
                stats.get("not_recommended_count", 0),
                stats.get("recommended_percentage", 0.0),
                stats.get("reviews_with_images_count", 0),
                stats.get("reviews_with_videos_count", 0),
                rating_stats.get("average", 0.0),
                rating_stats.get("positive_percentage", 0.0)
            )

            con.execute("""
                        INSERT INTO products (product_id, product_category, review_count, question_count,
                                              recommended_count, not_recommended_count, recommended_percentage,
                                              reviews_with_images_count, reviews_with_videos_count,
                                              average_rating, positive_percentage)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (product_id) DO
                        UPDATE SET
                            review_count = excluded.review_count,
                            average_rating = excluded.average_rating,
                            positive_percentage = excluded.positive_percentage
                        """, product_data)
            print(f"Статистику товару {tcin} збережено/оновлено.")

        # Обробка масиву відгуків
        if "reviews" in data and "results" in data["reviews"]:
            reviews_data = data["reviews"]
            total_pages = reviews_data.get("total_pages", 1)
            results = reviews_data.get("results", [])

            if not results:
                break

            reviews_batch = []
            for review in results:
                reviews_batch.append((
                    review.get("id"),
                    int(tcin),
                    float(review.get("Rating", 0)),
                    review.get("title", ""),
                    review.get("text", ""),
                    review.get("is_verified", False),
                    review.get("submitted_at")
                ))

            # Пакетна вставка відгуків
            if reviews_batch:
                con.executemany("""
                                INSERT INTO reviews (id, product_id, rating, title, text, is_verified, submitted_at)
                                VALUES (?, ?, ?, ?, ?, ?, ?) ON CONFLICT (id) DO NOTHING
                                """, reviews_batch)

            print(f"Опрацьовано сторінку {page}/{total_pages} ({len(reviews_batch)} відгуків)")
        else:
            print("Більше відгуків не знайдено.")
            break

        page += 1
        time.sleep(0.5)  # Затримка між запитами, щоб не отримати блокування (Rate Limit)

    con.close()
    print(f"Збір даних для TCIN {tcin} успішно завершено.")

fetch_and_store_reviews(TCin, Category)