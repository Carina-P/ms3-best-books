"""
Server-side code for the application ms3-best-books.
"""

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


###########
# Book/s: #
###########
def get_best_books():
    """
    Search in database for the ten best books according to books grades.

    Return: (list of dictionaries) - the ten best books
    """
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
    """
    Returns colours used when showing category groups

    return: (list of str) - the colours
    """
    return [
        'darkgreen', 'acid', 'sandy', 'orange', 'brown'
        ]


def get_groups():
    """
    Get current category groups from database

    return: (list of dictionaries) - with category groups
    """
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
def get_books():
    """
    Fetch best books and current category groups.
    Take user to home-page and show retrieved information.
    """
    best_books = get_best_books()
    category_groups = get_groups()

    return render_template(
        "books.html", best_books=best_books, category_groups=category_groups
    )


@app.route("/book/<book_id>")
def get_book(book_id):
    """
    Get information about book with id equal to book_id.
    Render the book information page and show retrieved information.

    Input:
        book_id (object): The database _id for book
    """
    book = mongo.db.books.find_one({"_id": ObjectId(book_id)})

    # Round average grade, retrived from database, to one decimal
    book["avg_gr_rounded"] = round(float(book["average_grade"]), 1)
    # Round average grade to integer - that is number of stars to show for book
    book["stars"] = int(round(float(book["average_grade"]), 0))

    book_details = mongo.db.books_details.find_one(
        {"book_id": ObjectId(book_id)}
    )

    return render_template(
        "book.html", book=book, book_details=book_details
    )


@app.route("/search", methods=["GET", "POST"])
def search():
    """
    With given search-string (containing book title or author), retrieved from
    form in page, search in database for books with that title or author.

    Render search-result page and show retrieved information
    """
    search_str = request.form.get("title_or_author")
    books = list(mongo.db.books.find({"$or": [
        {"title": {"$regex": ".*" + search_str + ".*"}},
        {"author": {"$regex": ".*" + search_str + ".*"}}
        ]}))

    if not(books):
        flash("Sorry, there is no book in database matching your input")
        return redirect(url_for("get_books"))

    for book in books:
        # Round average grade, retrived from database, to one decimal
        avg_gr_rounded = round(float(book["average_grade"]), 1)
        book["avg_gr_rounded"] = avg_gr_rounded

    return render_template(
        "search_result.html", books=books
    )


@app.route("/add/book", methods=["GET", "POST"])
def add_book():
    """
    Get information about book from form in page and add book information to
    database. Inform user if book is added or not.
    And then book details page is rendered with new database information.
    """
    if request.method == "POST":
        username = session["username"]
        grade_str = request.form.get("grade")
        grade = int(grade_str)
        if grade_str:
            grade = int(grade_str)
            average_grade = grade
            no_of_votes = 1
        else:
            grade=0
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
        # Only add opinion if grade and/or review is given
        # Notice that two collections are updated with review: reviews and
        # book_details that contains the five last reviews.
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
        flash('The book "' + book["title"] + '" is successfully added')

    return redirect(url_for("get_book", book_id=result.inserted_id))


@app.route("/delete/book/<book_id>")
def delete_book(book_id):
    """
    Remove book with id = book_id from database.
    Redirect user to home page.
    """
    mongo.db.books.delete_one({"_id": ObjectId(book_id)})
    mongo.db.books_details.delete_one({"book_id": ObjectId(book_id)})
    mongo.db.reviews.delete_many({"book_id": ObjectId(book_id)})
    flash("Book Successfully Deleted")
    return redirect(url_for("get_books"))


####################
# Opinions/reviews #
####################
def get_5_reviews(book_id):
    """
    Get the five latest reviews for a book with id=book_id in database.

    input:
        book_id (str): Id for book in database
    return: (directory with:
                reviews_max5: (list with, at the most, five latest reviews)
                more_reviews: (str "y" or "n" depending on if there are more
                than five reviews)
            )
    )
    """
    # Try to retieve max six reviews to find out if there is more than five
    reviews_max5 = list(mongo.db.reviews.find(
        {"book_id": ObjectId(book_id)}).sort("_id", -1).limit(6))

    # If more than 5 reviews remove oldest review of them
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


@app.route("/add/opinion", methods=["GET", "POST"])
def add_opinion():
    """
    Get review information about book and opinion from form in page.
    Add opinion about the book to database.

    Then redirect user to book detail page.
    """
    book_id = request.form.get("book_id")
    grade_str = request.form.get("grade_m")
    review = request.form.get("review_m")
    # if something is wrong and review and grade is missing
    if not(review) and not(grade_str):
        flash("No opinion added since you gave no values")
        return redirect(url_for("get_books"))

    # Grade is given
    if grade_str:
        grade = int(grade_str)
        book = mongo.db.books.find_one({"_id": ObjectId(book_id)})

        # Now one more vote is given for the book
        no_of_votes = int(book["no_of_votes"]) + 1
        # New vote gives an new average_grade
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

    mongo.db.books_details.update_one(
            {"book_id": ObjectId(book_id)}, {"$set": get_5_reviews(book_id)})

    flash("Opinion Successfully Added")

    return redirect(url_for("get_book", book_id=book_id))


@app.route("/change/opinion", methods=["GET", "POST"])
def change_opinion():
    """
    Read from form in page and update database with the change in opinion.
    Notice: If the grade is changed - average_grade must be recalculated.
    And if review is changed, besides collection: reviews, it might also effect
    collection: books-details that contains the five latest reviews.
    """
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

    mongo.db.books_details.update_one(
            {"book_id": ObjectId(book_id)}, {"$set": get_5_reviews(book_id)})

    flash("Opinion Successfully Changed")

    return redirect(url_for("get_book", book_id=book_id))


@app.route("/delete/opinion/<book_id>/<review_id>")
def delete_opinion(book_id, review_id):
    """
    Delete opinion, with id=review_id, from database.
    Notice: This affects the average grade for the book with id=book_id
    and it also might affect the last 5 reviews that is stored in collection:
    book_details.
    Then redirect user to page with book details.
    """
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

    mongo.db.books_details.update_one(
            {"book_id": ObjectId(book_id)}, {"$set": get_5_reviews(book_id)})

    flash("Opinion Successfully Deleted")
    return redirect(url_for("get_book", book_id=book_id))


@app.route("/reviews/<book_id>/<title>", methods=["GET", "POST"])
def get_reviews(book_id, title):
    """
    Get all reviews for a book with id=book_id in database.
    Render the reviews page and show retrieved information.
    """
    reviews = list(mongo.db.reviews.find(
        {"book_id": ObjectId(book_id)}).sort("_id", -1)
    )

    return render_template(
        "reviews.html", reviews=reviews, title=title, book_id=book_id
    )


###################
# Category groups #
###################
@app.route("/categories")
def get_category_groups():
    """
    Get all category groups from the database.
    Render category_groups page and show retrieved information.
    """
    category_groups = list(
        mongo.db.category_groups.find().sort("group_name", 1)
    )
    return render_template(
        "category_groups.html", category_groups=category_groups
    )


@app.route("/add/group", methods=["GET", "POST"])
def add_group():
    """
    Render page with category groups.
    If form is filled out, new category group name is retrieved from form and
    then added to database. When done redirect user to page with category
    groups.
    """
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
    """
    Render category group page with current category group information.

    If values in form is changed and posted, database is updated accordingly.
    Notice that all books that have this category group also have to be updated
    with changed category group name. Then user is redirected to category
    groups page
    """
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
    """
    Delete group in database with id=category_group_id.
    Notice that all books in this category_group is effected. Their category
    group is changed to "Other".
    User is then redirected to page with category groups.
    """
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
    """
    Get category group from form and find the ten most popular books that
    belong to this category group.
    Then render page search_results.
    """
    category = request.form.get("category")
    category_books = list(
        mongo.db.books.find(
            {"category_group": category}
            ).sort("average_grade", -1).limit(10)
        )

    if not(category_books):
        flash("No books in that category group in database")
        return redirect(url_for("get_books"))
    
    # The average grade is rounded to one decimal.
    for book in category_books:
        book["avg_gr_rounded"] = round(float(book["average_grade"]), 1)

    return render_template(
        "search_result.html", books=category_books,
        show_category=True, category=category
    )


#########################
# Access administration #
#########################
@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Register user in database.
    Then redirect user to home-page.
    If user already exists in database, user is redirected to login page.
    """
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

        # Put username in session-variable
        session["username"] = sign_up["username"]
        flash("Sign Up successfull - Welcome, {}!".format(
            request.form.get("username")
        ))
        return redirect(url_for("get_books"))

    return render_template("login.html", login=False)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Get username and password from form in page. Check that combination of user
    and password exists. If OK redirect user to home page. Otherwise user is
    returned to login page.
    """
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
    """
    Logout user, which is done by removing session variable username.
    Redirect user to home page.
    """
    flash("You have been logged out")
    session.pop("username")
    return redirect(url_for("get_books"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
