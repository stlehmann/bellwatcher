import machine
import time
from urequests import post

HOST_URI = 'http://mrl33h.de/bell/api/add'


class R_TRIG:

    def __init__(self):
        self.previous_in = False
        self.out = False
        self.in_ = False

    def process(self, in_=None):
        self.in_ = in_ or self.in_
        self.out = in_ and not self.previous_in
        self.previous_in = in_
        return self.out


class TON:

    def __init__(self, seconds=None):
        self.seconds = seconds or 0.0
        self.in_ = False
        self.t0 = None
        self.out = False

    def process(self, in_=None):
        self.in_ = in_ or self.in_
        if self.in_:
            if self.t0 is None:
                self.t0 = time.ticks_ms()
            else:
                self.out = time.ticks_ms() - self.t0 >= (self.seconds * 1000.0)
        else:
            self.out = False
            self.t0 = None
        return self.out


pin_bell = machine.Pin(16, machine.Pin.IN)
sound_rtrig = R_TRIG()
ton = TON(5.0)
trig_counter = 0
state = 0


time.sleep(5)
while True:
    sound = pin_bell.value() == 0
    sound_rtrig.process(sound)

    if state == 0:
        if sound_rtrig.out:
            trig_counter = 1
            ton.process(in_=False)
            state = 10

    elif state == 10:
        ton.process(in_=True)
        if sound_rtrig.out:
            trig_counter += 1
        if ton.out:
            state = 20

    elif state == 20:
        ton.process(in_=False)
        resp = post(HOST_URI, data={'count': trig_counter})
        time.sleep(10)
        state = 0
