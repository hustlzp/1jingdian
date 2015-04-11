# coding: utf-8
from flask import render_template, Blueprint, g
from ..forms import FeedbackForm
from ..models import db, Feedback
from ..utils.permissions import UserPermission

bp = Blueprint('feedback', __name__)


@bp.route('/feedback', methods=['POST', 'GET'])
@UserPermission()
def add():
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(content=form.content.data, user_id=g.user.id)
        db.session.add(feedback)
        db.session.commit()
        return render_template('site/message.html', title='提交成功',
                               message="反馈已经送达，感谢你对壹经典的支持！")
    return render_template('feedback/add.html', form=form)
