import time
import serial

ser = serial.Serial(  # 下面这些参数根据情况修改
  port='COM13',# 串口
  baudrate=9600,# 波特率
  parity=serial.PARITY_ODD,
  stopbits=serial.STOPBITS_TWO,
  bytesize=serial.SEVENBITS

)
every_time = time.strftime('%Y-%m-%d %H:%M:%S')# 时间戳\
time_start = time.time()
# data = ''
data_list = []
while True:
  data = ser.readline()
  data = data.decode()
#   intdata = int.from_bytes(data, byteorder='big', signed = False)
  now_time = time.time()
  print(now_time-time_start,": ", data)