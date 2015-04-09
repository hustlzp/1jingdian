# coding: utf-8
from flask import render_template, Blueprint

bp = Blueprint('feedback', __name__)


@bp.route('/feedback/page/<int:page>')
@bp.route('/feedback', defaults={'page': 1})
def index(page):
    return render_template('feedback/index.html')
