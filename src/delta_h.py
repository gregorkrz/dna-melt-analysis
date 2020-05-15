import numpy as np
k1 = float(input('K1: '))
t1 = float(input('T1: ')) + 273.15
k2 = float(input('K2: '))
t2 = float(input('T2: ')) + 273.15

deltaH = -0.008314*np.log(k2/k1) / (1/t2-1/t1)
print(deltaH)
