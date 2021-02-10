//GY-25  ARDUINO
//   GY25                  arduino UNO
//   VCC----------------------VCC
//   RX-----------------------TX
//   TX-----------------------RX
//   GND----------------------GND
#include <SoftwareSerial.h>
#include <Wire.h>

SoftwareSerial mySerial(2,3);//建立軟體串列埠腳位 (RX, TX)
int YPR[3];
unsigned char Re_buf[8],counter=0;
unsigned char sign=0;

void setup()
{ 
  Serial.begin(115200);
  while (!Serial) {
  }
  mySerial.begin(115200);  
  delay(2000);   
  mySerial.write(0XA5);
  mySerial.write(0X52);    //初始化GY25,连续输出模式
}
//-------------------------------------------------------------
void loop() {
  serialEvent();
  if(sign)
  {  
     sign=0;
     if(Re_buf[0]==0xAA && Re_buf[7]==0x55)        //检查帧头，帧尾
     {                 
            YPR[0]=(Re_buf[1]<<8|Re_buf[2])/100;   //合成数据，去掉小数点后2位
            YPR[1]=(Re_buf[3]<<8|Re_buf[4])/100;
            YPR[2]=(Re_buf[5]<<8|Re_buf[6])/100;
              
            Serial.print("YPR[0]: ");
            Serial.print(YPR[0]);      //显示航向
            Serial.print(" "); 
            Serial.print("YPR[1]: ");                    
            Serial.print(YPR[1]);     
            Serial.print(" ");
            Serial.print("YPR[2]: ");  
            Serial.print(YPR[2]);   
            Serial.println("");   
            delay(100);           
   }
  }
}
//---------------------------------------------------------------
void serialEvent() {
  while (mySerial.available()) {   
    Re_buf[counter]=(unsigned char)mySerial.read();
    if(counter==0&&Re_buf[0]!=0xAA) return;      // 检查帧头         
    counter++;      
    if(counter==8)                //接收到数据
    {   
       counter=0;                 //重新赋值，准备下一帧数据的接收
       sign=1;
    }      
  }
}
