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


@app.route("/", methods=["GET", "POST"])
@app.route("/get_books", methods=["GET", "POST"])
def get_books():
    if request.method == "POST":
        category = request.form.get("category")
        print(category)
        category_books = list(
            mongo.db.books.find(
                {"category_group": category}
                ).sort("average_grade", -1).limit(10)
        )
        contains_category = 1
        print(contains_category)
    else:
        category_books = []
        contains_category = 0
        print(contains_category)

    books = mongo.db.books.find()
    category_groups = list(mongo.db.category_groups.find())
    # Do not want to send ObjectId
    group_names = [item["group_name"] for item in category_groups]
    return render_template(
        "books.html", books=books, category_groups=group_names,
        contains_category=contains_category, category_books=category_books
    )


@app.route("/get_book/<book_id>")
def get_book(book_id):
    book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    book_details = mongo.db.books_details.find_one(
        {"book_id": ObjectId(book_id)}
    )

    return render_template(
        "get_book.html", book=book, book_details=book_details
    )


@app.route("/add_book", methods=["GET", "POST"])
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
            opinion = {"grade": grade, "review": review, "added_by": username}
            reviews_max5.append(opinion)
            reviews = {
                "grade": grade,
                "review": review,
                "added_by": username,
                "book_id": result.inserted_id
            }
            mongo.db.reviews.insert_one(reviews)

        book_details = {
            "published_date": request.form.get("published_date"),
            "identifier": request.form.get("identifier"),
            "description": request.form.get("description"),
            "reviews_max5": reviews_max5,
            "more_reviews": "False",
            "book_id": result.inserted_id
        }

        mongo.db.books_details.insert_one(book_details)
        flash("Book Successfully Added")

    return redirect(url_for("get_books"))


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("sign_up"))

        sign_up = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "email": request.form.get("email")
        }
        mongo.db.users.insert_one(sign_up)

        session["username"] = sign_up["username"]
        flash("Sign Up successfull")
        return redirect(url_for("get_books"))

    return render_template("sign_up.html")


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
                return redirect(url_for("login"))

        else:
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


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

    return render_template("add_group.html")


@app.route("/edit_group/<id>", methods=["GET", "POST"])
def edit_group(id):
    if request.method == "POST":
        new_name = {
            "group_name": request.form.get("group_name")
        }
        print(new_name)
        mongo.db.category_groups.update({"_id": ObjectId(id)}, new_name)
        flash("Category Group Succesfully Updated")
        return redirect(url_for("get_category_groups"))

    group = mongo.db.category_groups.find_one({"_id": ObjectId(id)})
    return render_template("edit_group.html", group=group)


@app.route("/delete_group/<id>")
def delete_group(id):
    mongo.db.category_groups.remove({"_id": ObjectId(id)})
    flash("Category Group Successfully Deleted")
    return redirect(url_for("get_category_groups"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
