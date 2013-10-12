import tornado.ioloop
import tornado.web
import torndb

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates")  
STATIC_PATH = os.path.join(os.path.dirname(__file__), "static")  

db = torndb.Connection(
    host="root",
    database="1jingdian",
    user="root",
    password="xiaowangzi"
)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, ss")

class Application(tornado.web.Application):
    handlers = [
        (r"/", IndexHandler),
    ],
    settings = dict(
        template_path=TEMPLATE_PATH,
        static_path=STATIC_PATH,
        debug=True
    )
    tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
    app = tornado.httpserver.HTTPServer(Application())
    app.listen(9999)
    tornado.ioloop.IOLoop.instance().start()