import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from data_models import db, Author, Book


SORTING_OPTIONS = {
    "Book Title": "title",
    "Author Name": "author.name",
    "ISBN": "isbn",
    "Book ID": "id",
}

sort_by = SORTING_OPTIONS["Book Title"]

# Ensure 'data' directory exists
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

app = Flask(__name__)
db_path = os.path.join(data_dir, "library.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

db.init_app(app)


# Create Flask routes
@app.route("/")
def home():
    """
    Show the home page
    :return: HTML template
    """
    global sort_by
    sort_by = request.args.get("sort", sort_by)
    if sort_by not in SORTING_OPTIONS.values():
        sort_by = SORTING_OPTIONS["Book Title"]
    title_search = request.args.get("search")

    if title_search:
        books = Book.query.filter(Book.title.contains(title_search)).all()
    else:
        books = Book.query.all()

    return render_template(
        "home.html", books=books, sort_by=sort_by, sorting_options=SORTING_OPTIONS
    )


@app.route("/add_author", methods=["GET"])
def show_add_author():
    """
    Show the add author template
    :return: HTML template
    """
    return render_template("add_author.html")


@app.route("/add_author", methods=["POST"])
def add_author():
    """
    Add an author to the database
    :return: HTML template
    """
    author_name = request.form.get("name")
    birthdate = request.form.get("birthdate")
    date_of_death = request.form.get("date_of_death")

    if not author_name:
        # If no author name is provided, return a json response and an invalid request status code
        return {"error": "Author name is required"}, 400
    if not birthdate:
        # If no birth date is provided, return a json response and an invalid request status code
        return {"error": "Birth date is required"}, 400

    birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
    if date_of_death:
        date_of_death = datetime.strptime(date_of_death, "%Y-%m-%d")
    else:
        date_of_death = None

    author = Author(name=author_name, birth_date=birthdate, date_of_death=date_of_death)
    db.session.add(author)
    db.session.commit()

    # Redirect to the home page
    return redirect(url_for("home"))


@app.route("/add_book", methods=["GET"])
def show_add_book():
    """
    Show the add book template
    :return: HTML template
    """
    authors = Author.query.all()
    return render_template("add_book.html", authors=authors)


@app.route("/add_book", methods=["POST"])
def add_book():
    """
    Add a book to the database
    :return: HTML template
    """
    title = request.form.get("title")
    isbn = request.form.get("isbn")
    author_id = request.form.get("author_id")

    if not title:
        # If no title is provided, return a json response and an invalid request status code
        return {"error": "Title is required"}, 400
    if not author_id:
        # If no author id is provided, return a json response and an invalid request status code
        return {"error": "Author id is required"}, 400

    book = Book(title=title, isbn=isbn, author_id=author_id)
    db.session.add(book)
    db.session.commit()

    # Redirect to the home page
    return redirect(url_for("home"))


@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    """
    Delete a book from the database
    :param book_id: The book id
    :return: HTML template
    """
    book = Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()

    # Redirect to the home page
    return redirect(url_for("home"))


@app.route("/remove_author", methods=["GET"])
def show_remove_author():
    """
    Show the remove author template
    :return: HTML template
    """
    authors = Author.query.all()
    return render_template("remove_author.html", authors=authors)


@app.route("/remove_author", methods=["POST"])
def remove_author():
    """
    Remove an author from the database
    :return: HTML template
    """
    author_id = request.form.get("author_id")

    if not author_id:
        # If no author id is provided, return a json response and an invalid request status code
        return {"error": "Author id is required"}, 400

    author = Author.query.get(author_id)
    for book in author.books:
        db.session.delete(book)
    db.session.delete(author)
    db.session.commit()

    # Redirect to the home page
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)

    # with app.app_context():
    #     db.create_all()
