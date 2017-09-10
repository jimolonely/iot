
import serial

def write(pin):
    try:
        ser = serial.Serial('/dev/ttyACM0',9600)
        if pin==1:
            ser.write('1')
        else:
            ser.write('0')
    except:
        print('error')

if __name__=='__main__':
    p = int(input('1 or 0:'))
    write(p)
