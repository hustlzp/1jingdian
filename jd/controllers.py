#-*- coding: UTF-8 -*-
import markdown2
from flask import render_template
from jd import app, db
from jd.models import Book, Excerpt


@app.route('/')
def index():
    """Display the latest excerpts"""
    excerpts = Excerpt.query.all()
    return render_template("index.html", excerpts=excerpts)


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
