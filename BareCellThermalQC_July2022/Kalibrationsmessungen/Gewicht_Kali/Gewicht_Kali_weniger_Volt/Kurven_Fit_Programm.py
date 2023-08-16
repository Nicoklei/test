import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

#---------------Curve-Fit---------------#
#define Function
def func(x,m,n):
   return x*m+n

#get data(every 15 pairs off data the channal changes to the next. So there are 15 pairs of achan0 data and than 15 of achan1 and so on)
path_d = 'Gewicht_Kalibration_Zelle_1.txt'
datafile = np.loadtxt(path_d, delimiter='\t', unpack=True)
a,b = 12,13
A1,B1 = datafile[a],datafile[b]

A=[43,37.5,32,26.5,23.75,21,18,15.5,13,9.25,4.75]

werte = np.array([])
werte1 = np.array([])
B = np.array([])
dB = np.array([])
i=0
while i < 11:
   werte = A1[3+15*i:12+15*i]
   werte1 = np.append(werte1,B1[3+15*i:12+15*i])
   B=np.append(B,np.sum(A1[3+15*i:12+15*i])/10)
   dB=np.append(dB,np.sum(B1[3+15*i:12+15*i])/10)
   i += 1

#print(B,dB)

#A=np.sort(A1)
#B=np.sort(B1)
#C=np.sort(C1)
#D=np.sort(D1)



x = np.array([])
for i in range(0,130):
   x = np.append(x,i)

#curve-fit-program
popt,pcov = curve_fit(func,A,(B*1000)/4)
errors = np.sqrt(np.diag(pcov))
print('Steigung: ' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5))+ '\n' + 'y-Achse: ' + str(popt[1].round(5)) + '+/-' + str(errors[1].round(5)))
print('Nochmal komplett: y=' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5)) + '*x+' + str(popt[1].round(5))+ '+/-' + str(errors[1].round(5)))

#creat fit
xlin = np.linspace(min(A),max(A),100)
ylin = func(xlin,popt[0],popt[1])

#creat axis and draw function
ax = plt.figure(dpi=350).add_subplot(1,1,1)
#ax.set_facecolor('gainsboro')
plt.errorbar(A,(B*1000)/4,yerr=(dB*1000)/4, color='royalblue',fmt='.',label='m = %s +/- %s \nn = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5))))
#plt.errorbar(x,B, color='firebrick',fmt='+',label='Channel 2')
#plt.errorbar(x,C, color='yellow',fmt='+',label='Channel 3')
#plt.errorbar(x,D, color='orangered',fmt='+',label='Channel 4')
#plt.errorbar(x,(E+1.7), color='navy',fmt='+',label='Channel 1b')
plt.plot(xlin,ylin,color='firebrick', label='Fit-Gerade',lw=1.2)

plt.xlabel('Gewicht / kg')
plt.ylabel('Ausgangsspannung / mV/V')
plt.legend(loc='best')
plt.grid(True, which='minor',linestyle='--', color='darkgray', lw=0.5)
plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
plt.tight_layout()
plt.savefig("Kalibration_Zelle1_4V_mVV.png")

