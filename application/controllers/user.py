# coding: utf-8
from datetime import datetime
from flask import render_template, Blueprint, redirect, request, url_for, flash, g, json, abort
from ..utils.permissions import UserPermission
from ..utils.uploadsets import avatars, crop_image, process_image_for_cropping
from ..models import db, User, Notification
from ..forms import SettingsForm, ChangePasswordForm

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


@bp.route('/my/change_password', methods=['GET', 'POST'])
@UserPermission()
def change_password():
    """修改密码"""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        g.user.password = form.new_password.data
        db.session.add(g.user)
        db.session.commit()
        flash('密码修改成功')
        return redirect(url_for('.settings'))
    return render_template('user/change_password.html', form=form)


@bp.route('/my/upload_avatar', methods=['POST'])
@UserPermission()
def upload_avatar():
    try:
        filename, (w, h) = process_image_for_cropping(request.files['file'], avatars)
    except Exception, e:
        return json.dumps({'result': False, 'error': e.__repr__()})
    else:
        return json.dumps({
            'result': True,
            'image_url': avatars.url(filename),
            'width': w,
            'height': h
        })


@bp.route('/my/crop_avatar', methods=['POST'])
@UserPermission()
def crop_avatar():
    filename = request.form.get('filename')
    top_left_x_ratio = request.form.get('top_left_x_ratio', type=float)
    top_left_y_ratio = request.form.get('top_left_y_ratio', type=float)
    bottom_right_x_ratio = request.form.get('bottom_right_x_ratio', type=float)
    bottom_right_y_ratio = request.form.get('bottom_right_y_ratio', type=float)

    try:
        new_avatar_filename = crop_image(filename, avatars, top_left_x_ratio, top_left_y_ratio,
                                         bottom_right_x_ratio, bottom_right_y_ratio)
    except Exception, e:
        return json.dumps({'result': False, 'message': e.__repr__()})
    else:
        g.user.avatar = new_avatar_filename
        db.session.add(g.user)
        db.session.commit()
        return json.dumps({'result': True, 'image_url': avatars.url(new_avatar_filename)})


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
