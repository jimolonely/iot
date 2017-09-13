#-*-coding:utf-8-*-

import serial
import requests
import time
import threading

def write(cmd):
    print(cmd)
    try:
        ser = serial.Serial('/dev/ttyACM0',9600)
        ser.write(bytes(cmd,encoding='utf-8'))
    except Exception as e:
        print(e)

def get_cmd():
    url = 'http://127.0.0.1:8000/getcmd'
    cmd = '0'
    while 1:
        try:
            resp = requests.get(url,timeout=5)
            cmd = resp.text
        except Exception as e:
            print(e)
        write(cmd)
        time.sleep(2)

if __name__=='__main__':
    t = threading.Thread(target=get_cmd)
    t.start()
