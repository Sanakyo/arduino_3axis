import pyfirmata as pf
import time

arduino = pf.Arduino('/dev/ttyACM0')
servos = [arduino.get_pin('d:4:s'), arduino.get_pin('d:3:s'), arduino.get_pin('d:2:s')]
servoNames = ["Bottom Servo", "Middle Servo", "Top Servo"]
defaultServoDegrees = [50, 90, 180]

for index, servo in enumerate(servos):
    servo.write(defaultServoDegrees[index])
time.sleep(1)
print("Servos set to default position. (50, 90, 180)")

while True:
    prompt = input("Enter a command: ")
    if prompt is not None:
        for index, degree in enumerate(prompt.split(" ")):
            servos[index].write(int(degree))
            print(servoNames[index] + ": " + degree + " ", end="")
        print()
        time.sleep(1)
