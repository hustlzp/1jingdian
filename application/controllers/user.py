# coding: utf-8
from datetime import datetime
from flask import render_template, Blueprint, redirect, request, url_for, flash, g, json
from ..utils.permissions import UserPermission
from ..utils.uploadsets import avatars, process_avatar
from ..models import db, User, Notification
from ..forms import SettingsForm

bp = Blueprint('user', __name__)


@bp.route('/people/<int:uid>', defaults={'page': 1})
@bp.route('/people/<int:uid>/page/<int:page>')
def profile(uid, page):
    user = User.query.get_or_404(uid)
    votes = user.voted_pieces.paginate(page, 20)
    return render_template('user/profile.html', user=user, votes=votes)


@bp.route('/people/<int:uid>/share', defaults={'page': 1})
@bp.route('/people/<int:uid>/share/page/<int:page>')
def share(uid, page):
    user = User.query.get_or_404(uid)
    pieces = user.pieces.paginate(page, 20)
    return render_template('user/share.html', user=user, pieces=pieces)


@bp.route('/people/<int:uid>/likes', defaults={'page': 1})
@bp.route('/people/<int:uid>/likes/page/<int:page>')
def likes(uid, page):
    user = User.query.get_or_404(uid)
    collections = user.liked_collections.paginate(page, 20)
    return render_template('user/collections.html', user=user, collections=collections)


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


@bp.route('/my/notifications', defaults={'page': 1})
@bp.route('/my/notifications/page/<int:page>')
@UserPermission()
def notifications(page):
    notifications = g.user.notifications.paginate(page, 15)
    return render_template('user/notifications.html', notifications=notifications)


@bp.route('/my/notification/<int:uid>/check')
@UserPermission()
def check_notification(uid):
    notification = Notification.query.get_or_404(uid)
    notification.checked = True
    notification.checked_at = datetime.now()
    db.session.add(notification)
    db.session.commit()
    return redirect(notification.link)


@bp.route('/my/notifications/check', methods=['POST'])
@UserPermission()
def check_all_notifications():
    notifications = g.user.notifications.filter(~Notification.checked)
    for notification in notifications:
        notification.checked = True
        notification.checked_at = datetime.now()
        db.session.add(notification)
    db.session.commit()
    return json.dumps({'result': True})
