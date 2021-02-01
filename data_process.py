from multiprocessing import Process, Queue
import csv
import keyboard
import os
import time
import serial

time_start = time.time()
def string_to_float(str):
  return float(str)

def get_data_from_serial(ser, cut=','):

  data = ser.readline()
  data = data.decode()
  num_list = []
  n = len(data)
  num_str1 = ''
  num_str2 = ''
  cut_flag = 0
  for i in range(1,n-1):
      if data[i] == cut:
          cut_flag = 1
          continue
      if cut_flag:
          num_str2 = num_str2+data[i]
      else:
          num_str1 = num_str1+data[i]
  now_time = time.time()
  num_list.append(now_time-time_start)
  num_str2 = string_to_float(num_str2)
  num_list.append(num_str2)
  return num_list

def pre_csv_file(file_path='csv_file/save_csv.csv',csv_head=[],mode='new'):
  '''
  csv file creation
  '''
  def create_csv(csv_head = [], path='csv_file/save_csv.csv'):
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
  file_path = 'csv_file/save_csv.csv'
  csv_head  = ['time','value']
  mode = 'new'

  ser = serial.Serial( port='COM13', baudrate=9600,parity=serial.PARITY_ODD,
  stopbits=serial.STOPBITS_TWO,bytesize=serial.SEVENBITS)
  # pre process of csv file
  pre_csv_file(file_path,csv_head,mode)

  # read data and save in csv file
  with open(file_path,'a+', newline='') as f:
    csv_write = csv.writer(f)
    n = 0
    while q.empty():
        num_list=get_data_from_serial(ser)
        csv_write.writerow(num_list)
        print('\r', num_list, end='')
        n = n+1

def key_board_listen(q):
    keyboard.wait('esc')
    q.put(1)

if __name__ == "__main__":
  q = Queue()
  p1 = Process(target=data_to_csv, args=(q,))
  p2 = Process(target=key_board_listen, args=(q,))
  p1.start()
  p2.start()
  p1.join()
  p2.join()