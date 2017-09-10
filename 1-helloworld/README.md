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
### 先从Arduino开始
只需要关注串口的值，然后控制灯泡即可

*hello.ino*
```arduino
/**
循环检测串口；
如果串口数据为1则点亮灯泡；
否则熄灭灯泡。
*/
int ledPin = 13;
char ch = '1';
void setup(){
  Serial.begin(9600);
  pinMode(ledPin,OUTPUT);
}

void loop(){
  Serial.write(ch);
  while(1){
    if(Serial.available()){
      ch = Serial.read();
      Serial.print(ch);
      if(ch=='1'){
        digitalWrite(ledPin,HIGH);
      }else{
        digitalWrite(ledPin,LOW);
      }
    }
  }
}
```
### 如何向串口写数据
使用python的pyserial模块，需要安装，然后简单测试一下：

*test.py*
```python
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
```
linux下的串口可以在Arduino的IDE里看到，也可以使用下面的命令查看：
```shell
jimo@jimo-PC:~$ ls /dev/tty
tty    tty13  tty19  tty24  tty3   tty35  tty40  tty46  tty51  tty57  tty62  ttyS1
tty0   tty14  tty2   tty25  tty30  tty36  tty41  tty47  tty52  tty58  tty63  ttyS2
tty1   tty15  tty20  tty26  tty31  tty37  tty42  tty48  tty53  tty59  tty7   ttyS3
tty10  tty16  tty21  tty27  tty32  tty38  tty43  tty49  tty54  tty6   tty8   
tty11  tty17  tty22  tty28  tty33  tty39  tty44  tty5   tty55  tty60  tty9   
tty12  tty18  tty23  tty29  tty34  tty4   tty45  tty50  tty56  tty61  ttyS0 
```
windows下直接就是COMx

但是我们需要的输入不是来自命令行，而是服务器，我们通过不断轮训获取服务器的命令，然后写入串口。所以在此之前先将服务器搭建了。

