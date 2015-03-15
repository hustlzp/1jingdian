# coding: utf-8
from flask import render_template, Blueprint, redirect, request, url_for, flash, g, json
from ..utils.permissions import UserPermission
from ..utils.uploadsets import avatars, process_avatar
from ..models import db, User
from ..forms import SettingsForm

bp = Blueprint('user', __name__)


@bp.route('/people/<int:uid>', defaults={'page': 1})
@bp.route('/people/<int:uid>/page/<int:page>')
def profile(uid, page):
    user = User.query.get_or_404(uid)
    pieces = user.created_pieces.paginate(page, 20)
    return render_template('user/profile.html', user=user, pieces=pieces)


@bp.route('/people/<int:uid>/votes', defaults={'page': 1})
@bp.route('/people/<int:uid>/votes/page/<int:page>')
def votes(uid, page):
    user = User.query.get_or_404(uid)
    votes = user.voted_pieces.paginate(page, 20)
    return render_template('user/votes.html', user=user, votes=votes)


@bp.route('/people/<int:uid>/collections')
def collections(uid):
    user = User.query.get_or_404(uid)
    return render_template('user/collections.html', user=user)


@bp.route('/my/settings', methods=['GET', 'POST'])
@UserPermission()
def settings():
    """个人设置"""
    form = SettingsForm(obj=g.user)
    if form.validate_on_submit():
        form.populate_obj(g.user)
        db.session.add(g.user)
        db.session.commit()
        flash('设置已保存')
        return redirect(url_for('.settings'))
    return render_template('user/settings.html', form=form)


@bp.route('/upload_avatar', methods=['POST'])
@UserPermission()
def upload_avatar():
    try:
        filename = process_avatar(request.files['file'], avatars, 160)
    except Exception, e:
        return json.dumps({'result': False, 'error': e.__repr__()})
    else:
        g.user.avatar = filename
        db.session.add(g.user)
        db.session.commit()
        return json.dumps({'result': True, 'avatar_url': avatars.url(filename)})
