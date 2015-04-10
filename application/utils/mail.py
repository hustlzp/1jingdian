# coding: utf-8
import json
import traceback
import requests
from flask import current_app, render_template, url_for
from .helpers import absolute_url_for
from .security import encode
from ..models import db, MailLog


def send_invitation_mail(to, invitation_code):
    """发送内测邀请码到用户邮箱"""
    url = absolute_url_for('account.register', code=invitation_code)
    return send_mail(to,
                     '小流派',
                     "邀请您参与小流派内测",
                     render_template('mail/invitation.html', invitation_code=invitation_code,
                                     url=url))


def send_activate_mail(user):
    """发送激活链接到用户邮箱"""
    url = absolute_url_for('account.activate', token=encode(user.id))
    return send_mail(user.email,
                     '小流派',
                     "激活你在小流派的账号",
                     render_template('mail/activate.html', url=url))


def send_reset_password_mail(user):
    """发送密码重置链接"""
    url = absolute_url_for('account.reset_password', token=encode(user.id))
    return send_mail(user.email,
                     '小流派',
                     "密码重置",
                     render_template('mail/reset_password.html', url=url))


def send_mail(to, fromname, subject, html):
    """通用的邮件发送函数，返回成功与否"""
    config = current_app.config
    url = "http://sendcloud.sohu.com/webapi/mail.send.json"
    params = {
        "api_user": config['SC_API_USER'],
        "api_key": config['SC_API_KEY'],
        "to": to,
        "from": config['SC_FROM'],
        "fromname": fromname,
        "subject": subject,
        "html": html
    }

    try:
        r = requests.post(url, data=params)
    except Exception, e:
        log = MailLog(email=to, message=traceback.format_exc())
        db.session.add(log)
        db.session.commit()
        print(log.message)
        return False
    else:
        if r.status_code != 200:
            log = MailLog(email=to,
                          message="Do not conform to the basic sending format of SendCloud.")
            db.session.add(log)
            db.session.commit()
            print(log.message)
            return False

        result = json.loads(r.text)
        if result['message'] == 'success':
            return True
        else:
            log = MailLog(email=to, message=result['errors'].join('; '))
            db.session.add(log)
            db.session.commit()
            print(log.message)
            return False
