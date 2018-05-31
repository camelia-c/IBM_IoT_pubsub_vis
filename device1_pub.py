import ibmiotf.device
import threading
import time
from random import randint

class EmulatedDevice(threading.Thread):

    token = "**************"

    def __init__(self, org, devtype, devid):
        threading.Thread.__init__(self)
        self.organization = org
        self.device_type = devtype
        self.device_id = devid

        self.reading = {}
        self.count_sent = 0
        self.count_ack = 0

        self.deviceOptions = {"org": self.organization,
                             "type": self.device_type,
                             "id": self.device_id ,
                             "auth-method": "token",
                             "auth-token": self.token}
        self.deviceCli = ibmiotf.device.Client(self.deviceOptions)

        #connect the device
        self.deviceCli.connect()

    def myOnPublishCallback(self):
        self.count_ack = self.count_ack + 1
        print("IoT platform acknowledged " + str(self.count_ack) +
              " out of a total of " + str(self.count_sent) +
              " sent by " + self.device_id)

    def run(self):
        print("device " + self.device_id + " is connected")

        for iter in range(30):
            #refresh data
            for sensor in ['a','b','c','d','e','f','g','h']:
                self.reading[sensor] = randint(0, 50)


            self.reading['latitude'] = 51.749499
            self.reading['longitude'] = -1.268661


            success = self.deviceCli.publishEvent(event="sensors_reading", msgFormat="json",
                                                  data = self.reading, qos=0,
                                                  on_publish=self.myOnPublishCallback)
            self.count_sent = self.count_sent + 1

            #sleep 10 seconds
            time.sleep(10)

        print("device " + self.device_id + " is disconnected")








if __name__ == '__main__':
    emdev1 = EmulatedDevice(org = "******", devtype="dev_rpi3", devid="dev1")
    emdev2 = EmulatedDevice(org = "******", devtype="dev_rpi3", devid="dev2")
    emdev3 = EmulatedDevice(org = "******", devtype="dev_rpi3", devid="dev3")

    emdev1.start()
    emdev2.start()
    emdev3.start()







