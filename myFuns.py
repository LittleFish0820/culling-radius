import math
import numpy as np
import matplotlib.pyplot as plt

def showMap(data):
    n = len(data)
    X = [data[i].x for i in range(n)]
    Y = [data[i].y for i in range(n)]
    color = [color_map[data[i].state] for i in range(n)]
    plt.figure(figsize = (5, 5), dpi = 100)
    plt.grid(True, linestyle = '--', alpha = 0.5)
    plt.xlim([-5.2, 5.2])
    plt.ylim([-5.2, 5.2])
    plt.xticks([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
    plt.yticks([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
    plt.scatter(X, Y, s = 8, c = color)
    plt.show()

def select(p):
    return 1 if np.random.random() <= p else 0

def Euclidean(x, y):
    return x * x + y * y

def trans_kernel(d, h_0 = 0.0016, d_0 = 1.9, alpha = 2.1):
    return h_0 / (1 + math.pow(d / d_0, alpha))

def culling_capacity(t):
    if 0 <= t < 4:
        return 0
    elif 4 <= t < 5:
        return 2 * t - 8
    elif 5 <= t < 11:
        return 7 / 12.0 * (t - 5) * (t - 5) + 2
    return 23

def cal_reproduction_value(matrix_d, i, c = 1, T = 2):
    R_i = 0
    for j in range(len(matrix_d)):
        d_ij = matrix_d[i][j]
        R_i += 1 - math.pow(c / (c + T * trans_kernel(d_ij)), c)
    return R_i
    
def estimate_E(data, matrix_d, i, t):
    return cal_reproduction_value(matrix_d, i) * estimate_p(data, matrix_d, i, t)
    
def estimate_p(data, matrix_d, i, t):
    return 1 - math.exp(-estimate_lambda(data, matrix_d, i, t))

def estimate_lambda(data, matrix_d, i, t, T = 2):
    res = 0
    for j in range(len(data)):
        d_ij = matrix_d[i][j]
        h_ij = trans_kernel(d_ij)
        I = 0
        if data[j].state == "Detected":
            I = T - min(t - data[j].time_detected, T)
        res += h_ij * I
    return res

def cal_lambda(data, matrix_d, i):
    res = 0
    for j in range(len(matrix_d)):
        d_ij = matrix_d[i][j]
        h_ij = trans_kernel(d_ij)
        state_j = 1 if data[j].state == "Infected" else 0
        res += h_ij * state_j
    return res

def cal_p(data, matrix_d, i):
    return 1 - math.exp(-cal_lambda(data, matrix_d, i))

def cal_matrix_d(data):
    n = len(data)
    D = [[0] * n for _ in range(n)] 
    for i in range(n):
        for j in range(i + 1, n):
            x_i, y_i = data[i].x, data[i].y
            x_j, y_j = data[j].x, data[j].y
            D[i][j] = D[j][i] = Euclidean(x_i - x_j, y_i - y_j)
    return D
