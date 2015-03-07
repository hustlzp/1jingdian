# coding: utf-8
from flask import render_template, Blueprint, redirect, request, url_for
from ..forms import SigninForm, SignupForm
from ..utils.account import signin_user, signout_user
from ..utils.permissions import VisitorPermission, UserPermission
from ..models import db, User, Book

bp = Blueprint('book', __name__)


@bp.route('/')
def books():
    """All books"""
    books = Book.query
    return render_template("book/books.html", books=books)


@bp.route('/<int:uid>')
def view(uid):
    """Single book page"""
    book = Book.query.get_or_404(uid)
    return render_template("book/book.html", book=book)