# -*- coding: utf-8 -*-
import numpy as np
import math
import matplotlib.pyplot as plt
#plt.style.use()
#matplotlib.rcParams["text.usetex"] = True

def gamma(x, alpha = 7, beta = 1):
    return math.pow(beta, alpha) * math.pow(x, alpha - 1) * math.exp(-beta * x) / math.gamma(alpha)

x = [0.1 * i for i in range(200)]
y = [0] * 200
for i in range(len(x)):
    y[i] = gamma(x[i])

plt.figure(figsize = (5, 3))
plt.plot(x, y, c = 'blue')

plt.xticks(x[::20])
yticks = [0.025 * i for i in range(7)]
plt.yticks(yticks[1:])
plt.grid(True, linestyle = '--', alpha = 0.5)
plt.xlim([0, 20])
plt.ylim([0, 0.17])
plt.title("Probability Density Function of Gamma")
plt.text(10, 0.125, r"$f(x) = \frac{1}{720}x^6e^{-x}$", fontsize = 18)
plt.savefig("./Gamma.jpg")
plt.show()


