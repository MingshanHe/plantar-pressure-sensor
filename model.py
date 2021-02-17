# /*
#  * @Author: MingshanHe
#  * @Email: hemingshan@robotics.github.com
#  * @Date: 2021-02-17 17:54:54
#  * @Last Modified by:   MingshanHe
#  * @Last Modified time: 2021-02-17 17:54:54
#  * @Description: Description
#  */
import numpy as np
import math
import random
from pre_labels_cases import *

class Network(object):
    def __init__(self, ni, nh, no):
        self.input_n = ni
        self.hidden_n = nh
        self.output_n = no
        # init cells
        self.input_cells  = np.array([0.0]*self.input_n)
        self.hidden_cells = np.array([0.0]*self.hidden_n)
        self.output_cells = np.array([0.0]*self.output_n)
        # init weights
        self.input_weights  = self.make_matrix(self.input_n, self.hidden_n)
        self.output_weights = self.make_matrix(self.hidden_n, self.output_n)
        # random activate
        for i in range(self.input_n):
            for h in range(self.hidden_n):
                self.input_weights[i][h]  = self.rand(-0.2, 0.2)
        for h in range(self.hidden_n):
            for o in range(self.output_n):
                self.output_weights[h][o] = self.rand(-2.0, 2.0)
        # init correction matrix
        self.input_correction  = self.make_matrix(self.input_n, self.hidden_n)
        self.output_correction = self.make_matrix(self.hidden_n, self.output_n)

    def predict(self, inputs):
        # activate input layer
        self.input_cells = inputs
        # activate hidden layer
        result = self.input_cells.dot(self.input_weights)
        for i in range(self.hidden_n):
            self.hidden_cells[i] = self.sigmoid(result[i])
        # activate output layer
        result = self.hidden_cells.dot(self.output_weights)
        for i in range(self.output_n):
            self.output_cells[i] = self.sigmoid(result[i])
        return self.output_cells[:]

    def back_propagate(self, case, label, learn, correct):
        # feed forward
        self.predict(case)
        # get output layer error
        output_deltas = np.array([0.0]*self.output_n)
        error = label - self.output_cells
        for o in range(self.output_n):
            output_deltas[o] = self.sigmod_derivate(self.output_cells[o]) * error[o]
        # get hidden layer error
        hidden_deltas = np.array([0.0]*self.hidden_n)
        result = output_deltas.dot(self.output_weights.T)
        for h in range(self.hidden_n):
            hidden_deltas[h] = self.sigmod_derivate(self.hidden_cells[h]) * result[h]
        # update output weights
        for h in range(self.hidden_n):
            for o in range(self.output_n):
                change = output_deltas[o] * self.hidden_cells[h]
                self.output_weights[h][o] += learn * change + correct * self.output_correction[h][o]
                self.output_correction[h][o] = change
        # update input weights
        for i in range(self.input_n):
            for h in range(self.hidden_n):
                change = hidden_deltas[h] * self.input_cells[i]
                self.input_weights[i][h] += learn * change + correct * self.input_correction[i][h]
                self.input_correction[i][h] = change
        # get global error
        error = 0.0
        for o in range(len(label)):
            error += 0.5 * (label[o] - self.output_cells[o]) ** 2
        return error

    def train(self, cases, labels, limit=10000, learn=0.05, correct=0.1):
        for i in range(limit):
            error = 0.0
            for j in range(len(cases)):
                label = labels[j]
                case = cases[j]
                error += self.back_propagate(case, label, learn, correct)
            if i%100 == 0:
                print("i: ",i," error: ",error,'output_label: ',self.output_cells)

    def sigmoid(self,x):
        try:
            return 1.0 / (1.0 + math.exp(-x))
        except OverflowError:
            return 0
    def sigmod_derivate(self,x):
        return x * (1 - x)

    def make_matrix(self,m, n):  # 创造一个指定大小的矩阵
        mat = np.ones((m,n))
        return mat

    def rand(self,a, b):
        return (b - a) * random.random() + a

if __name__ == "__main__":
    # nn = Network(3,3,3)
    # cases  = [np.array([1,0,0]),np.array([0,1,0]),np.array([0,0,1])]
    # labels = [np.array([0,1,0]),np.array([0,0,1]),np.array([1,0,0])]
    # nn.train(case,label)
    nn = Network(10,10,3)

    cases,labels = pre_labels_cases()
    nn.train(cases,labels,limit=500,learn=0.1)
    print(nn.input_weights)
    print(nn.output_weights)
    for i in range(len(cases)):
        print(nn.predict(cases[i]),labels[i])
        
