import tornado.ioloop
import tornado.web
import json
import urllib
from tornado import httpclient
from tornado import httputil

#send request to localhost:8889/drone/1
# with json file
# {
#     "event_type": "find",
#     "location": {
#         "lat": 37.42957816886063,
#         "lng": -122.08342415743255
#     },
#     "event_id": "B97B2A2A-5578-4138-AAF6-E732EB7E2EE0",
#     "drone_id": "EBD1478E-E282-11E7-801E-EC044BD6D9BE",
#     "token": "0x68aad0248835378caa1e5b2051be35a5ff1ded828786cfc",
#     "token_check_url": "https://safewrd.com/token-check",
#     "stream_url": "rtmp://90.1.34.1:8711/live"
# }


drone1_header = {'Authorization': 'Token 20fe4f04fe765cf265b81dbccd54a74303deba39', 'VehicleID': 'cAHoOyIi'}
drone2_header = {'Authorization': 'Token 84d440b0ba95c19ccd8e56a2cf0e540694798850', 'VehicleID': 'r6nRDos0'}

global_set_url = "http://dev.flytbase.com/rest/ros/flytsim/navigation/position_set_global"
take_off_url = "http://dev.flytbase.com/rest/ros/flytsim/navigation/take_off"

def takeoff(header,alt):
    body = json.dumps({"takeoff_alt": alt})
    http_client = httpclient.HTTPClient()
    response = http_client.fetch("http://dev.flytbase.com/rest/ros/flytsim/navigation/take_off", method='POST', headers=header, body=body)
    print(response.body)
    http_client.close()
    return response.body

def glob_set_pt(header,lat,lng,alt):
    body = json.dumps({
        "twist":
            {"twist":
                { "linear":{
                    "x": lat,
                    "y": lng,
                    "z": alt
                    },"angular":{
                        "z": alt
                    }
                }
            },
            "tolerance": 0.3,
            "async": True,
            "yaw_valid" : True
    })
    http_client = httpclient.HTTPClient()
    response = http_client.fetch("http://dev.flytbase.com/rest/ros/flytsim/navigation/position_set_global", method='POST', headers=header, body=body)
    print(response.body)
    http_client.close()
    return response.body


def land(header):
    http_client = httpclient.HTTPClient()
    response = http_client.fetch("http://dev.flytbase.com/rest/ros/flytsim/navigation/land", headers=header)
    print(response.body)
    http_client.close()
    return response.body




class DroneHandler(tornado.web.RequestHandler):
    def get(self, drone_id):
        if drone_id == "1":
            resp = takeoff(drone1_header,5)
            print(resp)


    def post(self,id):
        if self.request.headers["Content-Type"].startswith("application/json"):
            # if id == 1:
            self.json_args = json.loads(self.request.body)
            self.location = self.json_args['location']
            self.lat = self.location['lat']
            self.lng = self.location['lng']
            self.alt = 5.00
            # takeoff(drone1_header,self.alt)
            glob_set_pt(drone1_header,self.lat,self.lng,self.alt)
            # land(drone1_header)



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(xyz)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/drone/(.*)", DroneHandler),
    ])



if __name__ == "__main__":
    app = make_app()
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()