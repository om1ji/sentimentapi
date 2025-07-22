import sqlite3
import flask
from flask import request
from datetime import datetime

app = flask.Flask("SentimentAPI")


class DatabaseService:
    def __init__(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                sentiment TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
        """

        with sqlite3.connect("reviews.db") as conn:
            self.cursor = conn.cursor()
            self.cursor.execute(create_table_query)

    def get_reviews(self, sentiment: str = None):
        with sqlite3.connect("reviews.db") as conn:
            cursor = conn.cursor()
            if sentiment:
                cursor.execute(
                    "SELECT * FROM reviews WHERE sentiment = ?", (sentiment,)
                )
            else:
                cursor.execute("SELECT * FROM reviews")
            reviews = cursor.fetchall()
            result = [
                dict(zip(["id", "text", "sentiment", "created_at"], review))
                for review in reviews
            ]
            return result

    def add_review(self, text: str, sentiment: str):
        now = datetime.utcnow().isoformat()
        with sqlite3.connect("reviews.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO reviews (text, sentiment, created_at) VALUES (?, ?, ?)",
                (text, sentiment, now),
            )
            review_id = cursor.lastrowid
            cursor.execute("SELECT * FROM reviews WHERE id = ?", (review_id,))
            review = cursor.fetchone()
            result = dict(zip(["id", "text", "sentiment", "created_at"], review))

        return result


class ReviewService:
    SENTIMENT_KEYWORDS = {
        "positive": ("хорош", "отличн", "любим", "любл", "прекрасн"),
        "negative": ("плох", "ужасн", "отврат"),
    }

    def __init__(self):
        pass

    @classmethod
    def get_sentiment(cls, text: str) -> str:
        text_lower = text.lower()
        for sentiment, keywords in cls.SENTIMENT_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return sentiment
        return "neutral"

    def add_review(self, review_text: dict) -> dict:
        sentiment = reviews_service.get_sentiment(review_text)
        result = db.add_review(review_text, sentiment)
        return result

    def get_sentiments(self, sentiment: str = None) -> dict:
        reviews = db.get_reviews(sentiment)
        return {"reviews": reviews}


db = DatabaseService()
reviews_service = ReviewService()


@app.route("/reviews", methods=["POST"])
def process_review():
    data = request.get_json()
    text = data.get("text", None)

    if text is None:
        return {"error": "Поле text пропущено"}, 400

    if text == "":
        return {"error": "Поле text пустое"}, 400

    result = reviews_service.add_review(text)
    return result, 201


@app.get("/reviews")
def get_reviews():
    params = request.args
    sentiment = params.get("sentiment", None)
    result = reviews_service.get_sentiments(sentiment)
    return result, 200


if __name__ == "__main__":
    app.run(port=8000)
