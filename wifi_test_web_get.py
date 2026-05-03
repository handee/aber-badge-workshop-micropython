import network
import time
import machine
import urequests

print("Starting...")
ssid='your ssid'# edit this
password='your password' # also this, obv
import network
def do_connect():
    wlan = network.WLAN()
    wlan.active(False)
    wlan.active(True)
    macaddr= wlan.config('mac')
    print('Hello! This is my mac address:')
    print(macaddr)
    print('These are the access points I can see:')
    nets=wlan.scan()
    for net in nets:
        print(net)
    print('Now I am going to try to connect to ...')
    print(ssid)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid,password)
        while not wlan.isconnected():
            pass
    print('Hurrah I have an IP Address and it is in the following line:')
    print('network config:', wlan.ipconfig('addr4'))
do_connect()
r=urequests.get('https://www.hannahdee.wales/test.txt')
print(r.status_code)
print(r.text)

