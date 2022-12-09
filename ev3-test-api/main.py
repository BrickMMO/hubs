#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.iodevices import DCMotor

import urequests as requests
import json

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Initialize the EV3 Brick
ev3 = EV3Brick()

# Set volume to 100% and make a beep to signify program has started
ev3.speaker.set_volume(100)
ev3.speaker.beep()

# Turn off the light
ev3.light.off()

# Initialize EV3 touch sensor and motors
motorA = Motor(Port.A)
motorB = Motor(Port.B)
lights = DCMotor(Port.C)
touch = TouchSensor(Port.S1)

# Initialize lights
ev3.light.on(Color.RED)

# Set button vairble
touchButton = "Off"

# Create a loop to react to buttons
while True:

    # Check for center button events
    if Button.CENTER in ev3.buttons.pressed():

        motorA.stop()
        motorB.stop()
        lights.dc(0)
        ev3.light.off()
        touchButton = "Off"
        break

    
    # Make an API call to the brain settings
    # Online URL
    # res = requests.get(url='http://console.brickmmo.com/api/brain?key=OSCAR')
    # Localhost URL
    res = requests.get(url='http://192.168.1.8:8888/api/brain?key=OSCAR')

    data = json.loads(res.text)

    status = data['data']['brain']['brain_ports'][0]['settings']['status']

    print(status)    
    
    # If status is on
    if status is "on":

        motorA.dc(100)
        motorB.dc(100)
        lights.dc(100)
        ev3.light.on(Color.GREEN)
        touchButton = "On"

    # If status is off
    else:

        motorA.stop()
        motorB.stop()
        lights.dc(0)
        ev3.light.on(Color.RED)
        touchButton = "Off"

    wait(5000)

# Use the speech tool to signify the program has finished
ev3.speaker.say("Program complete")
