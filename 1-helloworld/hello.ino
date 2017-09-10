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
