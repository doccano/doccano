import os
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.web import url


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')

    def post(self):
        pass


BASE_DIR = os.path.dirname(__file__)


def main():
    application = tornado.web.Application([
        url(r'/', IndexHandler, name='index'),
    ],
        template_path=os.path.join(BASE_DIR, 'templates'),
        static_path=os.path.join(BASE_DIR, 'static'),
    )
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get('PORT', 8080))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
