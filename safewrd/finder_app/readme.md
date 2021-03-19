To run the application


cd safewrd/finder_app
python main_activity.py

Wait for the app to initialize and drones to be connected. If no drones from the list are available
then app will gracefully shutdown.


Creating a new session/mission:

python test_script.py
(this will return a session id), e.g, S0015168190028796


Trying remote access during active session/mission:
i. this will work only when drone is waiting at POI location,
ii. only one request will be served at a time.
iii. Each request will keep the drone access locked for 10 sec after command execution.
     During this time no other request will be entertained.
iv. Send session ID as argument for following test script.


python test_remote_access.py S0015168190028796