import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket

# http://niltoid.com/blog/raspberry-pi-arduino-tornado/
# Adding websockets to your Tornado app is easy. Below is the modified version of server.py. It also includes support for command line arguments on line 8 (so you can run the program using “python server.py –port=8080″).
# And here is the corresponding index.html, which connects to the websocket server. I used KineticJS to quickly create a simple red circle on a canvas which listens from click events.  Be sure that your “ws://” url is correct.
#
#
#
 
from tornado.options import define, options
define("port", default=8080, help="run on the given port", type=int)
 
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')
 
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'new connection'
        self.write_message("connected")
 
    def on_message(self, message):
        print 'message received %s' % message
        self.write_message('message received %s' % message)
 
    def on_close(self):
        print 'connection closed'
 
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler),
            (r"/ws", WebSocketHandler)
        ]
    )
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.listen(options.port)
    print "Listening on port:", options.port
    tornado.ioloop.IOLoop.instance().start()
