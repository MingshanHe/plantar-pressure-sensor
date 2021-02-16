from multiprocessing import Process, Queue
import csv
import keyboard
import os
import time
import serial 

time_start = 0
now_time = 0
flag = True

def string_to_float(str):

  return float(str)

def get_data_from_serial(ser, cut=','):
  global flag
  global time_start
  global now_time
  data = ser.readline()
  data = data.decode()
  if(flag):
    time_start = time.time()
    flag = False
  num_list = []
  n = len(data)
  num_str1 = ''
  num_str2 = ''
  num_str3 = ''
  num_str4 = ''
  num_str5 = ''
  cut_flag = 0
  for i in range(0,n):
      if data[i] == cut:
          cut_flag += 1
          continue
      if (cut_flag == 1):
          num_str2 = num_str2+data[i]
      elif (cut_flag == 2):
          num_str3 = num_str3+data[i]
      elif (cut_flag == 3):
          num_str4 = num_str4+data[i]
      elif (cut_flag == 4):
          num_str5 = num_str5+data[i]
      else:
          num_str1 = num_str1+data[i]
  now_time = time.time()
  num_list.append(now_time-time_start)
  num_str1 = string_to_float(num_str1)
  num_list.append(num_str1)
  num_str2 = string_to_float(num_str2)
  num_list.append(num_str2)
  num_str3 = string_to_float(num_str3)
  num_list.append(num_str3)
  num_str4 = string_to_float(num_str4)
  num_list.append(num_str4)
  # print(num_str5)
  num_str5 = string_to_float(num_str5)
  num_list.append(num_str5)
  return num_list

def pre_csv_file(file_path='csv_file/2021_2_16_stand.csv',csv_head=[],mode='new'):
  '''
  csv file creation
  '''
  def create_csv(csv_head = [], path='csv_file/2021_2_16_stand.csv'):
    with open(path,'w',newline='') as f:
      csv_write = csv.writer(f)
      if csv_head!=[]:
        csv_write.writerow(csv_head)

  if mode =='new':
    if os.path.isfile(file_path):
      os.remove(file_path)
    create_csv(csv_head, file_path)
  elif mode == 'add':
    if os.path.isfile(file_path) == False:
      print('源文件缺失，自动新建')
      create_csv(csv_head,file_path)

def data_to_csv(q):
  global time_start
  global now_time
  file_path = 'csv_file/2021_2_16_stand.csv'
  csv_head  = ['time','Angle_Thigh','Angle_Calf','Presure_Front','Presure_Middle','Presure_Back']
  mode = 'new'

  ser = serial.Serial( port='COM13', baudrate=115200,parity=serial.PARITY_ODD,
  stopbits=serial.STOPBITS_TWO,bytesize=serial.SEVENBITS)
  # pre process of csv file
  pre_csv_file(file_path,csv_head,mode)

  # read data and save in csv file
  with open(file_path,'a+', newline='') as f:
    csv_write = csv.writer(f)
    n = 0
    while (now_time-time_start)<=2:
        num_list=get_data_from_serial(ser)
        csv_write.writerow(num_list)
        print('\r', num_list, end='')
        n = n+1

if __name__ == "__main__":
   
  q = Queue()
  p1 = Process(target=data_to_csv, args=(q,))
  p1.start()
  p1.join()
