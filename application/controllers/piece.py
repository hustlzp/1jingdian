# coding: utf-8
from flask import render_template, Blueprint, redirect, request, url_for
from ..forms import SigninForm, SignupForm
from ..utils.account import signin_user, signout_user
from ..utils.permissions import VisitorPermission, UserPermission
from ..models import db, User, Book, Piece

bp = Blueprint('piece', __name__)


@bp.route('/<int:uid>')
def view(uid):
    """Single piece page"""
    piece = Piece.query.get_or_404(uid)
    return render_template("piece/piece.html", piece=piece)
