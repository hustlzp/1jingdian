#-*- coding: UTF-8 -*-
from 1jingdian import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)
    author = db.Column(db.String(50), unique=True)
    intro = db.Column(db.String(50), unique=True)
    cover_image = db.Column(db.String(50), unique=True)
    amazon_url = db.Column(db.String(50), unique=True)
    douban_url = db.Column(db.String(50), unique=True)
    pub_date = db.Column(db.String(50), unique=True)
    press = db.Column(db.String(50), unique=True)
    pages_num = db.Column(db.String(50), unique=True)
    price = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return '<Book %s>' % self.title

class Excerpt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title =db.Column(db.String(50), unique=True)
    content = db.Column(db.Text())
    review = db.Column(db.String(50), unique=True)
    page_start = db.Column(db.String(50), unique=True)
    page_end = db.Column(db.String(50), unique=True)
    create_time = db.Column(db.String(50), unique=True)

    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    book = db.relationship('Book', backref=db.backref('excerpts'))

    def __repr__(self):
        return '<Excerpt %s>' % self.title