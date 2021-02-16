import csv
import numpy as np
with open( 'csv_file/test.csv','w',newline='') as csvfile:
    csv_write = csv.writer(csvfile)
    csv_write.writerow([[1,1,1],[1,2,1]])

csvFile = open('csv_file/test.csv','r')
reader  = csv.reader(csvFile)
for i in reader:
    print(i)
    print(type(i))