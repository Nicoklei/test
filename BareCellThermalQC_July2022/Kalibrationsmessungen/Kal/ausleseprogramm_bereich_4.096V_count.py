import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

N=0
n=15
start=n-1
run = 0
#---------------Curve-Fit---------------#
#define Function
def func(x,m,n):
   return x*m+n

#get data(every 15 pairs off data the channal changes to the next. So there are 15 pairs of achan0 data and than 15 of achan1 and so on)
datafile = np.loadtxt('Kalibration_ADC1_4.096V_ADC2_4.096V_ADC3_4.096V.txt', delimiter='	', unpack=True)
a,da,b,db = 36,37,38,39#32,33,34,35#28,29,30,31#24,25,26,27#20,21,22,23#16,17,18,19#12,13,14,15#8,9,10,11#4,5,6,7#0,1,2,3
A,dA,B,dB = datafile[a],datafile[da],datafile[b],datafile[db]

#curve-fit-program
popt,pcov = curve_fit(func,B,A,sigma=(dA+0.0001))
errors = np.sqrt(np.diag(pcov))
#print('Steigung: ' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5))+ '\t' + 'y-Achse: ' + str(popt[1].round(5)) + '+/-' + str(errors[1].round(5)))
#print('Nochmal komplett: y=' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5)) + '*x+' + str(popt[1].round(5))+ '+/-' + str(errors[1].round(5)) + '\n')

#creat fit
xlin = np.linspace(min(B), max(B),1000)
ylin = func(xlin,popt[0],popt[1])

#creat axis and draw function
ax = plt.figure(dpi=350).add_subplot(1,1,1)

plt.errorbar(B,A,xerr=dB,yerr=dA, color='royalblue',fmt='.',label='m = %s +/- %s \nn = (%s +/- %s) V'%(str(popt[0].round(5)),str(errors[0].round(7)),str(popt[1].round(5)),str(errors[1].round(5))))
plt.plot(xlin,ylin,color='firebrick', label='Fit-Gerade',lw=1.2)

plt.ylabel('Gemessene Spannung ADC / V')
plt.xlabel('ADC Counts')
plt.grid(True, which='minor',linestyle='--', color='darkgray', lw=0.5)
plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
plt.legend(loc='best')	
plt.tight_layout()
plt.savefig('ADC3_channal5_4,096V_count.png')
	
