import os
from flask import (
    Flask, flash, render_template, redirect,
    request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


def get_best_books():
    ten_best_books = list(
        mongo.db.books.find().sort("average_grade", -1).limit(10)
    )

    number_count = 1
    for book in ten_best_books:
        book["avg_gr_rounded"] = round(float(book["average_grade"]), 1)
        book["place"] = number_count
        book["stars"] = int(round(float(book["average_grade"]), 0))

        number_count += 1

    return ten_best_books


def get_colours():
    return [
        'darkgreen', 'acid', 'sandy', 'orange', 'brown'
        ]


def get_groups():
    cat_groups = list(mongo.db.category_groups.find())
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


@app.route("/", methods=["GET", "POST"])
@app.route("/books", methods=["GET", "POST"])
def get_books():
    best_books = get_best_books()
    category_groups = get_groups()

    return render_template(
        "books.html", best_books=best_books, category_groups=category_groups
    )


@app.route("/book/<book_id>")
def get_book(book_id):
    book = mongo.db.books.find_one({"_id": ObjectId(book_id)})

    book["avg_gr_rounded"] = round(float(book["average_grade"]), 1)
    book["stars"] = int(round(float(book["average_grade"]), 0))

    book_details = mongo.db.books_details.find_one(
        {"book_id": ObjectId(book_id)}
    )

    return render_template(
        "book.html", book=book, book_details=book_details
    )


@app.route("/search", methods=["GET", "POST"])
def search():
    search_str = request.form.get("title_or_author")
    books = list(mongo.db.books.find({"$or": [
        {"title": {"$regex": ".*" + search_str + ".*"}},
        {"author": {"$regex": ".*" + search_str + ".*"}}
        ]}))

    if not(books):
        flash("Sorry, there is no book in database matching your input")
        return redirect(url_for("get_books"))

    for book in books:
        avg_gr_rounded = round(float(book["average_grade"]), 1)
        book["avg_gr_rounded"] = avg_gr_rounded

    return render_template(
        "search_result.html", books=books
    )


@app.route("/add/book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        username = session["username"]
        grade = request.form.get("grade")
        if grade:
            average_grade = grade
            no_of_votes = 1
        else:
            average_grade = 0
            no_of_votes = 0

        book = {
            "title": request.form.get("title"),
            "author": request.form.get("author"),
            "image": request.form.get("image_link"),
            "category": request.form.get("category"),
            "average_grade": average_grade,
            "no_of_votes": no_of_votes,
            "added_by": username,
            "category_group": request.form.get("category_group")
        }
        result = mongo.db.books.insert_one(book)

        reviews_max5 = []
        review = request.form.get("review")
        if grade or review:
            reviews = {
                "grade": grade,
                "review": review,
                "added_by": username,
                "book_id": result.inserted_id
            }
            review_result = mongo.db.reviews.insert_one(reviews)

            opinion = {
                "_id": review_result.inserted_id,
                "grade": grade,
                "review": review,
                "added_by": username,
                "book_id": result.inserted_id
                }
            reviews_max5.append(opinion)

        book_details = {
            "published_date": request.form.get("published_date"),
            "identifier": request.form.get("identifier"),
            "description": request.form.get("description"),
            "reviews_max5": reviews_max5,
            "more_reviews": "n",
            "book_id": result.inserted_id
        }

        mongo.db.books_details.insert_one(book_details)
        flash("Book Successfully Added")

    return redirect(url_for("get_books"))


@app.route("/delete_book/<id>")
def delete_book(id):
    mongo.db.books.delete_one({"_id": ObjectId(id)})
    mongo.db.books_details.delete_one({"book_id": ObjectId(id)})
    mongo.db.reviews.delete_many({"book_id": ObjectId(id)})
    flash("Book Successfully Deleted")
    return redirect(url_for("get_books"))


@app.route("/add_opinion", methods=["GET", "POST"])
def add_opinion():
    book_id = request.form.get("book_id")
    grade_str = request.form.get("grade_m")
    review = request.form.get("review_m")
    if not(review) and not(grade_str):
        flash("No opinion added since you gave no values")
        return redirect(url_for("get_books"))

    if grade_str:
        grade = int(grade_str)
        book = mongo.db.books.find_one({"_id": ObjectId(book_id)})

        no_of_votes = int(book["no_of_votes"]) + 1
        new_average = (
            float(book["average_grade"]) * int(book["no_of_votes"]) + grade
            )/no_of_votes
        new_grading = {
            "average_grade": new_average,
            "no_of_votes": no_of_votes
        }
        mongo.db.books.update_one(
            {"_id": ObjectId(book_id)}, {"$set": new_grading})

    add_review = {
        "grade": grade_str,
        "review": review,
        "added_by": session["username"],
        "book_id": ObjectId(book_id)
    }
    mongo.db.reviews.insert_one(add_review)

    reviews_max5 = list(mongo.db.reviews.find(
        {"book_id": ObjectId(book_id)}).sort("_id", -1).limit(6))

    if len(reviews_max5) > 5:
        reviews_max5.pop()
        more_reviews = "y"
    else:
        more_reviews = "n"

    update_details = {
        "reviews_max5": reviews_max5,
        "more_reviews": more_reviews
    }
    mongo.db.books_details.update_one(
            {"book_id": ObjectId(book_id)}, {"$set": update_details})

    flash("Opinion Successfully Added")

    return redirect(url_for("get_book", book_id=book_id))


@app.route("/change_opinion", methods=["GET", "POST"])
def change_opinion():
    book_id = request.form.get("book_id")
    review_id = request.form.get("review_id")
    grade_str = request.form.get("grade_m")
    review = request.form.get("review_m")
    if not(review) and not(grade_str):
        flash("Something is wrong")
        return redirect(url_for("get_book", book_id=book_id))

    old_review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    if (old_review["grade"] != grade_str):
        grade_diff = int(grade_str) - int(old_review["grade"])
        book = mongo.db.books.find_one({"_id": ObjectId(book_id)})

        no_of_votes = int(book["no_of_votes"])
        new_average = (
            float(book["average_grade"]) * int(
                book["no_of_votes"]) + grade_diff)/no_of_votes
        new_grading = {
            "average_grade": new_average
        }
        mongo.db.books.update_one(
            {"_id": ObjectId(book_id)}, {"$set": new_grading})

    change_review = {
        "grade": grade_str,
        "review": review
    }
    mongo.db.reviews.update_one(
        {"_id": ObjectId(review_id)}, {"$set": change_review})

    reviews_max5 = list(mongo.db.reviews.find(
        {"book_id": ObjectId(book_id)}).sort("_id", -1).limit(6))

    if len(reviews_max5) > 5:
        reviews_max5.pop()
        more_reviews = "y"
    else:
        more_reviews = "n"

    update_details = {
        "reviews_max5": reviews_max5,
        "more_reviews": more_reviews
    }
    mongo.db.books_details.update_one(
            {"book_id": ObjectId(book_id)}, {"$set": update_details})

    flash("Opinion Successfully Changed")

    return redirect(url_for("get_book", book_id=book_id))


@app.route("/delete_opinion/<book_id>/<review_id>")
def delete_opinion(book_id, review_id):
    opinion = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    if not opinion:
        flash("Something went wrong")
        return redirect(url_for("get_book", book_id=book_id))

    mongo.db.reviews.delete_one({"_id": ObjectId(review_id)})

    book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    if opinion["grade"] and opinion["grade"] != "0":
        if book["no_of_votes"] < 2:
            no_of_votes = 0
            average_grade = 0
        else:
            no_of_votes = book["no_of_votes"]-1
            average_grade = (
                float(book["average_grade"]) * int(book["no_of_votes"])
                - int(opinion["grade"]))/no_of_votes
        new_grading = {
            "average_grade": average_grade,
            "no_of_votes": no_of_votes
        }
        mongo.db.books.update_one(
            {"_id": ObjectId(book_id)}, {"$set": new_grading})

    reviews_max5 = list(mongo.db.reviews.find(
        {"book_id": ObjectId(book_id)}).sort("_id", -1).limit(6))

    if len(reviews_max5) > 5:
        reviews_max5.pop()
        more_reviews = "y"
    else:
        more_reviews = "n"

    update_details = {
        "reviews_max5": reviews_max5,
        "more_reviews": more_reviews
    }
    mongo.db.books_details.update_one(
            {"book_id": ObjectId(book_id)}, {"$set": update_details})

    flash("Opinion Successfully Deleted")
    return redirect(url_for("get_book", book_id=book_id))


@app.route("/reviews/<book_id>/<title>", methods=["GET", "POST"])
def get_reviews(book_id, title):
    reviews = list(mongo.db.reviews.find(
        {"book_id": ObjectId(book_id)}).sort("_id", -1)
    )

    return render_template("reviews.html", reviews=reviews, title=title)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("signup", login=False))

        sign_up = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "email": request.form.get("email")
        }
        mongo.db.users.insert_one(sign_up)

        session["username"] = sign_up["username"]
        flash("Sign Up successfull")
        return redirect(url_for("get_books"))

    return render_template("login.html", login=False)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()}
        )

        if existing_user:
            if check_password_hash(
                existing_user["password"], request.form.get("password")
            ):
                session["username"] = request.form.get("username").lower()
                flash("Welcome, {}!".format(request.form.get("username")))
                return redirect(url_for("get_books"))
            else:
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login", login=True))

        else:
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login", login=True))

    return render_template("login.html", login=True)


@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("username")
    return redirect(url_for("get_books"))


@app.route("/get_category_groups")
def get_category_groups():
    category_groups = list(
        mongo.db.category_groups.find().sort("group_name", 1)
    )
    return render_template(
        "category_groups.html", category_groups=category_groups
    )


@app.route("/add_group", methods=["GET", "POST"])
def add_group():
    if request.method == "POST":
        group_name = {
            "group_name": request.form.get("group_name")
        }
        mongo.db.category_groups.insert_one(group_name)
        flash("New Category group Added")
        return redirect(url_for("get_category_groups"))

    return render_template("category_group.html")


@app.route(
    "/edit/group/<category_group_id>/<old_group_name>", methods=["GET", "POST"]
)
def edit_group(category_group_id, old_group_name):
    if request.method == "POST":
        new_name = request.form.get("group_name")

        mongo.db.category_groups.update_one({
            "_id": ObjectId(category_group_id)}, {
                "$set": {"group_name": new_name}
                })

        # Update affected books with the new category group name
        mongo.db.books.update_many({
            "category_group": old_group_name
            }, {
                "$set": {"category_group": new_name}
                })
        flash("Category Group Succesfully Updated")
        return redirect(url_for("get_category_groups"))

    group = mongo.db.category_groups.find_one({
        "_id": ObjectId(category_group_id)})
    return render_template("category_group.html", group=group, edit=True)


@app.route("/delete/group/<category_group_id>/<category_group>")
def delete_group(category_group_id, category_group):
    mongo.db.category_groups.remove({"_id": ObjectId(category_group_id)})

    # Update all affected books, to category group "Other"
    mongo.db.books.update_many({
            "category_group": category_group
            }, {
                "$set": {"category_group": "Other"}
                })
    flash("Category Group Successfully Deleted")
    return redirect(url_for("get_category_groups"))


@app.route("/search/category", methods=["GET", "POST"])
def search_category():
    category = request.form.get("category")
    category_books = list(
        mongo.db.books.find(
            {"category_group": category}
            ).sort("average_grade", -1).limit(10)
        )

    if not(category_books):
        flash("No books in that category group in database")
        return redirect(url_for("get_books"))

    for book in category_books:
        book["avg_gr_rounded"] = round(float(book["average_grade"]), 1)

    return render_template(
        "search_result.html", books=category_books,
        show_category=True, category=category
    )


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
