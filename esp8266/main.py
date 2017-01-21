import machine
import time
from urequests import post

HOST_URI = 'http://mrl33h.de/bell/api/add'


bell = machine.Pin(16, machine.Pin.IN)
led = machine.Pin(5, machine.Pin.OUT)


def send():
    resp = post(HOST_URI)
    if resp.text == 'ok':
        led.high()
    time.sleep(10)
    led.low()


time.sleep(5)
while True:
    if bell.value() == 0:
        send()
