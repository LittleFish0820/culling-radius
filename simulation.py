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
             "Detected"    : "blue",
             "Removed"     : "black"}

def generate_map():
    parent = farm(0, 0)
    data = [parent]
    
    iterator = 1
    l_inner = 1
    l_outer = 3
    
    inner_count = 1
    outer_count = 0
    inner_MAX = 200
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
        
        if Euclidean(off_x, off_y) <= 1:
            if inner_count < inner_MAX:
                inner_count += 1
            else:
                continue
        elif outer_count < outer_MAX:
            outer_count += 1
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
    plt.figure(figsize = (5, 5), dpi = 100)
    plt.grid(True, linestyle = '--', alpha = 0.5)
    plt.xlim([-5.2, 5.2])
    plt.ylim([-5.2, 5.2])
    plt.xticks([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
    plt.yticks([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
    plt.scatter(X, Y, s = 6, c = color)
    plt.show()
    
def start_up(data):
    #index = np.random.randint(0, len(data))
    index = 0
    data[index].state = "Infected"    
    data[index].time_infected = 0
    
    matrix_d = cal_matrix_d(data)
    
    exposed_count = 0
    infected_count = 1
    
    t = 0
    while exposed_count + infected_count < 14:    
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
                    exposed_count += 1
            # 修改状态
            if data[i].state == "Exposed" and data[i].time_exposed + 2 == t:
                data[i].state = "Infected"
                data[i].time_infected = t
                infected_count += 1
                exposed_count -= 1
        t += 1
    return data, matrix_d, t
  
def risk_based_culling(data, matrix_d, start_time):
    t = start_time
    # 扑杀队列
    queDetected = deque()
    
    count = 1
    
    while count > 0:
        
        # 给Infected点生成t_d
        for i in range(len(data)):
            if data[i].state == "Infected":
                if data[i].time_detected == -1:
                    t_d = int(np.random.gamma(2, 1))
                    data[i].time_detected = t + t_d
                if data[i].time_detected == t:
                    data[i].state = "Detected"
                    queDetected.append(i)
                    
        # AI传播
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
        
        # Detected扑杀
        farPoint = [-1, 0]
        Len = len(queDetected)
        
        for c in range(Len):
            cur = queDetected.popleft()
            radius = Euclidean(data[cur].x, data[cur].y)
            if farPoint[1] < radius:
                farPoint[0] = cur
                farPoint[1] = radius
            data[cur].state = "Removed"
            data[cur].time_removed = t
             
        # 预防扑杀

        R = [[0, -1] for _ in range(len(data))]
        for i in range(len(data)):
            R[i][0] = i
            if data[i].state == "Detected" or data[i].state == "Removed":
                continue
            R[i][1] = estimate_E(data, matrix_d, i, t)
        R.sort(key = lambda x : -x[1])
        for c in range(10 * Len):
            radius = Euclidean(data[R[c][0]].x, data[R[c][0]].y)
            if farPoint[1] < radius:
                farPoint[0] = cur
                farPoint[1] = radius            
            data[R[c][0]].state = "Removed"
            data[R[c][0]].time_removed = t
        
        for i in range(len(data)):
            radius = Euclidean(data[i].x, data[i].y)
            if radius <= 1.2 * farPoint[1] and data[i].state != "Removed":
                data[i].state = "Removed"
                data[i].time_removed = t
            
        count = 0
        for i in range(len(data)):
            if data[i].state == "Exposed" or data[i].state == "Infected":
                count += 1
                
        t += 1
    
    return data, t

if __name__ == "__main__":
    
    data = generate_map()
    #showMap(data)
    
    data, matrix_d, t = start_up(data)
    showMap(data)
    
    data, t = risk_based_culling(data, matrix_d, t)
    showMap(data)
    
    
    

