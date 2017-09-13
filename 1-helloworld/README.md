# 说明
智能家居第一步：helloworld：点亮一个灯泡。

通过Android客户端发送命令，通过外网服务器，树莓派担任控制主机，轮训进行接收服务器信息，然后向串口发送命令，Arduino接收到串口信息判断是否点亮一个灯泡。

需要用到：
1. Arduino
2. Raspberry Pi（开发时可以用电脑）
3. 云服务器（可选，假如有外网映射工具的话）
4. python
5. web服务器相关
6. Android开发相关

# 实现
## 先从Arduino开始
只需要关注串口的值，然后控制灯泡即可

[hello.ino](https://github.com/jimolonely/iot/blob/master/1-helloworld/hello.ino)
```arduino
/**
循环检测串口；
如果串口数据为1则点亮灯泡；
否则熄灭灯泡。
*/

int ledPin = 13;
char ch = '0';
void setup(){
  Serial.begin(9600);
  pinMode(ledPin,OUTPUT);
}

void loop(){
    if(Serial.available()>0){
      ch = Serial.read();
      if(ch=='1'){
        digitalWrite(ledPin,HIGH);
      }else {
        digitalWrite(ledPin,LOW);
      }
    }
}
```
## 如何向串口写数据
使用python的pyserial模块，需要安装，然后简单测试一下：

[test.py](https://github.com/jimolonely/iot/blob/master/1-helloworld/test.py)
```python
import serial

def write(pin):
    try:
        ser = serial.Serial('/dev/ttyACM1',9600)
        if pin==1:
            ser.write('1')
        else:
            ser.write('0')
    except:
        print('error')

if __name__=='__main__':
    p = int(input('1 or 0:'))
    write(p)
```
linux下的串口可以在Arduino的IDE里看到，也可以使用下面的命令查看：
```shell
jimo@jimo-PC:~$ ls /dev/tty*
/dev/tty    /dev/tty17  /dev/tty26  /dev/tty35  /dev/tty44  /dev/tty53  /dev/tty62
/dev/tty0   /dev/tty18  /dev/tty27  /dev/tty36  /dev/tty45  /dev/tty54  /dev/tty63
/dev/tty1   /dev/tty19  /dev/tty28  /dev/tty37  /dev/tty46  /dev/tty55  /dev/tty7
/dev/tty10  /dev/tty2   /dev/tty29  /dev/tty38  /dev/tty47  /dev/tty56  /dev/tty8
/dev/tty11  /dev/tty20  /dev/tty3   /dev/tty39  /dev/tty48  /dev/tty57  /dev/tty9
/dev/tty12  /dev/tty21  /dev/tty30  /dev/tty4   /dev/tty49  /dev/tty58  /dev/ttyACM1
/dev/tty13  /dev/tty22  /dev/tty31  /dev/tty40  /dev/tty5   /dev/tty59  /dev/ttyS0
/dev/tty14  /dev/tty23  /dev/tty32  /dev/tty41  /dev/tty50  /dev/tty6   /dev/ttyS1
/dev/tty15  /dev/tty24  /dev/tty33  /dev/tty42  /dev/tty51  /dev/tty60  /dev/ttyS2
/dev/tty16  /dev/tty25  /dev/tty34  /dev/tty43  /dev/tty52  /dev/tty61  /dev/ttyS3
```
windows下直接就是COMx

但是我们需要的输入不是来自命令行，而是服务器，我们通过不断轮训获取服务器的命令，然后写入串口。所以在此之前先将服务器搭建了。

## 服务器
为了尽可能简单，采用一个不依赖其他库的python框架：[bottle.py](https://github.com/bottlepy/bottle)

服务器要做的事很简单，接受来自2个地方的请求，APP和设备。

APP：发出控制命令，服务器存在某个地方（内存，数据库）

设备：不断轮训取得命令数据，或许可以增加上传数据，然后APP可以查看。

可以看一个很简单的实现：

[server.py](https://github.com/jimolonely/iot/blob/master/1-helloworld/web-server/server.py)
```python
#-*-coding:utf-8-*-

from bottle import run,route

@route('/')
def index():
    return 'Hello World'

cmd = 0

@route('/writecmd/<command>')
def write_cmd(command):
    global cmd
    cmd = command
    return str(cmd)

@route('/getcmd')
def get_cmd():
    return str(cmd)

run(host='127.0.0.1',port=8080)
```
我们只需访问：

http://127.0.0.1:8080/writecmd/0或1 写入命令

http://127.0.0.1:8080/getcmd 读取命令

使用cmd存储命令，记住global cmd
```python
cmd = 0
@route('/writecmd/<command>')
def write_cmd(command):
    global cmd
    cmd = command
    return str(cmd)
```

## 获取命令
现在有了服务器，可以供设备查询了。修改test.py，增加访问，当然是使用号称给人类使用的库requests。

[device_req.py](https://github.com/jimolonely/iot/blob/master/1-helloworld/device_req.py)
```python
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
    url = 'http://127.0.0.1:8080/getcmd'
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
```

## 到这里

会发现同时访问服务器很容易就挂了，device的代码也很容易就阻塞了。

经过实验，我发现是服务器太弱了，bottle虽然简单，不过还是太差了，所以换成django。

## 换成django服务器

主要代码是一样的，写入的访问方式变了：http://127.0.0.1:8000/write?cmd=0
```python
from django.http import HttpResponse

cmd = '0'

def write(req):
    global cmd
    cmd = req.GET['cmd']
    return HttpResponse(cmd)

def getcmd(req):
    return HttpResponse(cmd)
```
然后就很顺利了。修复了一些bug，优化一下代码。现在只差客户端了。



