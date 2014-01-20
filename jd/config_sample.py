# coding: utf-8

# IP
HOST_STRING = ''

# app config
DEBUG = True
SECRET_KEY = ""
PERMANENT_SESSION_LIFETIME = 3600 * 24 * 7
SESSION_COOKIE_NAME = '1jd_session'

# db config
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "1jingdian"
SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s/%s" % (DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

# SMTP config
SMTP_SERVER = ""
SMTP_PORT = 25
SMTP_USER = ""
SMTP_PASSWORD = ""
SMTP_FROM = ""
SMTP_ADMIN = ""
