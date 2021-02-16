import csv
import matplotlib.pyplot as plt

csvFile = open('csv_file/2021_2_16_run.csv','r')
reader  = csv.reader(csvFile)

x = []
y1 = []
y2 = []
y3 = []
y4 = []
y5 = []
y6 = []
for item in reader:
    if reader.line_num == 1:
        continue
    x.append(float(item[0]))
    y1.append(float(item[1]))
    y2.append(float(item[2]))
    y3.append(float(item[3]))
    y4.append(float(item[1]))
    y5.append(float(item[2]))
    y6.append(float(item[3]))
plt.plot(x,y1,label="value1")
plt.plot(x,y2,label="value2")
plt.plot(x,y3,label="value3")
plt.plot(x,y4,label="value4")
plt.plot(x,y5,label="value5")
plt.plot(x,y6,label="value6")
plt.legend()
plt.show()
