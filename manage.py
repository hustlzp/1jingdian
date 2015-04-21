# coding: utf-8
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from application import create_app
from application.models import db
from application.utils.assets import build
from application.utils.helpers import generate_lcs_html


# Used by app debug & livereload
PORT = 5000

app = create_app()
manager = Manager(app)

# db migrate commands
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    """Run app."""
    app.run(port=PORT)


@manager.command
def live():
    """Run livereload server"""
    from livereload import Server
    import formic

    server = Server(app)

    # css
    for filepath in formic.FileSet(include="application/static/css/**/*.css"):
        server.watch(filepath)
    # html
    for filepath in formic.FileSet(include="application/templates/css/**/*.html"):
        server.watch(filepath)
    # js
    for filepath in formic.FileSet(include="application/static/js/**/*.js"):
        server.watch(filepath)
    # image
    for filepath in formic.FileSet(include="application/static/image/**/*.*"):
        server.watch(filepath)

    server.serve(port=PORT)


@manager.command
def createdb():
    """Create database."""
    db.create_all()


@manager.command
def build_assets():
    build(app)


@manager.command
def calculate_piece_content_length():
    from application.models import Piece

    with app.app_context():
        for piece in Piece.query:
            piece.content = piece.content
            db.session.add(piece)
        db.session.commit()


@manager.command
def test():
    # src = u'ABCBDAB'
    # dest = u'BDCABA'
    # print(generate_lcs_html(src, dest))
    import re

    pattern = re.compile(r"url\([\'\"]?([^\'\"/][^\'\"\)]+)[\'\"]?\)")
    for match in pattern.finditer(
            'backurl("../dsada")ground: #ffffff url("/Jcrop.gif");font-size: 0;url("dsada")'):
        full = match.group(0)
        inner_url = match.group(1)
        print("%s, %s" % full, inner_url)


if __name__ == "__main__":
    manager.run()
