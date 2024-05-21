import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd

#---------------Curve-Fit---------------#
#define Function
def func(x,m,n):
   return x*m+n

#get data(every 15 pairs off data the channal changes to the next. So there are 15 pairs of achan0 data and than 15 of achan1 and so on)
path_d = 'ZW_PDBBareCells_Quali-0_2023-09-28.xlsx'
df = pd.read_excel(path_d, sheet_name=8,skiprows=4, usecols=[3])
datafile = df.to_numpy()

x = np.array([])
A1 = np.array([])
for i in range(0,488):
   x = np.append(x,i)
   A1 = np.append(A1,float(datafile[i]))

print(A1,x,type(x),type(x[1]),type(A1),type(x[1]))

#curve-fit-program
#popt,pcov = curve_fit(func,A,C0-C)
#errors = np.sqrt(np.diag(pcov))
#print('Steigung: ' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5))+ '\n' + 'y-Achse: ' + str(popt[1].round(5)) + '+/-' + str(errors[1].round(5)))
#print('Nochmal komplett: y=' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5)) + '*x+' + str(popt[1].round(5))+ '+/-' + str(errors[1].round(5)))

#creat fit
#xlin = np.linspace(min(A),max(A),1000)
#ylin = func(xlin,popt[0],popt[1])

#creat axis and draw function
ax = plt.figure(dpi=350).add_subplot(1,1,1)
#ax.set_facecolor('gainsboro')
plt.errorbar(x,A1, color='royalblue',fmt='+', label='Datapoint')
plt.plot([0,488],[0.416,0.416],color='black', label='Maximum value',linestyle='dashed')
#plt.errorbar(x,B, color='firebrick',fmt='+',label='Channel 2')
#plt.errorbar(x,C, color='yellow',fmt='+',label='Channel 3')
#plt.errorbar(x,D, color='orangered',fmt='+',label='Channel 4')
#plt.errorbar(x,(E+1.7), color='navy',fmt='+',label='Channel 1b')
#plt.plot(xlin,ylin,color='firebrick', label='Fit-Gerade',lw=1.2)

plt.xlabel('Cooling Block')
plt.ylabel('Mass/g')
plt.legend(loc='best')
plt.grid(True, which='minor',linestyle='--', color='darkgray', lw=0.5)
plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
plt.tight_layout()
plt.savefig("Mass_graph_Cooling Block")

