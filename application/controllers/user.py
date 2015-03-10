# coding: utf-8
from flask import render_template, Blueprint, redirect, request, url_for, flash, g
from ..forms import SigninForm, SignupForm
from ..utils.account import signin_user, signout_user
from ..utils.permissions import VisitorPermission, UserPermission
from ..models import db, User
from ..forms import SettingsForm

bp = Blueprint('user', __name__)


@bp.route('/people/<int:uid>')
def profile(uid):
    user = User.query.get_or_404(uid)
    return render_template('user/profile.html', user=user)


@bp.route('/people/<int:uid>/votes')
def votes(uid):
    user = User.query.get_or_404(uid)
    return render_template('user/votes.html', user=user)


@bp.route('/people/<int:uid>/likes')
def likes(uid):
    user = User.query.get_or_404(uid)
    return render_template('user/likes.html', user=user)


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
