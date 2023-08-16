import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

#---------------Curve-Fit---------------#
#define Function
def func(x,m,n):
   return x*m+n

#get data(every 15 pairs off data the channal changes to the next. So there are 15 pairs of achan0 data and than 15 of achan1 and so on)
#path_d = 'Messung_Soft_PGS.txt'
#datafile = np.loadtxt(path_d, delimiter='\t', unpack=True)
#a,b,c = 0,6,8
#A1,B1,C = datafile[a],datafile[b],datafile[c]
A=[0.994e-3,1.994e-3,2.993e-3,3.992e-3,5.990e-3,7.990e-3,9.993e-3,11.996e-3]
dA=[(0.994*0.00045+0.002)*10**(-3),(1.994*0.00045+0.002)*10**(-3),(2.993*0.00045+0.002)*10**(-3),(3.992*0.00045+0.002)*10**(-3),(5.990*0.00045+0.002)*10**(-3),(7.990*0.00045+0.002)*10**(-3),(9.993*0.00045+0.002)*10**(-3),(11.996*0.00045+0.002)*10**(-3)]
dB=[(0.099283*0.012+0.0003),(0.198688*0.012+0.0003),(0.29807*0.012+0.0003),(0.3974*0.012+0.0003),(0.59616*0.012+0.0003),(0.79516*0.012+0.0003),(0.99434*0.012+0.0003),(1.19356*0.012+0.0003)]
dC=[(0.099497*0.012+0.0003),(0.199143*0.012+0.0003),(0.29872*0.012+0.0003),(0.3983*0.012+0.0003),(0.59752*0.012+0.0003),(0.79697*0.012+0.0003),(0.9966*0.012+0.0003),(1.19627*0.012+0.0003)]
dD=[(0.099693*0.012+0.0003),(0.19947*0.012+0.0003),(0.29923*0.012+0.0003),(0.39894*0.012+0.0003),(0.59846*0.012+0.0003),(0.79823*0.012+0.0003),(0.99817*0.012+0.0003),(1.19818*0.012+0.0003)]
dE=[(0.09949*0.012+0.0003),(0.199074*0.012+0.0003),(0.2986*0.012+0.0003),(0.39812*0.012+0.0003),(0.59723*0.012+0.0003),(0.79657*0.012+0.0003),(0.9961*0.012+0.0003),(1.19567*0.012+0.0003)]
B=[0.099283,0.198688,0.29807,0.3974,0.59616,0.79516,0.99434,1.19356]
C=[0.099497,0.199143,0.29872,0.3983,0.59752,0.79697,0.9966,1.19627]
D=[0.099693,0.19947,0.29923,0.39894,0.59846,0.79823,0.99817,1.19818]
E=[0.09949,0.199074,0.2986,0.39812,0.59723,0.79657,0.9961,1.19567]


x = np.array([])
for i in range(0,150):
   x = np.append(x,i)

#curve-fit-program
popt,pcov = curve_fit(func,A,B,sigma=dB)
errors = np.sqrt(np.diag(pcov))
popt1,pcov1 = curve_fit(func,A,C,sigma=dC)
errors1 = np.sqrt(np.diag(pcov))
popt2,pcov2 = curve_fit(func,A,D,sigma=dD)
errors2 = np.sqrt(np.diag(pcov))
popt3,pcov3 = curve_fit(func,A,E,sigma=dE)
errors3 = np.sqrt(np.diag(pcov))
#print('Steigung: ' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5))+ '\n' + 'y-Achse: ' + str(popt[1].round(5)) + '+/-' + str(errors[1].round(5)))
#print('Nochmal komplett: y=' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5)) + '*x+' + str(popt[1].round(5))+ '+/-' + str(errors[1].round(5)))

#creat fit
xlin = np.linspace(min(A),max(A),1000)
ylin = func(xlin,popt[0],popt[1])
ylin1 = func(xlin,popt1[0],popt1[1])
ylin2 = func(xlin,popt2[0],popt2[1])
ylin3 = func(xlin,popt2[0],popt3[1])

#creat axis and draw function
ax = plt.figure(dpi=350).add_subplot(1,1,1)
#ax.set_facecolor('gainsboro')
#plt.errorbar(A,, color='royalblue',fmt='+',label='m = %s +/- %s \nn = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5))))
plt.errorbar(A,B, color='firebrick',fmt='.',label='m = %s +/- %s \nn = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5))))
plt.errorbar(A,C, color='yellow',fmt='.',label='m = %s +/- %s \nn = %s +/- %s'%(str(popt1[0].round(5)),str(errors1[0].round(5)),str(popt1[1].round(5)),str(errors1[1].round(5))))
plt.errorbar(A,D, color='orangered',fmt='.',label='m = %s +/- %s \nn = %s +/- %s'%(str(popt2[0].round(5)),str(errors2[0].round(5)),str(popt2[1].round(5)),str(errors2[1].round(5))))
plt.errorbar(A,E, color='navy',fmt='.',label='m = %s +/- %s \nn = %s +/- %s'%(str(popt3[0].round(5)),str(errors3[0].round(5)),str(popt3[1].round(5)),str(errors3[1].round(5))))
plt.plot(xlin,ylin,color='firebrick', label='Fit-Gerade Widerstand 1',lw=1.2)
plt.plot(xlin,ylin1,color='yellow', label='Fit-Gerade Widerstand 2',lw=1.2)
plt.plot(xlin,ylin2,color='orangered', label='Fit-Gerade Widerstand 3',lw=1.2)
plt.plot(xlin,ylin3,color='navy', label='Fit-Gerade Widerstand 4',lw=1.2)

plt.xlabel('I / A')
plt.ylabel('U / V')
plt.legend(loc='best')
plt.grid(True, which='minor',linestyle='--', color='darkgray', lw=0.5)
plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
plt.tight_layout()
plt.savefig("Widerstands_Kalibration_f")

