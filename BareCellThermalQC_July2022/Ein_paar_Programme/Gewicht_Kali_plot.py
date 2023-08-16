import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

#---------------Curve-Fit---------------#
#define Function
def func(x,m,n):
   return x*m+n

#get data(every 15 pairs off data the channal changes to the next. So there are 15 pairs of achan0 data and than 15 of achan1 and so on)
#path_d = 'Gegen_Kalibration_Werte_1.txt'
#datafile = np.loadtxt(path_d, delimiter='\t', unpack=True)
#a,b,c,d = 12,14,13,15
#A1,B1,C1,D1 = datafile[a],datafile[b],datafile[c],datafile[d]

#A=np.sort(A1)
#B=np.sort(B1)
#C=np.sort(C1)
#D=np.sort(D1)

A=[4.75,9.25,15.5,21,26.5,32,37.5,43]
B=[0.0104,0.0222,0.0348,0.0454,0.0568,0.0685,0.0789,0.0903]

x = np.array([])
for i in range(0,150):
   x = np.append(x,i)

#curve-fit-program
popt,pcov = curve_fit(func,A,B)
errors = np.sqrt(np.diag(pcov))
print('Steigung: ' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5))+ '\n' + 'y-Achse: ' + str(popt[1].round(5)) + '+/-' + str(errors[1].round(5)))
print('Nochmal komplett: y=' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5)) + '*x+' + str(popt[1].round(5))+ '+/-' + str(errors[1].round(5)))

#creat fit
xlin = np.linspace(min(A),max(A),100)
ylin = func(xlin,popt[0],popt[1])

#creat axis and draw function
ax = plt.figure(dpi=350).add_subplot(1,1,1)
#ax.set_facecolor('gainsboro')
plt.errorbar(A,B, color='royalblue',fmt='+',label='m = %s +/- %s \nn = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5))))
#plt.errorbar(x,B, color='firebrick',fmt='+',label='Channel 2')
#plt.errorbar(x,C, color='yellow',fmt='+',label='Channel 3')
#plt.errorbar(x,D, color='orangered',fmt='+',label='Channel 4')
#plt.errorbar(x,(E+1.7), color='navy',fmt='+',label='Channel 1b')
plt.plot(xlin,ylin,color='firebrick', label='Fit-Gerade',lw=1.2)

plt.xlabel('Messung')
plt.ylabel('Volt')
plt.legend(loc='best')
plt.grid(True, which='minor',linestyle='--', color='darkgray', lw=0.5)
plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
plt.tight_layout()
plt.savefig("Messung_aller_Werte_angepasst_mehr")

