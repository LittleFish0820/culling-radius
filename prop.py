# -*- coding: utf-8 -*-
from myFuns import *
from collections import *
import matplotlib.pyplot as plt


class farm:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "Susceptible"
        self.time_exposed = -1
        self.time_infected = -1
        self.time_detected = -1
        self.time_removed = -1
        
color_map = {"Susceptible" : "blue", 
             "Exposed"     : "orange",
             "Infected"    : "red",
             "Detected"    : "green",
             "Removed"     : "black"}


def generate_map():
    parent = farm(0, 0)
    data = [parent]
    
    iterator = 1
    
    l_inner = 1
    l_outer = 3
    
    inner_square = l_inner * l_inner
    outer_square = l_outer * l_outer
    
    inner_count = 1
    outer_count = 0
    
    inner_MAX = 100
    outer_MAX = 600
    
    while iterator < inner_MAX + outer_MAX:
        x, y = parent.x, parent.y
        angle = np.random.uniform(0, 360)
        d = np.random.exponential(l_inner) if Euclidean(x, y) <= 1 else np.random.exponential(l_outer)
        off_x = x + d * math.sin(angle)
        off_y = y + d * math.cos(angle)
        
        while True:
            it = 1
            while Euclidean(off_x, off_y) > 25 and it < 40:
                angle = np.random.uniform(0, 360)
                d = np.random.exponential(l_inner) if Euclidean(x, y) <= 1 else np.random.exponential(l_outer)
                off_x = x + d * math.sin(angle)
                off_y = y + d * math.cos(angle)
                it += 1
            if Euclidean(off_x, off_y) > 25:
                index = np.random.randint(0, len(data))
                parent = data[index]
                x, y = parent.x, parent.y
                continue
            break
        
        if Euclidean(off_x, off_y) <= inner_square:
            if inner_count < inner_MAX:
                inner_count += 1
            else:
                continue
        elif Euclidean(off_x, off_y) <= 25:
            if outer_count < outer_MAX:
                outer_count += 1
            else:
                continue
        else:
            continue
        
        parent = farm(off_x, off_y)
        data.append(parent)
        iterator += 1
    
    return data       

def showMap(data):
    n = len(data)
    X = [data[i].x for i in range(n)]
    Y = [data[i].y for i in range(n)]
    color = [color_map[data[i].state] for i in range(n)]
    plt.figure(figsize = (10, 10), dpi = 100)
    plt.grid(True, linestyle = '--', alpha = 0.5)
    plt.scatter(X, Y, s = 12, c = color)
    plt.show()
  
def AItransmission(data):
    #index = np.random.randint(0, len(data))
    index = 0
    data[index].state = "Infected"    
    data[index].time_infected = 0
    
    matrix_d = cal_matrix_d(data)
    
    t = 0
    isDetected = False
    #while t < 21:
    while isDetected == False:    
        P = [0] * len(data)
        for i in range(len(data)):   
            # 计算Susceptible被感染的概率
            if data[i].state == "Susceptible":
                P[i] = cal_p(data, matrix_d, i)
                
        for i in range(len(data)):
            if P[i] > 0:
                # 随机模拟该概率是否成真
                label = select(P[i])
                if label == 1:
                    data[i].state = "Exposed"
                    data[i].time_exposed = t
            # 修改状态
            if data[i].state == "Exposed" and data[i].time_exposed + 2 == t:
                data[i].state = "Infected"
                data[i].time_infected = t
        
        # 给Infected点生成t_d
        for i in range(len(data)):
            if data[i].state == "Infected":
                if data[i].time_detected == -1:
                    t_d = int(np.random.gamma(7, 1))
                    data[i].time_detected = t + t_d
                if data[i].time_detected == t:
                    data[i].state = "Detected"
                    isDetected = True
        
        t += 1
    return data, matrix_d, t

def statistic(data):
    total = [0] * 10
    count = [0] * 10
    for i in range(len(data)):
        r_2 = Euclidean(data[i].x, data[i].y)
        for j in range(9, -1, -1):
            if r_2 <= 0.5 * (j + 1) * 0.5 * (j + 1): 
                total[j] += 1
                if data[i].state in ("Exposed", "Infected", "Detected"):
                    count[j] += 1
            else:
                break
    return total, count

if __name__ == "__main__":
    data = generate_map()
    showMap(data)
    
    data, matrix_d, t = AItransmission(data)
    showMap(data)
    
    total, count = statistic(data)
    ratio = [count[i] / total[i] for i in range(10)]
    
    # 感染个数
    x = [i * 0.5 for i in range(1, 11)]
    plt.figure(figsize = (5, 3))
    plt.plot(x, count, c = 'green')
    plt.show()    

    # 直方图
    diff = [0] * 10
    diff[0] = count[0]
    for i in range(1, 10):
        diff[i] = count[i] - count[i - 1]
    
    plt.figure(figsize = (5, 3))
    plt.bar(x, diff, width = 0.5)
    plt.show()
