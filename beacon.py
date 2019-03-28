# unlock the door via bluetooth LE beacon
from threading import Thread
import time

class Beacon(Thread):
    """docstring for Beacon."""

    def __init__(self, door):
        self.door = door
        Thread.__init__(self)

    def run(self):
        # actual run of beacon
        last_time = 0
        while 1:
            try:
                # main run

                #load bluetooth things, its w8 for samples

                # is it right sample??? it is unlock the door else again
                # check also last time!!!!
                # if time.time() - last_time < 3:
                #   continue

                # if is ok just last_time includet
                last_time = time.time()

                pass
            except Exception as e:
                pass
