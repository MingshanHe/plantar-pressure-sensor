#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import numpy as np
def pre_labels_cases():
    cases  = []
    labels = []

    csvFile = open('csv_file/2021_2_16_walk.csv','r')
    reader  = csv.reader(csvFile)
    flag = True
    for i in reader:
        if flag:
            flag = False
            continue
        case = []
        case.append(float(i[1]))
        case.append(float(i[2]))
        case.append(float(i[3]))
        case.append(float(i[4]))
        case.append(float(i[5]))
        case.append(float(i[6]))
        case.append(float(i[7]))
        case.append(float(i[8]))
        case.append(float(i[9]))
        case.append(float(i[10]))
        # case.append(float(0))
        label = i[11].split(",")
        for i in range(len(label)):
            label[i] = float(label[i])
        cases.append(np.array(case))
        labels.append(np.array(label))

    csvFile = open('csv_file/2021_2_16_stay.csv','r')
    reader  = csv.reader(csvFile)
    flag = True
    for i in reader:
        if flag:
            flag = False
            continue
        case = []
        case.append(float(i[1]))
        case.append(float(i[2]))
        case.append(float(i[3]))
        case.append(float(i[4]))
        case.append(float(i[5]))
        case.append(float(i[6]))
        case.append(float(i[7]))
        case.append(float(i[8]))
        case.append(float(i[9]))
        case.append(float(i[10]))
        # case.append(float(0))
        label = i[11].split(",")
        for i in range(len(label)):
            label[i] = float(label[i])
        cases.append(np.array(case))
        labels.append(np.array(label))
    return cases,labels