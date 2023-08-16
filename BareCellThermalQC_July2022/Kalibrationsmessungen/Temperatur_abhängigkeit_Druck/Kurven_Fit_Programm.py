import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

#---------------Curve-Fit---------------#
#define Function
def func(x,m,n):
   return x**2*m+x*n

#get data(every 15 pairs off data the channal changes to the next. So there are 15 pairs of achan0 data and than 15 of achan1 and so on)
path_d = 'Messung_Temp_abhängigkeit_Druck.txt'
datafile = np.loadtxt(path_d, delimiter='\t', unpack=True)
a,da,b,db,c,dc,d,dd,e,de = 0,1,2,3,4,5,6,7,8,9
A,dA,B,dB,C,dC,D,dD,E,dE = datafile[a],datafile[da],datafile[b],datafile[db],datafile[c],datafile[dc],datafile[d],datafile[dd],datafile[e],datafile[de]

r = range(0,len(A))
G=np.array([])
dG=np.array([])

for i in r:
   F=(A[i]/dA[i]**2+B[i]/dB[i]**2+C[i]/dC[i]**2+D[i]/dD[i]**2)/(1/(dA[i]**2)+1/dB[i]**2+1/dC[i]**2+1/dD[i]**2)
   dF=np.sqrt(1/(1/(dA[i]**2)+1/dB[i]**2+1/dC[i]**2+1/dD[i]**2))
   G=np.append(G,F)
   dG=np.append(dG,dF)
  
G=G[45:-1]
E=E[45:-1]
dE=dE[45:-1]

G=G[0]-G
E=E[0]-E

#curve-fit-program
popt,pcov = curve_fit(func,G,E)
errors = np.sqrt(np.diag(pcov))
#print('Steigung: ' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5))+ '\n' + 'y-Achse: ' + str(popt[1].round(5)) + '+/-' + str(errors[1].round(5)))
#print('Nochmal komplett: y=' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5)) + '*x+' + str(popt[1].round(5))+ '+/-' + str(errors[1].round(5)))

#creat fit
xlin = np.linspace(min(G),max(G),1000)
ylin = func(xlin,popt[0],popt[1])

#creat axis and draw function
ax = plt.figure(dpi=350).add_subplot(1,1,1)
#ax.set_facecolor('gainsboro')
plt.errorbar(G,E,xerr=dF,yerr=dE, color='royalblue',fmt='.',label='m = %s +/- %s \nn = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5))))
#plt.errorbar(x,B, color='firebrick',fmt='+',label='Channel 2')
#plt.errorbar(x,C, color='yellow',fmt='+',label='Channel 3')
#plt.errorbar(x,D, color='orangered',fmt='+',label='Channel 4')
#plt.errorbar(x,(E+1.7), color='navy',fmt='+',label='Channel 1b')
plt.plot(xlin,ylin,color='firebrick', label='Fit-Kurve mx²+nx',lw=1.2)

plt.xlabel('Delta T / °C')
plt.ylabel('Delta Gewicht/kg')
plt.legend(loc='best')
plt.grid(True, which='minor',linestyle='--', color='darkgray', lw=0.5)
plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
plt.tight_layout()
plt.savefig("Druckreduktion_durch_Temperatur_Unterschied")

