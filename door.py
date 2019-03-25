# main class for actual work with main GPIO and raspberry pi perytherals
import RPi.GPIO as GPIO     ## Import GPIO library
import time
import os
import sys
import json

class Door(object):
    """docstring for door."""

    def __init__(self, session):
        self.DOOR_STATE = None  # the main variable for door state -- due to internall sensor o so
        self._SESSION = session
        self.initDoor()

    def sensorChange(self, foo):
        self.getDoorState()
        print(self._SESSION)
        dt = {'action':'door-action', 'status': self.DOOR_STATE}
        try:
            self._SESSION.manager.broadcast(json.dumps(dt))
        except Exception as e:
            print(e)
            print('no ta straca se stala tady dopice kurvaaaa')

    def initDoor(self):
        #   initialize door, get actual status of the door and set function for state changes due to hall sensor
        GPIO.setmode(GPIO.BCM) ## Use board pin numbering
        #pins are pulled up because the reed switches are ON by default.
        GPIO.setup(18, GPIO.IN) # hall sensor setup
        GPIO.setup(14, GPIO.OUT)
        self.servo = GPIO.PWM(14, 50)  # pin 18, and 50 Hz
        
        self.getDoorState()
        self.servo.start(7.5) # set to neutral position - 7.5% duty cycle
        time.sleep(0.1)
        self.servo.ChangeDutyCycle(0)
        # set initial combination due to door state
        if self.DOOR_STATE:
            self.lock()
        else:
            self.unlock()

        # on update event
        GPIO.add_event_detect(18, GPIO.BOTH, callback=self.sensorChange)

    def getDoorState(self):
        self.DOOR_STATE = GPIO.input(18) # True means locked, False mens unlocked

    def lock(self):
        self.getDoorState()
        if self.DOOR_STATE:
            return True
        self.servo.ChangeDutyCycle(0.1)
        time.sleep(.1)
        self.servo.ChangeDutyCycle(0)
        time.sleep(1)
        self.getDoorState()

    def unlock(self):
        if not self.DOOR_STATE:
            return True
        self.servo.ChangeDutyCycle(22)
        time.sleep(.1)
        self.servo.ChangeDutyCycle(0)
        time.sleep(1)
        self.getDoorState()

    def onexit(self):
        self.servo.stop
        time.sleep(0.5)
        GPIO.cleanup()
