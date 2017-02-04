import machine
import time
from urequests import post


HOST_URI = 'http://mrl33h.de/bell/api/add'
# HOST_URI = 'http://192.168.1.102:8081/bell/api/add'


class R_TRIG:

    def __init__(self):
        self.previous_in = False
        self.out = False
        self.in_ = False

    def process(self, in_=None):
        if in_ is not None:
            self.in_ = in_
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
        if in_ is not None:
            self.in_ = in_

        self.out = False
        if self.in_:
            if self.t0 is None:
                self.t0 = time.ticks_ms()
            else:
                self.out = abs(time.ticks_ms() - self.t0) >= (self.seconds * 1000.0)
        else:
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
            print('State 0: Triggered')
            trig_counter = 1
            ton.process(in_=False)
            state = 10

    elif state == 10:
        ton.process(in_=True)
        if sound_rtrig.out:
            print('State 10: new rising edge')
            trig_counter += 1
        if ton.out:
            print('State 10: Timeout')
            state = 20

    elif state == 20:
        ton.process(in_=False)
        print('State 20: Sending post request')
        resp = post(HOST_URI, data='{"count": ' + str(trig_counter) + '}')
        print('State 20: Sent post')
        time.sleep(10)
        state = 0
