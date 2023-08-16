import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

#---------------Curve-Fit---------------#
#define Function
def func(x,m,n,d):
   return n*np.exp(-m*x)+d 

def func1(x,m,n):
   return m/x**(1/4)+n

path_d = 'Aluminium_gegen_20_09/Gemittelte_Werte_Aluminium_gegen_Druck_20_09.txt'
datafile = np.loadtxt(path_d, delimiter='\t', unpack=True)
a,da,b,db,c,dc,d,dd = 0,1,4,5,2,3,6,7
A,dA,B,dB,C,dC,D,dD = datafile[a],datafile[da],datafile[b],datafile[db],datafile[c],datafile[dc],datafile[d],datafile[dd]
path_d1 = 'Aluminium_gegen_21_09/Gemittelte_Werte_Aluminium_gegen_Druck_21_09.txt'
datafile1 = np.loadtxt(path_d1, delimiter='\t', unpack=True)
A1,dA1,B1,dB1,C1,dC1,D1,dD1 = datafile1[a],datafile1[da],datafile1[b],datafile1[db],datafile1[c],datafile1[dc],datafile1[d],datafile1[dd]
path_d1 = 'Aluminium/Messung_Lambda_Aluminium_25_08.txt'
datafile2 = np.loadtxt(path_d1, delimiter='\t', unpack=True)
A2,dA2,B2,dB2,C2,dC2,D2,dD2 = datafile2[a],datafile2[da],datafile2[b],datafile2[db],datafile2[c],datafile2[dc],datafile2[d],datafile2[dd]


E=(9.809*A/(0.0001*np.pi))*10**(-3)
dE=(9.809/(0.0001*np.pi))*dA*10**(-3)
#B=0.0002*(1/((0.0037*2+0.0002)/B0-(0.0037*2)/160))*(10**(4))
F=(0.0086/B-0.0076/C)*(10**4)
dF=np.sqrt((0.0086/(B)**2)**2*(dB)**2+(0.0076/(C)**2)**2*(dC)**2+(1/(B)-1/(C))**2*(0.0002)**2)*10**4

E1=(9.809*A1/(0.0001*np.pi))*10**(-3)
dE1=(9.809/(0.0001*np.pi))*dA1*10**(-3)
#B=0.0002*(1/((0.0037*2+0.0002)/B0-(0.0037*2)/160))*(10**(4))
F1=(0.0086/B1-0.0076/C1)*(10**4)
dF1=np.sqrt((0.0086/(B1)**2)**2*(dB1)**2+(0.0076/(C1)**2)**2*(dC1)**2+(1/(B1)-1/(C1))**2*(0.0002)**2)*10**4

E2=(9.809*A2/(0.0001*np.pi))*10**(-3)
dE2=(9.809/(0.0001*np.pi))*dA2*10**(-3)
#B=0.0002*(1/((0.0037*2+0.0002)/B0-(0.0037*2)/160))*(10**(4))
F2=(0.0086/B2-0.0076/C2)*(10**4)
dF2=np.sqrt((0.0086/(B2)**2)**2*(dB2)**2+(0.0076/(C2)**2)**2*(dC2)**2+(1/(B2)-1/(C2))**2*(0.0002)**2)*10**4


#curve-fit-program
popt,pcov = curve_fit(func,E,B,p0=[0.0001,0,7])
errors = np.sqrt(np.diag(pcov))
#creat fit
xlin = np.linspace(min(E),max(E),1000)
ylin = func(xlin,*popt)

popt1,pcov1 = curve_fit(func,E1,B1,p0=[0.0001,0,7])
errors1 = np.sqrt(np.diag(pcov1))
#creat fit
xlin1 = np.linspace(min(E1),max(E1),1000)
ylin1 = func(xlin1,*popt1)

popt2,pcov2 = curve_fit(func,E2,B2,p0=[0.0001,0,7])
errors2 = np.sqrt(np.diag(pcov2))
#creat fit
xlin2 = np.linspace(min(E2),max(E2),1000)
ylin2 = func(xlin2,*popt2)



#creat axis and draw function
ax = plt.figure(dpi=350).add_subplot(1,1,1)
#ax.set_facecolor('gainsboro')
#plt.errorbar(E,B,xerr=dE,yerr=dB, color='royalblue',fmt='.',label='Datenpunkte 20/09 ')#\nm = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
plt.errorbar(E1,C1,xerr=dE1,yerr=dC1, color='crimson',fmt='.',label='Datenpunkte 21/09 ')#\nm = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt1[0].round(5)),str(errors1[0].round(5)),str(popt1[1].round(5)),str(errors1[1].round(5)),str(popt1[2].round(5)),str(errors1[2].round(5))))
#plt.errorbar(E2,B2,xerr=dE2,yerr=dB2, color='firebrick',fmt='.',label='Datenpunkte 25/08 ')#\nm = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt2[0].round(5)),str(errors2[0].round(5)),str(popt2[1].round(5)),str(errors2[1].round(5)),str(popt2[2].round(5)),str(errors2[2].round(5))))
#plt.errorbar(x,B, color='firebrick',fmt='+',label='Channel 2')
#plt.errorbar(x,C, color='yellow',fmt='+',label='Channel 3')
#plt.errorbar(x,D, color='orangered',fmt='+',label='Channel 4')
#plt.errorbar(x,(E+1.7), color='navy',fmt='+',label='Channel 1b')
#plt.plot(xlin,ylin,color='firebrick', label=r'Fit-Kurve: $\frac{m}{x^{\frac{1}{4}}}+n$',lw=1.2)
#plt.plot(xlin1,ylin1,color='firebrick', label=r'Fit-Kurve: $n\cdot e^{-m\cdot x}+d$',lw=1.2)
#plt.plot(xlin,ylin,color='royalblue', label=r'Fit-Kurve: $n\cdot e^{-m\cdot x}+d$',lw=1.2)
#plt.plot(xlin1,ylin1,color='crimson', label=r'Fit-Kurve: $n\cdot e^{-m\cdot x}+d$',lw=1.2)
#plt.plot(xlin2,ylin2,color='firebrick', label=r'Fit-Kurve: $n\cdot e^{-m\cdot x}+d$',lw=1.2)


plt.xlabel('Druck / kPa')
plt.ylabel(r'Wärmeleitfähigkeit / $\frac{W}{m\cdot K}$')#r'TFM / $\frac{cm^{2} \cdot K}{W}$')
plt.legend(loc='best')
plt.grid(True, which='minor',linestyle='--', color='darkgray', lw=0.5)
plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
plt.tight_layout()
plt.savefig("Aluminium_alle_gemessenen_Werte_Lambda_oben2.png")

