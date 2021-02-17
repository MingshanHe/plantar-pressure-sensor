import csv
import matplotlib.pyplot as plt

csvFile = open('csv_file/2021_2_16_walk.csv','r')
reader  = csv.reader(csvFile)

x = []
y1 = []
y2 = []
y3 = []
y4 = []
y5 = []

for item in reader:
    if reader.line_num == 1:
        continue
    x.append(float(item[0]))
    y1.append(float(item[1]))
    y2.append(float(item[2]))
    y3.append(float(item[3]))
    y4.append(float(item[4]))
    y5.append(float(item[5]))
plt.plot(x,y1,label="Angle-Thigh")
plt.plot(x,y2,label="Angle-Calf")
plt.plot(x,y3,label="Presure-Front")
plt.plot(x,y4,label="Presure-Middle")
plt.plot(x,y5,label="Presure-Back")

plt.legend()
plt.show()
