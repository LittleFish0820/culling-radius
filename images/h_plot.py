import numpy as np
import math
import matplotlib.pyplot as plt
from myFuns import *

x = [0.1 * i for i in range(60)]
y = [0] * 60
for i in range(len(x)):
    y[i] = trans_kernel(x[i])

plt.figure(figsize = (5, 3))
plt.plot(x, y, c = 'green')

plt.xticks(x[::5])
yticks = [0.0002 * i for i in range(9)]
plt.yticks(yticks[1:])
plt.grid(True, linestyle = '--', alpha = 0.5)
plt.xlim([0, 6])
plt.ylim([0.0001, 0.0017])
plt.title("Transmission Kernel Function")
plt.text(3.0, 0.0014, r"$h_{ij} = \frac{h_0}{1 + (d/d_0)^\alpha}$", fontsize = 18)
plt.text(3.5, 0.0010, r"$h_0 = 0.0016$", fontsize = 12)
plt.text(3.5, 0.0008, r"$d_0 = 1.9$", fontsize = 12)
plt.text(3.5, 0.0006, r"$\alpha = 2.1$", fontsize = 12)
plt.savefig("./h.jpg")
plt.show()