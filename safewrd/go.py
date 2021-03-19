import tornado.ioloop
import tornado.web
import json
import urllib
import time
from tornado import httpclient
from tornado.httpclient import AsyncHTTPClient

from tornado.web import RequestHandler, asynchronous
from tornado import gen


count = 1

def update_status():
    global count
    count = count + 1
    print(count)



dron = {
    1: {'header': {
            'Authorization': 'Token 20fe4f04fe765cf265b81dbccd54a74303deba39',
            'VehicleID': 'cAHoOyIi'},
            'busy': 0,
            'location': {
                'lat': 37.42956160177652,
		        'lng': -122.08340004086494,
                'alt': 5},
            'battery' : 0
        }
    }



def takeoff(header,alt):
    body = json.dumps({"takeoff_alt": alt})
    def handle_response(response):
        if response.error:
            print("Error: %s" % response.error)
        else:
            print(response.body)

    http_client = AsyncHTTPClient()
    http_client.fetch("http://dev.flytbase.com/rest/ros/flytsim/navigation/take_off", handle_response, method='POST', headers=header, body=body)

def go(drone):
    lat = drone['location']['lat']
    lng = drone['location']['lng']
    alt = drone['location']['alt']
    header=drone['header']
    body = json.dumps({
                   "lat_x" : lat,
                   "long_y" : lng,
                   "rel_alt_z": alt,
                   "yaw": 0.0,
                   "tolerance": 0.3,
                   "async": True,
                   "yaw_valid" : True
                   })
    print(body)
    def handle_response(response):
        if response.error:
            print("Error: %s" % response.error)
        else:
            print(response.body)

    http_client = AsyncHTTPClient()
    http_client.fetch("http://dev.flytbase.com/rest/ros/flytsim/navigation/position_set_global", handle_response, method='POST', headers=header, body=body)


class DroneHandler(tornado.web.RequestHandler):
    @asynchronous
    def post(self, id):
        alt = int(id)
        global dron
        header = dron[1]['header']
        # takeoff(header,alt)
        go(dron[1])
        self.write('done')
        self.finish()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print('Hello')


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/drone/(.*)", DroneHandler),
    ])


if __name__ == "__main__":
    update_status()
    app = make_app()
    app.listen(8899)
    tornado.ioloop.PeriodicCallback(update_status, 5000).start()
    tornado.ioloop.IOLoop.current().start()
