import csv
import matplotlib.pyplot as plt

csvFile = open('csv_file/save_csv.csv','r')
reader  = csv.reader(csvFile)

x = []
y = []
for item in reader:
    if reader.line_num == 1:
        continue
    x.append(float(item[0]))
    y.append(float(item[1])*5.0/1023)
plt.plot(x,y)

plt.show()
