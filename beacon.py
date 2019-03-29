# unlock the door via bluetooth LE beacon
from threading import Thread
import time
import binascii
import os
import sys
from bluepy import btle
import time

class ScanPrint(btle.DefaultDelegate):
    def __init__(self, rssi, door):
        btle.DefaultDelegate.__init__(self)
        self.rssi = rssi
        self.door = door
        self.old = time.time()

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if dev.rssi < self.rssi:
            return False
        # mac address is: dev.addr
        if dev.addr != 'd8:63:1e:f6:53:82':
            return False
        dt = dev.getScanData()
        if dt[3][2] != '18031993-1234-abcd-0000-222222222222':
            return False
        # this is it our key
        if time.time() - self.old < 3:
            return False
        # ok muzem operovat!!!! teda otevira a zavirat vole ne
        self.old = time.time()
        self.door.getDoorState()
        if self.door.DOOR_STATE:
            self.door.unlock('SmartWatch')
        else:
            self.door.lock('SmartWatch')

class Beacon(Thread):
    """docstring for Beacon."""

    def __init__(self, door):
        self.door = door
        self.run_thread= True
        Thread.__init__(self)

    def run(self):
        # actual run of beacon
        # btle.Debugging = arg.verbose
        scanner = btle.Scanner(0).withDelegate(ScanPrint(-85, self.door))
        while self.run_thread:
            try:
                scanner.scan(2)
            except Exception as e:
                print(e)
