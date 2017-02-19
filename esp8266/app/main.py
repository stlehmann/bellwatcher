import network
import machine
import utime
from urequests import post

from control import TON, R_TRIG

__version__ = '0.0.1'

HOST_URI = 'http://mrl33h.de/bell/'
SOUND_TIME = 5.0
ALIVE_TIME = 3600.0
SLEEP_TIME = 10.0

STATE_INIT = 0
STATE_STANDBY = 5
STATE_TRIGGERED = 10
STATE_POST = 20
STATE_SLEEP = 30

sta_if = network.WLAN(network.STA_IF)
sound_in = False
sound_pin = machine.Pin(16, machine.Pin.IN)
sound_rtrig = R_TRIG()
sound_ton = TON(SOUND_TIME)
sound_counter = 0
sleep_ton = TON(SLEEP_TIME)
alive_ton = TON(ALIVE_TIME)
state = STATE_INIT


def init():
    print('Starting up')
    utime.sleep(1)
    if sta_if.active():
        print('Version: ', __version__)
        print('Network Connection active')
        print('IP: ', sta_if.ifconfig()[0])
    else:
        print('Error: Network connection not active')

    resp = post(HOST_URI + 'api/log', data='{"message": "Restarted"}')
    resp.close()


def main():
    while True:
        global state

        # Get value of sound sensor (inverted)
        sound_in = sound_pin.value() == 0
        sound_rtrig.process(sound_in)
        sound_ton.process(state == STATE_TRIGGERED)
        alive_ton.process(not alive_ton.out)
        sleep_ton.process(state == STATE_SLEEP)

        if state == STATE_INIT:
            print('Ready')
            state = STATE_STANDBY

        if state == STATE_STANDBY:
            if sound_rtrig.out:
                print('Rising Edge')
                counter = 1
                state = STATE_TRIGGERED

        elif state == STATE_TRIGGERED:
            if sound_rtrig.out:
                counter += 1
                print('Rising Edge ', counter)
            if sound_ton.out:
                state = STATE_POST

        elif state == STATE_POST:
            print('Post')
            resp = post(HOST_URI + 'api/add',
                        data='{"count": ' + str(counter) + '}')
            resp.close()
            print('Sleeping')
            state = STATE_SLEEP

        elif state == STATE_SLEEP:
            if sleep_ton.out:
                state = STATE_INIT

        if alive_ton.out:

            resp = post(HOST_URI + 'api/log', data='{"message": "Alive"}')
            resp.close()


init()
main()
