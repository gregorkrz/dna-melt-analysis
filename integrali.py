'''
Program za risanje grafov odvisnosti integralov od temperature (vhodna datoteka gre not prek standardnega vhoda)

data format:
1. vrstica: title
2. vrstica: T1, T2, T3...
Integral(start,end)
Int(T1)
Int(T2)
...
Integral(start,end)
Int(T1)
Int(T2)
'''
import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import sys
data = []
Xs = False
title = False
Ys = []
for line in sys.stdin:
	a = line.rstrip()
	a = a.upper()
	if(title == False):
		title = a
	elif(Xs == False):
		Xs = a.split(',')
		for i in range(len(Xs)):
			Xs[i] = float(Xs[i])
	elif(a == ''): pass
	elif(a.startswith('INTEGRAL(')):
		j = a.find('(')+1
		k = a.find(')')
		b = a[j:k].split(',')
		if(len(b)==1):
			b[0] = str(round(float(b[0]),2))
			data.append(b[0]+"ppm")
		elif(b[0] == 'custom'):
			data.append(b[1])
		else:
			b[0] = str(round(float(b[0]),2))
			b[1] = str(round(float(b[1]),2))
			data.append(b[0]+"-"+b[1]+"ppm")
		Ys.append([])
	else:
		l = len(Ys)-1
		Ys[l].append(float(line))

mi = Xs.index(min(Xs))
for i in range(len(Ys)):
	a = float(Ys[i][mi])
	for j in range(len(Ys[i])):
		Ys[i][j] = float(Ys[i][j])
		Ys[i][j] = 100 * Ys[i][j]/a

avg = []
print(data)
print(Xs)
print(Ys)
for i in range(len(Xs)):
	avg.append(0)
	for j in range(len(data)):
		avg[i] += Ys[j][i]
	avg[i] = avg[i]/(len(data))



Xs = np.array(Xs)
Ys = np.array(Ys)
avg = np.array(avg)
mpl.rcParams.update({'font.size': 10})
for i in range(len(data)):
	plt.plot(Xs,Ys[i],linewidth=1.5,linestyle="--",marker=".",label=data[i])
plt.plot(Xs,avg,linewidth=1.5,linestyle="--",marker=".",label='avg')
plt.grid()
plt.xlabel("T [°C]")
plt.ylabel("integral (5°C = 100%)")
plt.legend()
plt.title(title)
plt.show()
