#!python3.6
import threading
import fileinput
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress as linear
from scipy import interpolate
#fname = input("Filename: ")
fname = "data/arhiv/cd5.csv"
content = open(fname).readlines()
print(len(content))
wavelen = []
temp = []
cd = [] # podarrayi so za vsako valovno dolžino

#color_profile = [98, 114, 196] # original
color_profile = [226,170,0] # mutation 1 v2
#color_profile = [91,155,213] #mut2 ver1
#color_profile = [255,80,80] # mut2 ver2

for i in range(len(color_profile)):
    color_profile[i] = color_profile[i]/255

c = -1
def export(table):

    f = open('export.txt','w')
    for i in table:
        print(i)
        for y in range(len(i[0])):
            f.write(str(i[0][y]))
            f.write('\t')
            f.write(str(i[1][y]))
            f.write('\n')
        f.write('\n\n')
group = 5

for z in content:
    i = z.strip('\n')
    if(i.startswith("CircularDichro")):
        c+=1
    elif(c==1):
        c=2
    elif(c==2):
        for a in i.split(","):
            if(len(a)>0):
                temp.append(round(float(a)))
        for i in range(len(temp)): cd.append([])
        c=3
    elif(i=='' and c >= 3):
        break
    elif(c==3):
        t = i.split(",")
        print(t)
        wavelen.append(int(t[0]))
        cd.append([])
        k = len(cd)-1
        for j in range(len(temp)):
            cd[j].append(float(t[j+1]))



def grouped(cd,lamb):
    ret = [[],[]]
    c=0
    tc=0
    tl=0
    for i in range(len(cd)):
        if(c==group):
            c=0
            ret[0].append(tc/group)
            ret[1].append(tl/group)
            tc=0
            tl=0
        else:
            tc += cd[i]
            tl += lamb[i]
            c+=1

    return ret

def interp(cd,lamb):
    return interpolate.interp1d(lamb, cd, kind=3, fill_value='extrapolate')


def cdgraph():
    alpha=1
    plt.figure(figsize=(9.5,7))
    for i in range(len(temp)):
        a=grouped(cd[i],wavelen)
        b=interp(a[0],a[1])
        c=np.linspace(214, 315, num=500)
        
        plt.plot(c,b(c)/2,"-",label=str(temp[i]),color        =(color_profile[0], color_profile[1], color_profile[2], alpha))

        #export([[c, b(c)]])
        #plt.plot(c,b(c),"-",label=str(temp[i]))

        alpha=alpha-1/18*alpha
    plt.xlabel("λ [nm]",fontsize=23)
    plt.ylabel("CD [mdeg]",fontsize=23)
    plt.axis([200,320,-15,20],fontsize=23)
    plt.tick_params(axis='both', which='major', labelsize=23)
    plt.tick_params(axis='both', which='minor', labelsize=23)
    plt.grid()
    plt.show()

def cwl(wl):
    t = wavelen.index(wl)
    graph=[]
    for i in range(len(temp)):
        graph.append(cd[i][t])
    plt.figure()
    #plt.axis([0,80,0,10])

    plt.plot(temp,graph,"-")
    plt.show()

cdgraph()





