import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

#---------------Curve-Fit---------------#
#define Function
def func(x,m,n):
   return x*m+n

#get data(every 15 pairs off data the channal changes to the next. So there are 15 pairs of achan0 data and than 15 of achan1 and so on)
path_d = 'Cross_Kalibration_mehr_Werte.txt'
datafile = np.loadtxt(path_d, delimiter='\t', unpack=True)
a,da,b,db= 12,13,14,15
A,dA,B,dB = datafile[a],datafile[da],datafile[b],datafile[db]


x = np.array([])
for i in range(0,230):
   x = np.append(x,i)

#curve-fit-program
popt,pcov = curve_fit(func,(A*1000),(B*1000-2.215)/2.3359)
errors = np.sqrt(np.diag(pcov))
print('Steigung: ' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5))+ '\n' + 'y-Achse: ' + str(popt[1].round(5)) + '+/-' + str(errors[1].round(5)))
print('Nochmal komplett: y=' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5)) + '*x+' + str(popt[1].round(5))+ '+/-' + str(errors[1].round(5)))

#creat fit
xlin = np.linspace(min(A*1000),max((A*1000)),1000)
ylin = func(xlin,popt[0],popt[1])

#creat axis and draw function
ax = plt.figure(dpi=350).add_subplot(1,1,1)
#ax.set_facecolor('gainsboro')
plt.errorbar((A*1000),(B*1000-2.215)/2.3359,xerr=dA*1000,yerr=np.sqrt((1/2.3359)**2*0.453**2+(1/2.3359)**2*(dB*1000)**2+(((B*1000)-2.215)/2.3359**2)**2*0.01818**2), color='royalblue',fmt='.',label='m = %s +/- %s \nn = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5))))
#plt.errorbar(x,B, color='firebrick',fmt='+',label='Channel 2')
#plt.errorbar(x,C, color='yellow',fmt='+',label='Channel 3')
#plt.errorbar(x,D, color='orangered',fmt='+',label='Channel 4')
#plt.errorbar(x,(E+1.7), color='navy',fmt='+',label='Channel 1b')
plt.plot(xlin,ylin,color='firebrick', label='Fit-Gerade',lw=1.2)

plt.xlabel('Voltausgabe Messzelle / mV')
plt.ylabel('Gewicht Kalibrationszelle / kg')
plt.legend(loc='best')
plt.grid(True, which='minor',linestyle='--', color='darkgray', lw=0.5)
plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
plt.tight_layout()
plt.savefig("Cross_Kalibration_mV_Gewicht_Auftragung.png")

