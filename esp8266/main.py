import machine
import time
from urequests import post

HOST_URI = 'http://192.168.1.102:5000/api/add'


bell = machine.Pin(16, machine.Pin.IN)
led = machine.Pin(5, machine.Pin.OUT)


def send():
    resp = post(HOST_URI)
    if resp.text == 'ok':
        led.high()
    time.sleep(1)
    led.low()


time.sleep(5)
while True:
    if bell.value() == 0:
        send()
