import tornado.ioloop
import tornado.web

#
# To make sure everything works, create a file named “server.py” containing the following code (taken from Tornado’s site), and run it from terminal using the command “python server.py”
#
 
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
 
application = tornado.web.Application([
    (r"/", MainHandler),
])
 
if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
