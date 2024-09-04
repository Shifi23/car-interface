import pyfirmata2
import time

IGN = 4
SRT = 5
KSN = 7
PKL = 6
UNL = 8
LOC = 9
INL = 10
ACC = 11
rxled = 4
txled = 5

class RelayController:

    def __init__(self) -> None:
        self.port = pyfirmata2.Arduino.AUTODETECT
        self.controller = pyfirmata2.Arduino(self.port)
        self.controller.digital[IGN].write(1)
        self.controller.digital[KSN].write(1)
        self.controller.digital[SRT].write(1)
        self.controller.digital[PKL].write(1)
        self.controller.digital[UNL].write(1)
        self.controller.digital[LOC].write(1)
        self.controller.digital[INL].write(1)
        self.controller.digital[ACC].write(1)


    def test(self):
        self.controller.digital[rxled].write(1)
        self.controller.digital[txled].write(0)
        time.sleep(1)
        self.controller.digital[rxled].write(0)
        self.controller.digital[txled].write(1)
        time.sleep(1)
    
    def lock_car(self):
        self.controller.digital[LOC].write(0)
        time.sleep(0.5)
        self.controller.digital[LOC].write(1)
        time.sleep(0.5)
        self.controller.digital[LOC].write(0)
        time.sleep(0.5)
        self.controller.digital[LOC].write(1)
        time.sleep(0.5)

    def unlock_car(self):
        self.controller.digital[UNL].write(0)
        time.sleep(0.5)
        self.controller.digital[UNL].write(1)
        time.sleep(0.5)
        self.controller.digital[UNL].write(0)
        time.sleep(0.5)
        self.controller.digital[UNL].write(1)
        time.sleep(0.5)

    def start_engine(self):
        self.controller.digital[KSN].write(0)
        time.sleep(2)
        self.controller.digital[IGN].write(0)
        time.sleep(2)
        self.controller.digital[SRT].write(0)
        time.sleep(0.9)
        self.controller.digital[SRT].write(1)
        time.sleep(1)
        self.controller.digital[ACC].write(0)

    def stop_engine(self):
        self.controller.digital[KSN].write(1)
        self.controller.digital[IGN].write(1)
        self.controller.digital[SRT].write(1)
        self.controller.digital[PKL].write(1)
        self.controller.digital[ACC].write(1)

    def turn_on_parking_lights(self):
        self.controller.digital[PKL].write(0)
        self.controller.digital[INL].write(0)

    def turn_off_parking_lights(self):
        self.controller.digital[PKL].write(1)
        self.controller.digital[INL].write(1)
    
    def flash_hazard_lights(self):
        pass

    def __del__(self):
        self.controller.exit()
