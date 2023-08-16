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
path_d = 'Kalibration_ADC1_4.096V_ADC2_4.096V_ADC3_4.096V.txt'
datafile = np.loadtxt('Kalibration_ADC1_4.096V_ADC2_4.096V_ADC3_4.096V.txt', delimiter='	', unpack=True)
a,da = 2,3
A,dA = datafile[a],datafile[da]

B=np.array([])
dB=np.array([])

for i in np.arange(0,21):
	B = np.append(B,[0.165*i])
print(B)

dB=B*0.0001+0.002+B*0.0005+0.005

#curve-fit-program
popt,pcov = curve_fit(func,B,A,sigma=dA+0.0001)
errors = np.sqrt(np.diag(pcov))
#print('Steigung: ' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5))+ '\t' + 'y-Achse: ' + str(popt[1].round(5)) + '+/-' + str(errors[1].round(5)))
#print('Nochmal komplett: y=' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5)) + '*x+' + str(popt[1].round(5))+ '+/-' + str(errors[1].round(5)) + '\n')

#creat fit
xlin = np.linspace(min(B), max(B),100)
ylin = func(xlin,popt[0],popt[1])

#creat axis and draw function
ax = plt.figure(dpi=350).add_subplot(1,1,1)

plt.errorbar(B,A,xerr=dB,yerr=dA, color='royalblue',fmt='.',label='m = %s +/- %s \nn = %s +/- %s '%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5))))
plt.plot(xlin,ylin,color='firebrick', label='Fit-Gerade',lw=1.2)

plt.ylabel('ADC Counts')
plt.xlabel('Spannung Power Supply / V')
plt.grid(True, which='minor',linestyle='--', color='darkgray', lw=0.5)
plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
plt.legend(loc='best')	
plt.tight_layout()
plt.savefig('ADC1_channal1_4,096V_gegen_counts.png')

