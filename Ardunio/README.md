# GY-25 角度测量实验

  GY-25是一款倾斜度传感器模块，价格在40块钱左右，主要是因为在家，没把实验室的传感器拿回来，所以用这款来尝试控制算法，用于获得数据。其工作电压在3-5v功耗小，体积小。其工作原理是通过陀螺仪与加速度传感器通过数据融合算法最后得到直接的酵素数据。其体积小、高性价比、串口输出格式是特点，可以应用于许多方面。

## 技术参数 & 引脚说明

|   名称   |        参数        |
| :------: | :----------------: |
| 测量范围 |     -180°~180°     |
|  分辨率  |       0.01°        |
| 测量精度 |         1°         |
| 重复精度 |         1°         |
| 响应频率 | 100HZ（115200bps） |
| 工作电压 |        3~5V        |
| 工作电流 |        15mA        |
| 工作温度 |      -20°~85°      |
| 存储温度 |     -40°~125°      |
|   尺寸   |   11.5mm×15.5mm    |

<center>
    <div style="color:orange; border-bottom: 1px solid #d9d9d9;
        display: inline-block;
        color: #999;
        padding: 2px;">
            表1.第一种设计模式
    </div>
</center>

|   引脚   |  名称   |            说明            |
| :------: | :-----: | :------------------------: |
| **Pin1** | **VCC** |            3-5V            |
| **Pin2** | **RX**  |        串口数据接受        |
| **Pin3** | **TX**  |        串口数据发送        |
| **Pin4** | **GND** |            接地            |
| **Pin5** | **RST** | 内部使用，不需要连接，悬空 |
| **Pin6** | **B0**  | 内部使用，不需要连接，悬空 |
| **Pin7** | **SCL** |     I2C 时钟，按需连接     |
| **Pin8** | **SDA** |     I2C 数据，按需链接     |

<center>
    <div style="color:orange; border-bottom: 1px solid #d9d9d9;
        display: inline-block;
        color: #999;
        padding: 2px;">
            表2.引脚说明
    </div>
</center>

## 命令字节

* `0xA5+0x51`：查询模式，直接返回角度值，需每次读取都发送
* `0xA5+0x52`：自动模式，直接返回角度值，只需要初始化时发送一次
* `0xA5+0x53`：自动模式，ASC码输出，便于直接电脑助手查看
* `0xA5+0x54`：校正模式，校正俯仰横滚角0度，需要保持水平时候发送
* `0xA5+0x55`：校正模式，校正航向0度，航向任意角度清零



## 代码

```c++
//GY-25  ARDUINO
//   GY25                  arduino UNO
//   VCC----------------------VCC
//   RX-----------------------TX
//   TX-----------------------RX
//   GND----------------------GND

#include <Wire.h>
int YPR[3];
unsigned char Re_buf[8],counter=0;
unsigned char sign=0;

void setup()
{
  Serial.begin(115200);  
  delay(2000);   
  Serial.write(0XA5);
  Serial.write(0X52);    //初始化GY25,连续输出模式
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
  while (Serial.available()) {   
    Re_buf[counter]=(unsigned char)Serial.read();
    if(counter==0&&Re_buf[0]!=0xAA) return;      // 检查帧头         
    counter++;      
    if(counter==8)                //接收到数据
    {   
       counter=0;                 //重新赋值，准备下一帧数据的接收
       sign=1;
    }      
  }
}
```

## 软串口

  由于角度传感器共需要两个，但是，硬件串口只有一个，所以需要增加一个软串口来完成同时获得两个角度传感器的数值，如果存在硬件串口和软件串口的差异，可以通过同时启用两个软串口，来解决这个问题。软串口通信的库函数是`SoftwareSerial`库，那么这个库的使用只需要简单知道如下语法，其他的和`Serial`相同。

```c++
#include <SoftwareSerial.h>  //包含头文件
Software mySerial(rxPin,txPin) //创建SoftwareSerial类，并完成引脚定义
```

  之后就可以开开心心的用软串口读取数据啦。

<img src="Picture\1.png" style="zoom:50%;" />