import os
from flask import Flask, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


def get_best_books():
    """
    Search in database for the ten best books according to books grades.

    Return: (list of dictionaries) - the ten best books
    """
    try:
        ten_best_books = list(
            mongo.db.books.find().sort("average_grade", -1).limit(10)
        )
    except Exception as e:
        flash(
            "Something went wrong when accessing the database, to get books"
            + e
        )
        return []
    else:
        number_count = 1
        for book in ten_best_books:
            book["avg_gr_rounded"] = round(float(book["average_grade"]), 1)
            book["place"] = number_count
            book["stars"] = int(round(float(book["average_grade"]), 0))

            number_count += 1

    return ten_best_books


def get_colours():
    """
    Returns colours used when showing category groups
    Return: (list of str) - the colours
    """
    return [
        'darkgreen', 'acid', 'sandy', 'orange', 'red', 'brown'
        ]


def get_groups():
    """
    Get current category groups from database
    Return: (list of dictionaries) - with category groups
    """
    try:
        cat_groups = list(mongo.db.category_groups.find())
    except Exception as e:
        flash(
            "Something went wrong when accessing the database to get"
            + "category groups" + e
        )
        return []
    else:
        category_groups = []
        colours = get_colours()
        length = len(colours)

        index = 0
        for group in cat_groups:
            category_groups.append(
                {
                    "group_name": group['group_name'],
                    "colour": colours[index % length]
                }
            )
            index += 1

    return category_groups


def get_5_reviews(book_id):
    """
    Get the five latest reviews for a book with id=book_id in database.

    input:
        book_id (str): Id for book in database
    Return: (directory with:
                reviews_max5: (list with, at the most, five latest reviews)
                more_reviews: (str "y" or "n" depending on if there are more
                than five reviews)
            )
    )
    """
    # Try to retrieve max six reviews to find out if there is more than five
    try:
        reviews_max5 = list(mongo.db.reviews.find(
            {"book_id": ObjectId(book_id)}).sort("_id", -1).limit(6))
    except Exception as e:
        flash(
            "Something went wrong when accessing databas to retrieve "
            + "reviews" + e
        )
        return []

    # More than 5 reviews remove oldest review of them
    if len(reviews_max5) > 5:
        reviews_max5.pop()
        more_reviews = "y"
    else:
        more_reviews = "n"

    five_reviews = {
        "reviews_max5": reviews_max5,
        "more_reviews": more_reviews
    }
    return five_reviews
