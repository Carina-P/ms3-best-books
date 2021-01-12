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

from utilities import (
    get_best_books, get_groups, get_5_reviews
)

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/", methods=["GET", "POST"])
def get_books():
    """
    Fetch best books and current category groups.
    Take user to home-page and show retrieved information.
    """
    best_books = get_best_books()
    if best_books:
        category_groups = get_groups()

    return render_template(
        "pages/books.html", best_books=best_books,
        category_groups=category_groups
    )


@app.route("/book/<book_id>")
def get_book(book_id):
    """
    Get information about book with id equal to book_id.
    Render the book information page and show retrieved information.

    Input:
        book_id (object): The database _id for book
    """
    try:
        book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    except Exception as e:
        flash(
            "Something went wrong when accessing the database, to find book"
            + e
        )
        return redirect(url_for("get_books"))

    # Round average grade, retrived from database, to one decimal
    book["avg_gr_rounded"] = round(float(book["average_grade"]), 1)
    # Round average grade to integer - that is number of stars to show
    book["stars"] = int(round(float(book["average_grade"]), 0))

    try:
        book_details = mongo.db.books_details.find_one(
            {"book_id": ObjectId(book_id)}
        )
    except Exception as e:
        book_details = []
        flash(
            "Something went wrong when accessing the database, to find"
            + "book details" + e
        )
        return redirect(url_for("get_books"))

    return render_template(
        "pages/book.html", book=book, book_details=book_details
    )


@app.route("/search", methods=["GET", "POST"])
def search():
    """
    With given search-string (containing book title or author), retrieved from
    form in page, search in database for books with that title or author.

    Render search-result page and show retrieved information
    """
    search_str = request.form.get("title_or_author")
    try:
        books = list(mongo.db.books.find({"$or": [
            {"title": {"$regex": ".*" + search_str + ".*"}},
            {"author": {"$regex": ".*" + search_str + ".*"}}
            ]}))
    except Exception as e:
        flash(
            "Something went wrong when accessing the database, to get books"
            + e
        )
        books = []
        return redirect(url_for("get_books"))
    else:
        if not(books):
            flash("Sorry, there is no book in database matching your input")
            return redirect(url_for("get_books"))

    for book in books:
        # Round average grade, retrived from database, to one decimal
        avg_gr_rounded = round(float(book["average_grade"]), 1)
        book["avg_gr_rounded"] = avg_gr_rounded

    return render_template(
        "pages/search_result.html", books=books
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

        if grade_str:
            grade = int(grade_str)
            average_grade = grade
            no_of_votes = 1
        else:
            grade = 0
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

        try:
            result = mongo.db.books.insert_one(book)
        except Exception as e:
            flash(
                "Something went wrong when accessing the database, to insert"
                + "book" + e
            )
            # Do not try to do anything more, go back to home page
            return redirect(url_for("get_books"))

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
            try:
                review_result = mongo.db.reviews.insert_one(reviews)
            except Exception as e:
                flash(
                    "Something went wrong when accessing the database, to"
                    + "insert review" + e
                )
                # Do not try to do anything more, go back to home page
                return redirect(url_for("get_books"))

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

        try:
            mongo.db.books_details.insert_one(book_details)
        except Exception as e:
            flash(
                "Something went wrong when accessing the database, to insert"
                + "book details" + e
            )
            flash(
                "Notice! This probably means that book is inserted in "
                + "collection book but not in collection book details."
            )
            # Do not try to do anything more, go back to home page
            return redirect(url_for("get_books"))

        flash('The book "{}" is successfully added'.format(book["title"]))

    return redirect(url_for("get_book", book_id=result.inserted_id))


@app.route("/delete/book/<book_id>")
def delete_book(book_id):
    """
    Remove book with id = book_id from database.
    Redirect user to home page.

    Input:
        book_id: (str) - books id in database
    """
    try:
        mongo.db.books.delete_one({"_id": ObjectId(book_id)})
        mongo.db.books_details.delete_one({"book_id": ObjectId(book_id)})
        mongo.db.reviews.delete_many({"book_id": ObjectId(book_id)})
    except Exception as e:
        flash(
            "Something went wrong when accessing database to "
            + "delete book" + e
        )
    else:
        flash("Book Successfully Deleted")
    finally:
        return redirect(url_for("get_books"))


####################
# Opinions/reviews #
####################
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
        try:
            book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
        except Exception as e:
            flash(
                "Something went wrong when accessing database to find book"
                + "that opinion should be added to. Opinion is not added", e
                )
            # Do not try to do anything more, go back to home page
            return redirect(url_for("get_books"))

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

        try:
            mongo.db.books.update_one(
                {"_id": ObjectId(book_id)}, {"$set": new_grading}
                )
        except Exception as e:
            flash(
                "Something went wrong when accessing database to update"
                + " books grading. Opinion is not added. " + e
            )
            # Do not try to do anything more, go back to home page
            return redirect(url_for("get_books"))

    else:    # Grade is not given
        grade_str = "0"

    add_review = {
        "grade": grade_str,
        "review": review,
        "added_by": session["username"],
        "book_id": ObjectId(book_id)
    }
    try:
        mongo.db.reviews.insert_one(add_review)

        mongo.db.books_details.update_one({
                "book_id": ObjectId(book_id)
            }, {"$set": get_5_reviews(book_id)
                }
        )
    except Exception as e:
        flash(
            "Something went wrong when accessing database to insert "
            + "opinion and update books details. Thus perhaps database is "
            + "is corrupt regarding opinions for current book. " + e
        )
    else:
        flash("Opinion Successfully Added")
    finally:
        return redirect(url_for("get_book", book_id=book_id))


@app.route("/change/opinion/<return_to>/<title>", methods=["GET", "POST"])
def change_opinion(return_to, title):
    """
    Read from form in page and update database with the change in opinion.
    Notice: If the grade is changed - average_grade must be recalculated.
    And if review is changed, besides collection: reviews, it might also effect
    collection: books-details that contains the five latest reviews.
    Render page according to input parameter return_to
    Input:
        return_to: (str) - Where user should be redirected
        title: (str) - Title of book
    """
    book_id = request.form.get("book_id")
    review_id = request.form.get("review_id")
    grade_str = request.form.get("grade_m")
    review = request.form.get("review_m")

    if not(review) and not(grade_str):
        flash("Something is wrong, no information retrieved")
        return redirect(url_for("get_book", book_id=book_id))

    try:
        old_review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    except Exception as e:
        flash(
            "Something went wrong when accessing database, to find old grade"
            + " and review. Opinion is not changed. " + e
        )
        # Do not try to do anything more, go back to home page
        return redirect(url_for("get_books"))

    if (old_review["grade"] != grade_str):
        grade_diff = int(grade_str) - int(old_review["grade"])
        book = mongo.db.books.find_one({"_id": ObjectId(book_id)})

        no_of_votes = int(book["no_of_votes"])

        # If old review was 0 that vote was not counted before
        if old_review["grade"] == "0":
            no_of_votes += 1

        # This should not happen but to be sure not to divide with 0
        if no_of_votes != 0:
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

    try:
        mongo.db.reviews.update_one(
            {"_id": ObjectId(review_id)}, {"$set": change_review})

        mongo.db.books_details.update_one(
            {"book_id": ObjectId(book_id)}, {"$set": get_5_reviews(book_id)})
    except Exception as e:
        flash(
            "Something went wrong when accessing database to change "
            + "opinion and update books details. Thus perhaps database is "
            + "is corrupt regarding opinions for current book. " + e
        )
    else:
        flash("Opinion Successfully Changed")
    finally:
        if (return_to == "book"):
            return redirect(url_for("get_book", book_id=book_id))
        else:
            return redirect(
                url_for("get_reviews", book_id=book_id, title=title)
            )


@app.route("/delete/opinion/<book_id>/<review_id>/<return_to>/<title>")
def delete_opinion(book_id, review_id, return_to, title):
    """
    Delete opinion, with id=review_id, from database.
    Notice: This affects the average grade for the book with id=book_id
    and it also might affect the last 5 reviews that is stored in collection:
    book_details.
    Then redirect user to page according to input parameter return_to.
    Input:
        book_id: (str) - Books id in database
        review_id: (str) - Reviews id in database
        return_to: (str) - Redirect user to this page
        title: (str) - Books title
    """
    try:
        opinion = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    except Exception as e:
        flash(
            "Something went wrong when accessing database. "
            + e
        )

    # If did not find opinion
    if not opinion:
        flash(
            "Error when deleting opinion."
        )
        return redirect(url_for("get_book", book_id=book_id))

    try:
        mongo.db.reviews.delete_one({"_id": ObjectId(review_id)})

        book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    except Exception as e:
        flash(
            "Something went wrong when accessing database to delete review. "
            + "Database is perhaps corrupt now regarding current books"
            "reviews. " + e
        )
        # Do not try to do anything more, go back to home page
        return redirect(url_for("get_books"))

    # If no grade is given, no new average is needed
    if opinion["grade"] != "0":
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
        try:
            mongo.db.books.update_one(
                {"_id": ObjectId(book_id)}, {"$set": new_grading})
        except Exception as e:
            flash(
                "Something went wrong when accessing database to update "
                + "books grading. Database is perhaps corrupt now "
                + "regarding current books reviews. " + e
            )
            # Do not try to do anything more, go back to home page
            return redirect(url_for("get_books"))

    try:
        mongo.db.books_details.update_one(
            {"book_id": ObjectId(book_id)}, {"$set": get_5_reviews(book_id)})
    except Exception as e:
        flash(
            "Something went wrong when accessing database to update "
            + "books details last 5 opinions. Database is perhaps corrupt now "
            + "regarding current books reviews. " + e
        )
        # Do not try to do anything more, go back to home page
        return redirect(url_for("get_books"))

    flash("Opinion Successfully Deleted")
    if (return_to == "book"):
        return redirect(url_for("get_book", book_id=book_id))
    else:
        return redirect(url_for("get_reviews", book_id=book_id, title=title))


@app.route("/reviews/<book_id>/<title>", methods=["GET", "POST"])
def get_reviews(book_id, title):
    """
    Get all reviews for a book with id=book_id in database.
    Render the reviews page and show retrieved information.
    Input:
        book_id: (str) - Books id in database
        title: (str) - Books title
    """
    try:
        reviews = list(mongo.db.reviews.find(
            {"book_id": ObjectId(book_id)}).sort("_id", -1)
        )
    except Exception as e:
        flash(
            "Something went wrong when accessing database to retrive reviews. "
            + e
        )
        reviews = []
    finally:
        return render_template(
            "pages/reviews.html", reviews=reviews, title=title, book_id=book_id
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
    try:
        category_groups = list(
            mongo.db.category_groups.find().sort("group_name", 1)
        )
    except Exception as e:
        flash(
            "Something went wrong when accessing database to "
            + "retrieve category groups." + e
        )
        # Go back to home page
        return redirect(url_for("get_books"))

    return render_template(
        "pages/category_groups.html", category_groups=category_groups
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
        try:
            mongo.db.category_groups.insert_one(group_name)
        except Exception as e:
            flash(
                "Something went wrong when accessing database to "
                + "add category group. Group is not added. " + e
            )
        else:
            flash(
                'New category group "{}" added'.format(
                    group_name["group_name"]
                )
            )
        finally:
            return redirect(url_for("get_category_groups"))

    return render_template("pages/category_group.html")


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

    Input:
        category_group_id: (str) - Category groups id in database
        old_group_name: (str) - Category group name to change from
    """
    if request.method == "POST":
        new_name = request.form.get("group_name")

        try:
            mongo.db.category_groups.update_one({
                "_id": ObjectId(category_group_id)}, {
                    "$set": {"group_name": new_name}
                    }
                )
        except Exception as e:
            flash(
                "Something went wrong when accessing database to update "
                + "category group. Category group is not updated. " + e
            )
            return redirect(url_for("get_category_groups"))

        # Must update books belonging to changed category group
        try:
            mongo.db.books.update_many({
                "category_group": old_group_name
                }, {
                    "$set": {"category_group": new_name}
                    })
        except Exception as e:
            flash(
                "Something went wrong when accessing database to update"
                + " books belonging to changed category group. Database might"
                + "be corrupt regarding books having unchanged category group "
                + "name. " + e
            )
        else:
            flash(
                'Category Group Succesfully Updated to "{}"'.format(new_name)
            )
        finally:
            return redirect(url_for("get_category_groups"))

    try:
        group = mongo.db.category_groups.find_one({
            "_id": ObjectId(category_group_id)})
    except Exception as e:
        flash(
            "Something went wrong when accessing database to retrieve "
            + "all category groups. " + e
        )
        # Return to home page
        return redirect(url_for("get_books"))
    else:
        return render_template(
            "pages/category_group.html", group=group, edit=True
        )


@app.route("/delete/group/<category_group_id>/<category_group>")
def delete_group(category_group_id, category_group):
    """
    Delete group in database with id=category_group_id.
    Notice that all books in this category_group is effected. Their category
    group is changed to "Other".
    User is then redirected to page with category groups.
    Input:
        category_group_id: (str) - Category groups id in databas
        category_group: (str) - Name of category group
    """
    try:
        mongo.db.category_groups.remove({"_id": ObjectId(category_group_id)})
    except Exception as e:
        flash(
            "Something went wrong when accessing database, to remove "
            + "category group. Category group is probably not removed. "
            + e
        )
        return redirect(url_for("get_category_groups"))

    # Update all affected books, to category group "Other"
    try:
        mongo.db.books.update_many({
            "category_group": category_group
            }, {
                "$set": {"category_group": "Other"}
                })
    except Exception as e:
        flash(
            "Something went wrong when accessing database to change "
            + "category groups for books affected by deletion of category"
            "group. There might exist books that belong to deleted category"
            "group. " + e
        )
    else:
        flash('Category group "{}" deleted'.format(category_group))
    finally:
        return redirect(url_for("get_category_groups"))


@app.route("/search/category", methods=["GET", "POST"])
def search_category():
    """
    Get category group from form and find the ten most popular books that
    belong to this category group.
    Then render page search_results.
    """
    category = request.form.get("category")
    try:
        category_books = list(
            mongo.db.books.find(
                {"category_group": category}
                ).sort("average_grade", -1).limit(10)
            )
    except Exception as e:
        flash(
            "Something went wrong when accessing database, to find books "
            + "that belong to the category group. " + e
        )
        # Return to home page
        return redirect(url_for("get_books"))

    if not(category_books):
        flash('No books in that category group: "{}" in database'.format(
                category))
        return redirect(url_for("get_books"))

    # The average grade is rounded before shown on page.
    for book in category_books:
        book["avg_gr_rounded"] = round(float(book["average_grade"]), 1)

    return render_template(
        "pages/search_result.html", books=category_books,
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
        try:
            existing_user = mongo.db.users.find_one(
                {"username": request.form.get("username").lower()})
        except Exception as e:
            flash(
                "Something went wrong when accessing database to sign you up! "
                + e
            )
            # Return to home page
            return redirect(url_for("get_books"))

        # If user already exists in database
        if existing_user:
            flash('Username: {}, already exists'.format(existing_user))
            return redirect(url_for("signup", login=False))

        sign_up = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "email": request.form.get("email")
        }
        try:
            mongo.db.users.insert_one(sign_up)
        except Exception as e:
            flash(
                "Something went wrong when accessing database to sign you up! "
                + e
            )
            # Return to home page
            return redirect(url_for("get_books"))

        # Put username in session-variable
        session["username"] = sign_up["username"]
        flash("Sign Up successful - Welcome, {}!".format(
            request.form.get("username")
        ))
        return redirect(url_for("get_books"))

    return render_template("pages/login.html", login=False)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Get username and password from form in page. Check that combination of user
    and password exists. If OK redirect user to home page. Otherwise user is
    returned to login page.
    """
    if request.method == "POST":
        try:
            existing_user = mongo.db.users.find_one(
                {"username": request.form.get("username").lower()}
            )
        except Exception as e:
            flash(
                "Something went wrong when accessing database to log in! "
                + e
            )
            # Return to home page
            return redirect(url_for("get_books"))

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

    return render_template("pages/login.html", login=True)


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
