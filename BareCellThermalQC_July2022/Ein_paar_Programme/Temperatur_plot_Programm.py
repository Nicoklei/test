import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

#---------------Curve-Fit---------------#
#define Function
def func(x,m,n):
   return x*m+n

#get data(every 15 pairs off data the channal changes to the next. So there are 15 pairs of achan0 data and than 15 of achan1 and so on)
path_d = 'Vollständige_Temp_Kurve_Übernacht_Vakuum2.txt'
datafile = np.loadtxt(path_d, delimiter='\t', unpack=True)
a,da,b,db,c,dc,d,dd = 0,1,2,3,4,5,6,7
A,dA,B,dB,C,dC,D,dD = datafile[a],datafile[da],datafile[b],datafile[db],datafile[c],datafile[dc],datafile[d],datafile[dd]


x = np.array([])
for i in range(0,len(A)):
   x = np.append(x,i)

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
plt.errorbar(x,A,yerr=dA, color='royalblue',fmt='.',label='Temperatur oben')#'m = %s +/- %s \nn = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5))))
plt.errorbar(x,B,yerr=dB, color='firebrick',fmt='.',label='Temperatur mitte oben')
plt.errorbar(x,C,yerr=dC, color='yellow',fmt='.',label='Temperatur mitte unten')
plt.errorbar(x,D,yerr=dD, color='orangered',fmt='.',label='Temperatur unten')
#plt.errorbar(x,(E+1.7), color='navy',fmt='+',label='Channel 1b')
#plt.plot(xlin,ylin,color='firebrick', label='Fit-Gerade',lw=1.2)

plt.xlabel('Messung')
plt.ylabel('Temperatur / °C')
plt.legend(loc='best')
plt.grid(True, which='minor',linestyle='--', color='darkgray', lw=0.5)
plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
plt.tight_layout()
plt.savefig("Temperaturkurve_langzeit_2")

ax = plt.figure(dpi=350).add_subplot(1,1,1)
#ax.set_facecolor('gainsboro')
plt.errorbar(x,A, color='royalblue',fmt='-',label='Temperatur oben')#'m = %s +/- %s \nn = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5))))
plt.errorbar(x,B, color='firebrick',fmt='-',label='Temperatur mitte oben')
plt.errorbar(x,C, color='yellow',fmt='-',label='Temperatur mitte unten')
plt.errorbar(x,D, color='orangered',fmt='-',label='Temperatur unten')
#plt.errorbar(x,(E+1.7), color='navy',fmt='+',label='Channel 1b')
#plt.plot(xlin,ylin,color='firebrick', label='Fit-Gerade',lw=1.2)

plt.xlabel('Messung')
plt.ylabel('Temperatur / °C')
plt.legend(loc='best')
plt.grid(True, which='minor',linestyle='--', color='darkgray', lw=0.5)
plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
plt.tight_layout()
plt.savefig("Temperaturkurve_ohne_Fehler_langzeit_2")
