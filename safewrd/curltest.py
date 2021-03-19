import tornado.ioloop
import tornado.web
import json
import urllib
from tornado import httpclient
from tornado import httputil

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
        http_client = httpclient.HTTPClient()
        headers = {'Authorization': 'Token 20fe4f04fe765cf265b81dbccd54a74303deba39', 'VehicleID': 'cAHoOyIi'}
        try:
            response = http_client.fetch("http://dev.flytbase.com/rest/ros/flytsim/navigation/arm", headers=headers)
            # response = http_client.fetch("http://dev.flytbase.com/rest/ros/flytsim/navigation/arm", method='POST', headers=headers, body=body)
            print(response.body)
        except httpclient.HTTPError as e:
            # HTTPError is raised for non-200 responses; the response
            # can be found in e.response.
            print("Error: " + str(e))
        except Exception as e:
            # Other errors are possible, such as IOError.
            print("Error: " + str(e))
        http_client.close()


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()