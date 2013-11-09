#-*- coding: UTF-8 -*-
import sys
sys.path.append('/var/www/flaskconfig/1jingdian')
import config
from flask import Flask, request, url_for, session, g
from flask.ext.sqlalchemy import SQLAlchemy

# convert python's encoding to utf8
reload(sys)
sys.setdefaultencoding('utf8')

# app
app = Flask(__name__)
app.config.update(
    SECRET_KEY=config.SECRET_KEY,
    SESSION_COOKIE_NAME=config.SESSION_COOKIE_NAME,
    PERMANENT_SESSION_LIFETIME=config.PERMANENT_SESSION_LIFETIME,
    DEBUG=config.DEBUG
)

# SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://%s:%s@%s/%s' % (config.DB_USER, config.DB_PASSWORD, config.DB_HOST, config.DB_NAME)
db = SQLAlchemy(app)

# url generator for pagination
def url_for_other_page(page):
    view_args = request.view_args.copy()
    args = request.args.copy()
    args['page'] = page
    view_args.update(args)
    return url_for(request.endpoint, **view_args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page

# before every request
@app.before_request
def before_request():
    g.user_id = session['user_id'] if 'user_id' in session else None

import log
import controllers
import models