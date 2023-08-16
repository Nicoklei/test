import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

#---------------Curve-Fit---------------#
#define Function
def func(x,m,n,d):
   return n*np.exp(-m*x)+d

#get data(every 15 pairs off data the channal changes to the next. So there are 15 pairs of achan0 data and than 15 of achan1 and so on)
path_d = 'Lambda Messungen/Alu_Temp_nicht_vertauscht/Gemittelte_Werte_Aluminium_Tempsensoren_richtig.txt'
datafile = np.loadtxt(path_d, delimiter='\t', unpack=True)
a,da,b,db,c,dc,d,dd = 0,1,4,5,2,3,6,7
A,dA,B,dB,C,dC,D,dD = datafile[a],datafile[da],datafile[b],datafile[db],datafile[c],datafile[dc],datafile[d],datafile[dd]
path_d1 = 'Lambda Messungen/Aluminium_gegen_20_09/Gemittelte_Werte_Aluminium_gegen_Druck_20_09.txt'
datafile1 = np.loadtxt(path_d1, delimiter='\t', unpack=True)
A3,dA3,B3,dB3,C3,dC3,D3,dD3 = datafile1[a],datafile1[da],datafile1[b],datafile1[db],datafile1[c],datafile1[dc],datafile1[d],datafile1[dd]
path_d2 = 'Lambda Messungen/Aluminium/Messung_Lambda_Aluminium_25_08.txt'
datafile2 = np.loadtxt(path_d2, delimiter='\t', unpack=True)
A2,dA2,B2,dB2,C2,dC2,D2,dD2 = datafile2[a],datafile2[da],datafile2[b],datafile2[db],datafile2[c],datafile2[dc],datafile2[d],datafile2[dd]
path_d6 = 'Lambda Messungen/Aluminium_gegen_21_09/Gemittelte_Werte_Aluminium_gegen_Druck_21_09.txt'
datafile6 = np.loadtxt(path_d6, delimiter='\t', unpack=True)
A6,dA6,B6,dB6,C6,dC6,D6,dD6 = datafile6[a],datafile6[da],datafile6[b],datafile6[db],datafile6[c],datafile6[dc],datafile6[d],datafile6[dd]


A1=(9.809*A/(0.0001*np.pi))*10**(-3)
dA1=(9.809/(0.0001*np.pi))*dA*10**(-3)
#B=0.0002*(1/((0.0037*2+0.0002)/B0-(0.0037*2)/160))*(10**(4))
B1=(0.0086/B-0.0076/C)*(10**4)
dB1=np.sqrt((0.0086/(B)**2)**2*(dB)**2+(0.0076/(C)**2)**2*(dC)**2+(1/(B)-1/(C))**2*(0.0002)**2)*10**4

A4=(9.809*A3/(0.0001*np.pi))*10**(-3)
dA4=(9.809/(0.0001*np.pi))*dA3*10**(-3)
#B=0.0002*(1/((0.0037*2+0.0002)/B0-(0.0037*2)/160))*(10**(4))
B4=(0.0086/B3-0.0076/C3)*(10**4)
dB4=np.sqrt((0.0086/(B3)**2)**2*(dB3)**2+(0.0076/(C3)**2)**2*(dC3)**2+(1/(B3)-1/(C3))**2*(0.0002)**2)*10**4

A5=(9.809*A2/(0.0001*np.pi))*10**(-3)
dA5=(9.809/(0.0001*np.pi))*dA2*10**(-3)
#B=0.0002*(1/((0.0037*2+0.0002)/B0-(0.0037*2)/160))*(10**(4))
B5=(0.0086/B2-0.0076/C2)*(10**4)
dB5=np.sqrt((0.0086/(B2)**2)**2*(dB2)**2+(0.0076/(C2)**2)**2*(dC2)**2+(1/(B2)-1/(C2))**2*(0.0002)**2)*10**4

A7=(9.809*A6/(0.0001*np.pi))*10**(-3)
dA7=(9.809/(0.0001*np.pi))*dA6*10**(-3)
#B=0.0002*(1/((0.0037*2+0.0002)/B0-(0.0037*2)/160))*(10**(4))
B7=(0.0086/B6-0.0076/C6)*(10**4)
dB7=np.sqrt((0.0086/(B6)**2)**2*(dB6)**2+(0.0076/(C6)**2)**2*(dC6)**2+(1/(B6)-1/(C6))**2*(0.0002)**2)*10**4


#curve-fit-program
popt,pcov = curve_fit(func,A4,B4,p0=[0.0001,0,7])
errors = np.sqrt(np.diag(pcov))
#creat fit
xlin = np.linspace(min(A4),max(A4),1000)
ylin = func(xlin,*popt)

popt1,pcov1 = curve_fit(func,A5,B5,p0=[0.0001,0,7])
errors1 = np.sqrt(np.diag(pcov1))
#creat fit
xlin1 = np.linspace(min(A5),max(A5),1000)
ylin1 = func(xlin1,*popt1)

popt2,pcov2 = curve_fit(func,A7,B7,p0=[0.0001,0,7])
errors2 = np.sqrt(np.diag(pcov2))
#creat fit
xlin2 = np.linspace(min(A7),max(A7),1000)
ylin2 = func(xlin2,*popt2)


#creat axis and draw function
ax = plt.figure(dpi=350).add_subplot(1,1,1)
#ax.set_facecolor('gainsboro')
plt.errorbar(A1,B1,xerr=dA1,yerr=dB1, color='royalblue',fmt='.',label='Datenpunkte')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
plt.errorbar(A4,B4,xerr=dA4,yerr=dB4, color='crimson',fmt='.',label='m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
plt.errorbar(A5,B5,xerr=dA5,yerr=dB5, color='firebrick',fmt='.',label='m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt1[0].round(5)),str(errors1[0].round(5)),str(popt1[1].round(5)),str(errors1[1].round(5)),str(popt1[2].round(5)),str(errors1[2].round(5))))
plt.errorbar(A7,B7,xerr=dA7,yerr=dB7, color='navy',fmt='.',label='m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt2[0].round(5)),str(errors2[0].round(5)),str(popt2[1].round(5)),str(errors2[1].round(5)),str(popt2[2].round(5)),str(errors2[2].round(5))))
#plt.errorbar(x,B, color='firebrick',fmt='+',label='Channel 2')
#plt.errorbar(x,C, color='yellow',fmt='+',label='Channel 3')
#plt.errorbar(x,D, color='orangered',fmt='+',label='Channel 4')
#plt.errorbar(x,(E+1.7), color='navy',fmt='+',label='Channel 1b')
plt.plot(xlin,ylin,color='firebrick', label=r'Fit-Kurve: $n\cdot e^{-m\cdot x}+d$',lw=1.2)
plt.plot(xlin1,ylin1,color='firebrick', label=r'Fit-Kurve: $n\cdot e^{-m\cdot x}+d$',lw=1.2)
plt.plot(xlin2,ylin2,color='firebrick', label=r'Fit-Kurve: $n\cdot e^{-m\cdot x}+d$',lw=1.2)


plt.xlabel('Druck / kPa')
plt.ylabel(r'TFM / $\frac{cm^{2} \cdot K}{W}$')
plt.legend(loc='best')
plt.grid(True, which='minor',linestyle='--', color='darkgray', lw=0.5)
plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
plt.tight_layout()
plt.savefig("Aluminium_alle_gemessenen_Werte")

