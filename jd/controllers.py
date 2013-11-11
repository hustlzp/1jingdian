#-*- coding: UTF-8 -*-
import markdown2
from flask import render_template
from jd import app, db
from jd.models import Book, Excerpt


@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
def index(page):
    """Display the latest excerpts"""
    pagination = Excerpt.query.order_by(Excerpt.create_time.desc()).paginate(page, 1)
    excerpts = pagination.items
    return render_template("index.html", pagination=pagination, excerpts=excerpts)


@app.route('/excerpt/<int:excerpt_id>')
def excerpt(excerpt_id):
    """Single excerpt page"""
    excerpt = Excerpt.query.get_or_404(excerpt_id)
    return render_template("excerpt.html", excerpt=excerpt)


@app.route('/books')
def books():
    """All books"""
    books = Book.query.all()
    return render_template("books.html", books=books)


@app.route('/book/<int:book_id>')
def book(book_id):
    """Single book page"""
    book = Book.query.get_or_404(book_id)
    return render_template("book.html", book=book)
