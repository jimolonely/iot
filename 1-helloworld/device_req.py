#-*-coding:utf-8-*-

import serial
import requests
import time

def write(cmd):
    print(cmd)
    try:
        ser = serial.Serial('/dev/ttyACM0',9600)
        ser.write(cmd)
    except:
        print('error')

def get_cmd():
    url = 'http://127.0.0.1:8080/getcmd'
    while 1:
        resp = requests.get(url)
        write(resp.text)
        time.sleep(2)

if __name__=='__main__':
    get_cmd()
