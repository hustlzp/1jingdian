from flask import render_template
from jd import app, db
import markdown2


@app.route('/')
def index():
    """Display the latest excerpts"""
    notes = db.query("""
        select note.id, note.title, note.quote, note.page_start, note.page_end, note.create_time, book.cover_image, book.title as book_title, book.id as book_id
        from note, book
        where note.book_id = book.id
        order by note.create_time desc
    """)
    for n in notes:
        n['quote'] = n['quote'][0:115] + "..."
    render_template("index.html", notes=notes)


@app.route('/excerpt/<int:excerpt_id>')
def excerpt(excerpt_id):
    """Single excerpt page"""
    excerpt = db.get("""
        select note.id, note.title, note.quote, note.note, note.page_start, note.page_end, note.create_time, book.id, book.cover_image, book.title as book_title, book.id as book_id, book.author
        from note, book
        where note.id = %d
        and note.book_id = book.id
    """ % excerpt_id)
    excerpt['quote'] = markdown2.markdown(excerpt['quote'])
    excerpt['note'] = markdown2.markdown(excerpt['note'])
    render_template("excerpt.html", excerpt=excerpt)


@app.route('/books')
def books():
    """All books"""
    books = db.query("select * from book")
    render_template("books.html", books=books)


@app.route('/book/<int:book_id>')
def book(book_id):
    """Single book page"""
    # book
    book = db.get("select * from book where id = %d" % int(book_id))
    book['intro'] = markdown2.markdown(book['intro'])

    # notes
    notes = db.query("select * from note where book_id = %d order by page_start" % book_id)
    for n in notes:
        n['quote'] = n['quote'][0:100] + "..."
        n['start_percentage'] = n['page_start'] * 100 / book['pages_num']
        n['width_percentage'] = (n['page_end'] - n['page_start'] + 1) * 100 / book['pages_num']
    render_template("book.html", book=book, notes=notes)
