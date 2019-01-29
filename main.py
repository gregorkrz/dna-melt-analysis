import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import derivative
from scipy.stats import linregress as linear
from scipy import interpolate
import globals
from excel_export import * 
from calculations import * 

minBound = 0.2
maxBound = 0.8


baseline_number_of_points=15
filelist=["in.csv"]
temperatures = np.array([15.0, 90.0])
legend = True
export_images=False
with open('config.txt', encoding="utf-8-sig") as f:
    for line in f.readlines():
        if len(line.rstrip()) > 0 and line.rstrip()[0]!='#':
            key = line.rstrip().split('=')[0]
            val = line.rstrip().split('=')[1].rstrip()
            if key == 'filename': filelist=val.split(',')
            elif key == 'fontsize':
                plt.rcParams.update({'font.size': int(val)})
            elif key == 'temperature_range' and len(val.split(','))==2:
                val = val.split(",")
                temperatures = np.array([int(val[0]), int(val[1])])
            elif key == 'legend' and val == 'off':
                legend = False
            elif key == 'baseline_number_of_points':
                baseline_number_of_points = int(val)
            elif key == 'export_images' and val == 'on':
                export_images=True


for fname in filelist:
    content = []
    data_set_current = []
    Tcurrent = []
    Acurrent = []
    dna_conc_current = []
    with open(fname, encoding="cp1252") as f:
        content = f.readlines()

    first_row = True

    for line in content:
        x = line.rstrip().split(',')
        if all_same(x) and x[0]=='': break
        if x[0] != 'Temperature (°C)':
            if first_row:
                first_row = False
                for i in range(int(len(x)/2)):
                    if len(filelist) > 1: data_set_current.append("["+fname.split(".")[0]+"] "+x[2*i].rstrip())
                    else: data_set_current.append(x[2*i].rstrip())
                    if x[2*i+1].rstrip() != '': dna_conc_current.append(float(x[2*i+1].rstrip()))
                    else : dna_conc_current.append(2)
                    Tcurrent.append([])
                    Acurrent.append([])
            else:
                for i in range(len(data_set_current)):
                    if x[2*i] != '':
                        Tcurrent[i].append(float(x[2*i]))
                        Acurrent[i].append(float(x[2*i+1]))
    T += Tcurrent
    A += Acurrent
    dna_conc += dna_conc_current
    data_set += data_set_current

T = np.array(T)
A = np.array(A)


Ts = (np.linspace(temperatures.min(), temperatures.max(), num=300, endpoint=False))


for i in range(len(data_set)):
    temp = interpolate.interp1d(T[i], A[i], kind=3, fill_value='extrapolate')
    interpolated.append(temp)


odvodi = calc_der(data_set, interpolated, Ts)

baseline, ff = baseline_calc(baseline_number_of_points)

TMs = []
TMIs = []



for i in range(len(ff)):
    for j in range(1,len(ff[i])):
        if (ff[i][j-1] > 0.5 and ff[i][j] <= 0.5) or (ff[i][j] > 0.5 and ff[i][j-1] <= 0.5):
            TMs.append(linear_fit(
                T[i][j], T[i][j-1], ff[i][j], ff[i][j-1]
            ))
            TMIs.append([i, j])
            break


Ka = (1-ff)*(1-ff)/ff

for i in range(len(Ka)):
     Ka[i] = dna_conc[i]*Ka[i]*1e-6
Ka = 1/Ka
Ka2 = []
FROM = []
TO = []
for i in range(len(ff)):
    FROM.append(0)
    TO.append(0)
    for y in range(len(ff[i])):
        if(ff[i][0] > 0.5):
            if (ff[i][y] > minBound): TO[i] = y
            if (ff[i][y] > maxBound): FROM[i] = y
        else:
            if (ff[i][y] < minBound): FROM[i] = y
            if (ff[i][y] < maxBound): TO[i] = y


for i in range(len(Ka)):
    Ka2.append(Ka[i][FROM[i]:TO[i]])

Ka2 = np.array(Ka2)

## get Tm from dH, dS and Km ##


def drawAbs(ans, lst, savefig=False, name=''):
    global legend, baseline
    plt.figure()
    plt.xlabel("T [°C]")
    plt.ylabel("absorbance")
    for i in lst:
        if (ans != 2):
            plt.plot(T[i], A[i], ".", label=data_set[i])
        else:
            plt.plot(Ts, interpolated[i](Ts), "-", label=data_set[i])
        if (ans >= 1): plt.plot(Ts, Ts * baseline[i][0] + baseline[i][1], "--", color='gray')
        if (ans >= 1): plt.plot(Ts, Ts * baseline[i][2] + baseline[i][3], "--", color='gray')
    # if(ans>=1): plt.plot(Ts,Ts*(baseline[i][2]+baseline[i][0])/2+(baseline[i][3]+baseline[i][1])/2,"--",color='k') # average of both baselines (for determining Tm)
    if legend: plt.legend()
    if not savefig: plt.show()
    else:
        plt.savefig('OUT/'+name+'.png')
        plt.close()



for i in range(len(data_set)):
    if export_images: drawAbs(1, [i], True, data_set[i])

while True:
    print("0: Absorbance vs Temperature\n\t\t + baselines (1)\n\t\t + interpolated (2)\n((3: Derivative of absorbance vs Temperature))\n4: Fraction folded vs Temperature\n((5: lnKa(1/T)))\n((6: theor. graph))\nq: quit")
    ans = (input())
    if(ans == 'q'): break
    ans = int(ans)
    print("--------")
    for i in range(len(data_set)):
        print(str(i) + ": "+ data_set[i])
    inp = input()
    lst = []
    
    if len(inp.split("="))==2 and inp.split("=")[0]=='f':
        # include all oligos that include the text after "f="
        t = inp.split("=")[1].split(",")
        for i in range(len(data_set)):
            q = data_set[i]
            current = True
            for j in t:
                if j not in q:
                    current = False
            if current: lst.append(i)
    elif len(inp.split("-"))==2:
        t = inp.split("-")
        t[0]=int(t[0])
        t[1]=int(t[1])
        for i in range(t[1]-t[0]):
            lst.append(t[0]+i)
    else: lst = (inp.split(','))
    print("--------")
    for i in range(len(lst)):
        lst[i] = int(lst[i])
    if(ans == 0 or ans == 1 or ans == 2):
        drawAbs(ans,  lst)
        room_temp = 25
        if ans == 1:
            print("Absorbance values at room temperature:")
        for i in lst:
            print(data_set[i], "\t", baseline[i][0]*room_temp+baseline[i][1], "\t", baseline[i][2]*room_temp+baseline[i][3])
    elif ans == 3:
        plt.figure()
        plt.xlabel("T [°C]")
        plt.ylabel("dA/dT")
        for i in lst:
            plt.plot(Ts, odvodi[i], "-", label=data_set[i])
        if legend: plt.legend()
        plt.show()

    elif ans == 4:

        plt.figure()
        plt.xlabel("T [°C]")
        plt.ylabel("Ф")
        w = ExcelWriter()
        w.addWorksheet('fracFold(T)')
        Tm_table = [[],[]]
        for i in lst:
            plt.plot(T[i], ff[i], ".", label=data_set[i])
            Tm_table[0].append(data_set[i])
            Tm_table[1].append((round(TMs[i], 2)))
            w.writeTable([T[i].tolist(), ff[i].tolist()], [data_set[i], ''])
            print("Tm (", data_set[i], ") = ", str(round(TMs[i], 2)))
        w.writeTable(Tm_table, ['sample', 'Tm'])
        w.close()
        if legend: plt.legend()
        plt.show()
    elif ans == 5:
        plt.figure()
        plt.xlabel("1/T [1/K]")
        plt.ylabel("$lnK_a$")
        for i in lst:
            plt.plot(1/(T[i][FROM[i]:TO[i]]+273.15),np.log(Ka2[i]),".",label=data_set[i])
            tk, tn, _, _, _=linear(1/(T[i][FROM[i]:TO[i]]+273.15),np.log(Ka2[i]))
            plt.plot(1/(T[i][FROM[i]:TO[i]]+273.15),tk*(1/(T[i][FROM[i]:TO[i]]+273.15))+tn,"--",color=(0.8,0.8,0.8))
            print("ΔH ("+data_set[i]+") = "+str(round(tk*-0.008314))+" kJ/mol")
            print("ΔS ("+data_set[i]+") = "+str(round(tn*8.314))+" J/(molK)")
            print("Tm (corrected to 2uM) (" + data_set[i] + ") =", round(getTmCorrection((tk*-0.008314), (tn*8.314), dna_conc[i]), 2))
        if legend: plt.legend()
        plt.show()
    elif ans == 6:
        plt.figure()
        plt.xlabel("T [°C]")
        plt.ylabel("fraction folded")
        for i in lst:
            tk, tn, a1, a2, a3 = linear(1 / (T[i][FROM[i]:TO[i]] + 273.15), np.log(Ka2[i]))
            H = (tk * -0.008314)
            S = (tn * 0.008314)
            Ks = np.exp((H-(Ts+273.15)*S)/(-0.008314*(Ts+273.15)))
            A=dna_conc[i]*1e-6*Ks
            B = -2*dna_conc[i]*1e-6*Ks-1
            C=dna_conc[i]*1e-6*Ks
            D=quad(A,B,C)
            plt.plot(Ts, D, "--", color="gray")
            plt.plot(T[i], ff[i], ".", label=data_set[i])
        if legend: plt.legend()
        plt.show()
    elif ans == 7:
        # manual baseline determination
        break


