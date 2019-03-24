## SG90 servo

import RPi.GPIO as GPIO     ## Import GPIO library
import time
import os
import sys

GPIO.setmode(GPIO.BCM) ## Use board pin numbering

#pins are pulled up because the reed switches are ON by default.

GPIO.setup(18, GPIO.IN)

GPIO.setup(14, GPIO.OUT)
p25=GPIO.PWM(14, 50)  # pin 18, and 50 Hz


p25.start(7.5) # set to neutral position - 7.5% duty cycle
#p.ChangeFrequency
#p.stop
time.sleep(2)

while 1:
    for i in range(200):
        print('Cidlo: {}'.format(GPIO.input(18)))
        input('Do you want to close')
        p25.ChangeDutyCycle(0.1)
        time.sleep(.1)
        p25.ChangeDutyCycle(0)
        print('Cidlo: {}'.format(GPIO.input(18)))
        input('Do you want to open')
        #p25.ChangeDutyCycle(7.5)
        #time.sleep(.8)
        p25.ChangeDutyCycle(22)
        time.sleep(.1)
        p25.ChangeDutyCycle(0)
        #p25.ChangeDutyCycle(0.1)
        #time.sleep(.50290333)
        #p25.ChangeDutyCycle(7.5)
exit()
try:
    for i in range(100):
        print(i)
        time.sleep(1)
    exit()
    while True:
        print("nevim co se deje 1")
        for i in range(1, 30):
            p25.ChangeDutyCycle(i/2)
            time.sleep(0.04)

        print('nevim co de deje')
        for i in range(1, 30):
            p25.ChangeDutyCycle(14.5-(i/2))
            time.sleep(0.04)

except KeyboardInterrupt:
    p25.ChangeDutyCycle(7.5)
    p25.stop
    time.sleep(0.5)
GPIO.cleanup()

