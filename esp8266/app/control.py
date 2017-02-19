import utime


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
                self.t0 = utime.ticks_ms()
            else:
                self.out = abs(utime.ticks_ms() - self.t0) >= (self.seconds * 1000.0)
        else:
            self.t0 = None
        return self.out
