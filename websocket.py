import asyncio
import websockets
import pyfirmata as pf
import time
import json

port = 3456
arduino = pf.Arduino('/dev/ttyACM0')
servos = [arduino.get_pin('d:4:s'), arduino.get_pin('d:3:s'), arduino.get_pin('d:2:s')]
servoNames = ["Bottom Servo", "Middle Servo", "Top Servo"]
defaultServoDegrees = [50, 90, 140]

for index, servo in enumerate(servos):
    servo.write(defaultServoDegrees[index])
time.sleep(1)
print(f"Servos set to default position. ({defaultServoDegrees[0]}, {defaultServoDegrees[1]}, {defaultServoDegrees[2]})")

async def send_json(websocket, data):
    await websocket.send(json.dumps(data))

async def accept(websocket, path):
    await send_json(websocket, { "op": "HELLO", "axis": [ s.read() for s in servos ] }) 
    while True:
        data = await websocket.recv()
        print("RECV: " + data)
        packet = json.loads(data)
        await act(websocket, packet)
        
async def act(websocket, data):
    if data["op"] == "SET":
        for index, degree in enumerate(data["axis"]):
            servos[index].write(degree)
        await send_json(websocket, {"op": "ACK", "axis": [ s.read() for s in servos ] })
    if data["op"] == "RESET":
        for index, servo in enumerate(servos):
            servo.write(defaultServoDegrees[index])
        await send_json(websocket, {"op": "HELLO", "axis": [ s.read() for s in servos ] })
            

start_server = websockets.serve(accept, "0.0.0.0", port)
print("Start websocket server on " + str(port))
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
