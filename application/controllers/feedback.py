# coding: utf-8
from datetime import date, timedelta
from flask import render_template, Blueprint
from ..models import db, Piece
from ..utils.helper import get_pieces_data_by_day

bp = Blueprint('feedback', __name__)


@bp.route('/feedback/page/<int:page>')
@bp.route('/feedback', defaults={'page': 1})
def index(page):
    return render_template('feedback/index.html')
