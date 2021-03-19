import tornado.ioloop
import tornado.web
import json

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, Pratap")



class DroneHandler(tornado.web.RequestHandler):
    def get(self, droneId):
        self.write(droneId)

    def post(self,id):
        if self.request.headers["Content-Type"].startswith("application/json"):
            self.json_args = json.loads(self.request.body)
            self.write(id + ' ' + self.json_args["x"])
        else:
            self.json_args = None





def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/drone/(.*)", DroneHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()