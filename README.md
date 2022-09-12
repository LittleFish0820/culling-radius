# Random SEIDR



参考论文：Risk based culling for highly infectious diseases of livestock



## 五种状态

- S (Susceptible) 易感状态
- E (Exposed) 潜伏状态
- I (Infected) 具有传染性的状态
- D (Detected) 检测出疫情
- R (Removed) 被移除



## E to I

**1）传播核函数**
$$
h(d_{ij})=\frac{h_0}{1+(d_{ij}/d_0)^\alpha}
$$
**2）被感染力度**
$$
\lambda_i(t)=\sum\limits_{j\in N(i)}h(d_{ij})I(j)
$$
**3）被感染概率**
$$
p_i(t)=1-e^{\lambda_i(t)}
$$


## I to E

**时间分布**
$$
t_d-t_i\sim Ga(7,1),\quad t_d>t_i
$$


## E的风险值

**1) 具有传染性的养殖场的再生数**
$$
R_i=\sum\limits_{j\in N(i)}\bigg(1-\big(\frac{\beta}{\beta + T\cdot h(d_{ij})}\big)^\beta\bigg)
$$
**2) 易感养殖场的风险值**
$$
E_i = R_i \cdot p_i 
$$
**3) 风险值估计** 
$$
\hat\lambda_i(t)=\sum\limits_{j\in N(i)}h(d_{ij})\big(T-\min(t-t_{jd},T)\big)
$$


## 模拟过程

1. 生成地图
2. 选择初始传染源
3. 模拟传播过程
4. 发现疫情并执行策略，同时传播也在继续
5. 直到没有新增，模拟结束



