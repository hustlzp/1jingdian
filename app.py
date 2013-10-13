from __future__ import division
import math
import os, sys
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.web import url
import torndb
import markdown2

# config
import sys
sys.path.append('/var/www/tornconfig/1jingdian')
import config

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates")
STATIC_PATH = os.path.join(os.path.dirname(__file__), "static")

# db
db = torndb.Connection(
    host=config.DB_HOST,
    database=config.DB_NAME,
    user=config.DB_USER,
    password=config.DB_PWD
)

# handles
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        """display the latest note"""
        notes = db.query("""
            select note.id, note.title, note.quote, note.page_start, note.page_end, note.create_time, book.id, book.cover_image, book.title as book_title, book.id as book_id
            from note, book
            where note.book_id = book.id
            order by note.create_time desc
        """)
        for n in notes:
            n['quote'] = n['quote'][0:115] + "..."
        self.render("index.html", notes=notes)

class NoteHandler(tornado.web.RequestHandler):
    """single note page"""
    def get(self, note_id):
        note = db.get("""
            select note.id, note.title, note.quote, note.note, note.page_start, note.page_end, note.create_time, book.id, book.cover_image, book.title as book_title, book.id as book_id, book.author
            from note, book
            where note.book_id = %d
            and note.book_id = book.id         
        """ % int(note_id))
        note['quote'] = markdown2.markdown(note['quote'])
        note['note'] = markdown2.markdown(note['note'])
        self.render("note.html", note=note)

class BooksHandler(tornado.web.RequestHandler):
    """display all the books"""
    def get(self):
        books = db.query("select * from book")  
        self.render("books.html", books=books)

class BookHandler(tornado.web.RequestHandler):
    """single book page"""
    def get(self, book_id):
        #book
        book = db.get("select * from book where id = %d" % int(book_id))
        book['intro'] = markdown2.markdown(book['intro'])

        # notes
        notes = db.query("select * from note where book_id = %d order by page_start" % int(book_id))
        for n in notes:
            n['quote'] = n['quote'][0:100] + "..."
            n['start_percentage'] = n['page_start'] * 100 / book['pages_num']
            n['width_percentage'] = ((n['page_end'] - n['page_start'] + 1) * 100 / book['pages_num'])
        self.render("book.html", book=book, notes=notes)

# app
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            url(r"/", IndexHandler, name='index'),
            url(r"/note/(\d{7})", NoteHandler, name='note'),
            url(r"/books", BooksHandler, name='books'),
            url(r"/book/(\d{7})", BookHandler, name='book')
        ]
        settings = dict(
            template_path=TEMPLATE_PATH,
            static_path=STATIC_PATH,
            debug=config.DEBUG
        )
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
    app = tornado.httpserver.HTTPServer(Application())
    app.listen(9999)
    tornado.ioloop.IOLoop.instance().start()