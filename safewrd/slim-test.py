import tornado.ioloop
import tornado.web
import json
from time import time
from datetime import datetime
from tornado.httpclient import AsyncHTTPClient
from tornado.web import asynchronous
from tornado import gen
from math import radians, cos, sin, asin, sqrt



# url : localhost:8899/drone/1

# {
# 	"lat":37.430,
# 	"lng":-122.084,
# 	"alt":5,
# 	"wait_time":30
# }


count = 0


def start_stream(drone):
    header = drone['header']
    print('Starting streaming...')    
    url = 'https://dev.flytbase.com/rest/ros/flytsim/video_streaming/start_raspicam_stream',
    body=json.dumps({"image_width": 0,
                     "image_height": 0,
                     "framerate": 0,
                     "brightness": 0,
                     "saturation": 0,
                     "flip": True,
                     "remote_url": drone['stream_url'],
                     "remote_target": True})
    print body
    def stream_start_response(response):
        print (response)
        if response.error:
            print("Stream start Error: %s" % response.error)
        else:
            print('Streaming started...')
    http_client = AsyncHTTPClient()
    http_client.fetch(url, stream_start_response, method='POST', headers=header, body=body, request_timeout=180.0)

def stop_stream(drone):
    header = drone['header']
    print('Stopping streaming...')
    url = 'https://dev.flytbase.com/rest/ros/flytsim/video_streaming/stop_raspicam_stream'
    def stream_stop_response(response):
        print (response.body)
        if response.error:
            print("Stream stop Error: %s" % response.error)
        else:
            print('Streaming Stoped...')
    http_client = AsyncHTTPClient()
    http_client.fetch(url, stream_stop_response, method='GET', headers=header, request_timeout=180.0)


def takeoff(drone):
    # print (header)
    body = json.dumps({"takeoff_alt": drone['alt']})
    print (body)
    def handle_response(response):
        print ('Takeoff response: ' + response.body)
        if response.error:
            print("Error: %s" % response.error)
        else:
            print('End take off', response.body)
            print('Going to mission')
            drone['going_to'] = 'Mission';
            go(drone)

    http_client = AsyncHTTPClient()
    http_client.fetch("http://dev.flytbase.com/rest/ros/flytsim/navigation/take_off", handle_response, method='POST', headers=drone['header'], body=body)


def go(drone):
    body = json.dumps({
                   "lat_x" : drone['mission_location']['lat'],
                   "long_y" : drone['mission_location']['lng'],
                   "rel_alt_z": drone['alt'],
                   "yaw": 0.0,
                   "tolerance": 2.0,
                   "async": False,
                   "yaw_valid": True
                   })
    print('GO body ' + body)

    @gen.engine
    def go_handle_response(response):
        if response.error:
            print("[GO] Error: %s" % response.error)
            go(drone)
        else:
            print("[GO] RESP:" + response.body, datetime.now().isoformat() )
            resp = json.loads(response.body)
            if resp['success'] == False or resp['message'].find('UnSuccessful') >= 0:
                if drone['going_to'] == 'Mission':
                    print ('time out but continue to mission')
                    go(drone)
                else:
                    print('going to ', drone['going_to'])
            elif resp['success'] == True:
                print('Reached to Mission Point')
                wait_time = int(drone['mission_wait'])
                print('Wait for sec : ', wait_time,datetime.now().isoformat())
                yield gen.sleep(wait_time)
                drone['going_to'] = 'Home'
                print ("Mission Complete Returning to home", datetime.now().isoformat())
                stop_stream(drone)
                go_home(drone)


    http_client = AsyncHTTPClient()
    print('GO request', datetime.now().isoformat())
    http_client.fetch("http://dev.flytbase.com/rest/ros/flytsim/navigation/position_set_global", go_handle_response, method='POST', headers=drone['header'], body=body, request_timeout=240.)


def go_home(drone):
    body = json.dumps({
                   "lat_x" : drone["home_location"]['lat'],
                   "long_y" : drone["home_location"]['lng'],
                   "rel_alt_z": 5.00,
                   "yaw": 0.0,
                   "tolerance": 2.0,
                   "async": False,
                   "yaw_valid": True
                   })
    print('going home', body)
    def go_home_handle_response(response):
        if response.error:
            print("Error: %s" % response.error, "GO HOME")
            go_home(drone)
        else:
            print("GO HOME RESP", response.body, datetime.now().isoformat())
            resp = json.loads(response.body)
            if resp['success'] == False:
                if drone['going_to'] == 'Home':
                    print ('time out but continue to Home')
                    go_home(drone)
                else:
                    print('going to ', drone['going_to'])
            if resp['success'] == True:
                print('Reached at home, Landing...')
                land(drone)

    http_client = AsyncHTTPClient()
    print('sending the go_home request', datetime.now().isoformat())           
    http_client.fetch("http://dev.flytbase.com/rest/ros/flytsim/navigation/position_set_global", go_home_handle_response, method='POST', headers=drone['header'], body=body, request_timeout=240.)


def land(drone):
    body = json.dumps({"async": False})
    def land_resp(response):
        print(response.body)
        print('Mission Completed')
    http_client = AsyncHTTPClient()
    http_client.fetch("http://dev.flytbase.com/rest/ros/flytsim/navigation/land", land_resp, method='POST', headers=drone['header'], body=body)


class DroneHandler(tornado.web.RequestHandler):
    @asynchronous
    def post(self):
        print 'HERE'
        drone = json.loads(self.request.body)
        drone['header']  = {
            'Authorization': 'Token ' + drone['access_token'],
            'VehicleID': drone['vehicle_id']
        }
        print drone
        start_stream(drone)
        takeoff(drone)
        response = {'success': 1, 'drone': drone}
        self.write(response)
        self.finish()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print('Welcome to Flytbase')
        self.write("Welcome to Flytbase\n")
        self.finish()



def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/mission", DroneHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8899)
    tornado.ioloop.IOLoop.current().start()
