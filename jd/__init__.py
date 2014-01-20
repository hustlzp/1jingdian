# coding: utf-8
import sys
from flask import Flask, request, url_for, render_template
from flask_wtf.csrf import CsrfProtect
from . import config

# convert python's encoding to utf8
reload(sys)
sys.setdefaultencoding('utf8')


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # CSRF protect
    CsrfProtect(app)

    register_db(app)
    register_routes(app)
    register_jinja(app)
    register_error_handle(app)
    register_logger(app)
    register_uploadsets(app)

    @app.before_request
    def before_request():
        pass

    return app


def register_jinja(app):
    from . import filters
    app.jinja_env.filters['markdown'] = filters.markdown

    # inject vars into template context
    @app.context_processor
    def inject_vars():
        return dict()

    # url generator for pagination
    def url_for_other_page(page):
        view_args = request.view_args.copy()
        args = request.args.copy().to_dict()
        args['page'] = page
        view_args.update(args)
        return url_for(request.endpoint, **view_args)

    app.jinja_env.globals['url_for_other_page'] = url_for_other_page


def register_logger(app):
    """Send error log to admin by smtp"""
    if not app.debug:
        import logging
        from logging.handlers import SMTPHandler
        credentials = (config.SMTP_USER, config.SMTP_PASSWORD)
        mail_handler = SMTPHandler((config.SMTP_SERVER, config.SMTP_PORT), config.SMTP_FROM,
                                   config.SMTP_ADMIN, '1jd-log', credentials)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


def register_db(app):
    from .models import db
    db.init_app(app)


def register_routes(app):
    from .models import Book, Excerpt

    @app.route('/', defaults={'page': 1})
    @app.route('/page/<int:page>')
    def index(page):
        """Display the latest excerpts"""
        paginator = Excerpt.query.order_by(Excerpt.create_time.desc()).paginate(page, 12)
        return render_template("index.html", paginator=paginator)

    @app.route('/excerpt/<int:excerpt_id>')
    def excerpt(excerpt_id):
        """Single excerpt page"""
        excerpt = Excerpt.query.get_or_404(excerpt_id)
        return render_template("excerpt.html", excerpt=excerpt)

    @app.route('/books')
    def books():
        """All books"""
        books = Book.query
        return render_template("books.html", books=books)

    @app.route('/book/<int:book_id>')
    def book(book_id):
        """Single book page"""
        book = Book.query.get_or_404(book_id)
        return render_template("book.html", book=book)


def register_error_handle(app):
    @app.errorhandler(403)
    def page_403(error):
        return render_template('403.html'), 403

    @app.errorhandler(404)
    def page_404(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def page_500(error):
        return render_template('500.html'), 500


def register_uploadsets(app):
    # from .uploadsets import workimages
    # configure_uploads(app, (workimages))
    pass

app = create_app()