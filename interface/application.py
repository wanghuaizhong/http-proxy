# -*- coding: utf-8 -*-

import torndb
import tornado.httpserver
import tornado.web
import tornado.ioloop
import tornado.options

from tornado.options import define, options

define("port", default=8888, help="run port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="db host")
define("mysql_database", default="proxy", help="db name")
define("mysql_user", default="test", help="db user")
define("mysql_password", default="123456", help="db password")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/proxy/(\d+)", Index2Handler),
        ]

        tornado.web.Application.__init__(self, handlers)

        self.db = torndb.Connection(
            host=options.mysql_host,
            database=options.mysql_database,
            user=options.mysql_user,
            password=options.mysql_password
        )


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        db = self.application.db
        proxys = db.query("select ip, port from proxys where status = 1 limit 100")
        if proxys:
            ret_list = []
            for proxy in proxys:
                ret_list.append('%s:%s' % (proxy['ip'], proxy['port']))
            self.write('\n'.join(ret_list))
        else:
            self.write('no proxys...')


class Index2Handler(tornado.web.RequestHandler):
    def get(self, numbers):
        db = self.application.db
        proxys = db.query("select ip, port from proxys where status = 1 order by last_check_time desc limit %s" % numbers)
        if proxys:
            ret_list = []
            for proxy in proxys:
                ret_list.append('%s:%s' % (proxy['ip'], proxy['port']))
            self.write('\n'.join(ret_list))
        else:
            self.write('no proxys...')


def main():
    tornado.options.parse_command_line()
    app = tornado.httpserver.HTTPServer(Application())
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
