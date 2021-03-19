from aiohttp import web
import aiohttp
import asyncio
import time 
from mavsdk import System
from mavsdk import (MissionItem)
import functools

api_url = 'https://api.tranzmt.it/ws-mission/mission/{}/position'

loop = asyncio.get_event_loop()
drone = System()
loop.run_until_complete(drone.connect(system_address="udp://:14540"))

missions = dict()
has_landed = False
# def schedule_func(func, args=None, kwargs=None, interval=60, *, loop):
#     if args is None:
#         args = []
#     if kwargs is None:
#         kwargs = {}

#     async def periodic_func():
#         while True:
#             await func(*args, **kwargs)
#             await asyncio.sleep(interval, loop=loop)

#     return loop.create_task(periodic_func())

# create_scheduler = lambda loop: functools.partial(schedule_func, loop=loop)

async def _update_progress(data, start_mission):
    loop = asyncio.get_event_loop()
    while True:
        print('go...', time.time())
        _elapsed = int((time.time() - start_mission)) or 1    
        elapsed_payload = { 'user_id': data.get('user_id'), 'mission_id': data.get('eos_mission_id'), 'elapsed_sec': _elapsed }
        print('ELAPSED', str(elapsed_payload))
        async with aiohttp.ClientSession(loop=loop) as session:
            async with session.post('https://air.eosrio.io/api/update', json=elapsed_payload) as resp:
                json = await resp.json()
                print(json)
                if json.get('status') == 'ERROR':

                    print('MISSION HAS ENDED')
                    return
                    
        await asyncio.sleep(5)     
        
async def print_altitude(data):
    """ Prints the altitude """

    previous_altitude = None
    p_lat = None
    p_lng = None
    _t = time.time()
    async for position in drone.telemetry.position():
        if has_landed:
            print('returning because it has landed')
            return
        altitude = round(position.relative_altitude_m)
        latitude = position.latitude_deg
        longitude = position.longitude_deg
        if time.time() - _t < 1.5:
            continue
        _t = time.time()
        if p_lat != latitude or p_lng != longitude:
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url.format(data.get('mission_id')),json={'location':{ 'lat':latitude, 'lng': longitude}} ) as response:
                    try:
                        print(await response.json())
                    except Exception as inst:
                        print(inst)

            previous_altitude = altitude
            p_lat = latitude
            p_lng = longitude
            print(f"Altitude: {altitude}")
            print(f"Lat: {latitude}")
            print(f"Lon: {longitude}")        
        
async def _take_off_and_land(drone):

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok:
            print("Global position estimate ok")
            break

    print(f"-- Arming")        
    await drone.action.arm()
    print(f"-- Armed")            

    print(f"-- Taking off")    
    await drone.action.takeoff()
    print(f"-- Took off")

    await asyncio.sleep(5)

    print(f"-- Landing")
    await drone.action.land()
    print(f"-- Landed")
    
async def print_mission_progress(data, start_mission):
    loop = asyncio.get_event_loop()
    # periodic_updater_task = loop.create_task(_update_progress(data, start_mission))
    # asyncio.ensure_future(periodic_updater_task)
    
    asyncio.ensure_future(_update_progress(data, start_mission)) 

    # schedule = create_scheduler(loop=loop)
    # periodic_updater_task = schedule(_update_progress(data, start_mission), interval=1)
    
    # _elapsed = int((time.time() - start_mission)) or 1    
    # elapsed_payload = { 'user_id': data.get('user_id'), 'mission_id': data.get('eos_mission_id'), 'elapsed_sec': _elapsed }
    # print('ELAPSED', str(elapsed_payload))
    # async with aiohttp.ClientSession(loop=loop) as session:                
    #     async with session.post('https://air.eosrio.io/api/update', json=elapsed_payload) as resp:
    #         print(await resp.json())
    
    async for mission_progress in drone.mission.mission_progress():
        print(f"Mission progress: {mission_progress.current_item_index}/{mission_progress.mission_count}")
        if mission_progress.current_item_index == mission_progress.mission_count: # mission has ended
            async with aiohttp.ClientSession(loop=loop) as session:
                #periodic_updater_task.cancel()
                _elapsed = int((time.time() - start_mission)) or 1                
                elapsed_payload = { 'user_id': data.get('user_id'), 'mission_id': data.get('eos_mission_id'), 'elapsed_sec': _elapsed }
                print('[end] ELAPSED', str(elapsed_payload))                
                async with session.post('https://air.eosrio.io/api/update', json=elapsed_payload) as resp:
                    print(await resp.json())

                # unstake                
                unstake_payload = { 'user_id': data.get('user_id'), 'action_name' : 'unstake', 'data': { 'owner': data.get('eos_owner'), 'quantity': "{:.4f} AIR".format(300 - _elapsed - 1)}}
                print('UNSTAKE', str(unstake_payload))
                async with session.post('https://air.eosrio.io/api/action', json=unstake_payload) as resp:
                    print(await resp.json())
                    
                completion_payload = { 'user_id': data.get('user_id'), 'mission_id': data.get('eos_mission_id'), 'billed_time': _elapsed }
                print('COMPLETION', str(completion_payload))                    
                async with session.post('https://air.eosrio.io/api/complete', json=completion_payload) as resp:
                    print(await resp.json())
    
    
async def _mission(drone, lat, lng, wait):
    mission_items = []
    mission_items.append(MissionItem(lat, lng, 10, 60, True, 0, 0, MissionItem.CameraAction.TAKE_PHOTO, 5, float('nan')))

    await drone.mission.set_return_to_launch_after_mission(True)

    await drone.mission.upload_mission(mission_items)
    print(f"-- Uploaded missions")

    await drone.action.arm()
    print(f"-- Armed")

    await drone.mission.start_mission()
    print(f"-- Mission has started")
    has_landed = False

async def _update_mission(drone, lat, lng, wait=5):
    mission_items= []
    mission_items.append(MissionItem(lat, lng, 10, 60, True, 0, 0, MissionItem.CameraAction.TAKE_PHOTO, wait, float('nan')))

    await drone.mission.set_return_to_launch_after_mission(True)

    print(f"-- UPDATE mission")
    await drone.mission.upload_mission(mission_items)

    print(f"-- START mission after UPDATE")        
    await drone.mission.start_mission()
    

    
    
async def take_off_and_land(request):
    asyncio.ensure_future(_take_off_and_land(drone))
    return  web.Response(text='OK')        

async def observe_is_in_air(data):
    """ Monitors whether the drone is flying or not and
    returns after landing """

    was_in_air = False

    async for is_in_air in drone.telemetry.in_air():
        if is_in_air:
            was_in_air = is_in_air

        if was_in_air and not is_in_air:
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url.format(data.get('mission_id')),json={'landed': 1} ) as response:
                    has_landed = True
                    print(await response.json())

            await asyncio.get_event_loop().shutdown_asyncgens()
            return


async def mission(request):
    data = await request.json()
    print(str(data))
    mission_location = data.get('mission_location')
    start_mission_time = time.time()
    asyncio.ensure_future(_mission(drone, mission_location.get('lat'), mission_location.get('lng'), data.get('mission_wait')))
    asyncio.ensure_future(print_mission_progress(data, start_mission_time))
    asyncio.ensure_future(print_altitude(data))
#    asyncio.get_event_loop().run_until_complete(observe_is_in_air(data))
    asyncio.ensure_future(observe_is_in_air(data))
    return  web.Response(text='OK')

async def update_mission(request):
    #return web.Response(text='UPDATED')      
    data = await request.json()
    print(str(data))
    if not has_landed:
        asyncio.ensure_future(_update_mission(drone, data.get('lat'), data.get('lng')))
    return web.Response(text='UPDATED')     


app = web.Application()
app.add_routes([web.get('/example', take_off_and_land),
                web.post('/mission', mission),
                web.put('/mission', update_mission),])


web.run_app(app, port=8888)
