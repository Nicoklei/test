from lzma import FILTER_LZMA2
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

#---------------Curve-Fit---------------#
#define Function
def func(x,m,n,d):
   return n*np.exp(-m*x)+d

#get data(every 15 pairs off data the channal changes to the next. So there are 15 pairs of achan0 data and than 15 of achan1 and so on)
#path_d = 'Lambda Messungen/Messung_Lambda_PGS_22_08.txt'
datafile = np.loadtxt('mit_Vakuum/Gemittelte_Werte_CERN-09_höhere_Temperatur.txt', delimiter='\t', unpack=True)
A,dA,B,dB = datafile[2],datafile[3],datafile[4],datafile[5]
datafile1 = np.loadtxt('mit_Vakuum_nach_ohne_Vakuum_Messung/Gemittelte_Werte_CERN-09_höhere_Temperatur_Vakuum_2.txt', delimiter='\t', unpack=True)
A1,dA1,B1,dB1 = datafile1[2],datafile1[3],datafile1[4],datafile1[5]
datafile2 = np.loadtxt('ohne_Vakuum/Gemittelte_Werte_CERN-09_höhere_Temperatur_kein_Vakuum.txt', delimiter='\t', unpack=True)
A2,dA2,B2,dB2 = datafile2[2],datafile2[3],datafile2[4],datafile2[5]
datafile3 = np.loadtxt('mit_Vakuum_kalt/Gemittelte_Werte_CERN-09_niedrige_Temperatur_Vakuum.txt', delimiter='\t', unpack=True)
A3,dA3,B3,dB3 = datafile3[2],datafile3[3],datafile3[4],datafile3[5]


#A1=(9.809*A/(0.0001*np.pi))*10**(-3)
#dA1=(9.809/(0.0001*np.pi))*dA*10**(-3)
#B=0.0002*(1/((0.0037*2+0.0002)/B0-(0.0037*2)/160))*(10**(4))
C=(0.0092/B-0.0074/A)*(10**4)
dC=np.sqrt((0.0092/(B)**2)**2*(dB)**2+(0.0074/(A)**2)**2*(dA)**2+(1/(B)-1/(A))**2*(0.0002)**2)*10**4
C1=(0.0092/B1-0.0074/A1)*(10**4)
dC1=np.sqrt((0.0092/(B1)**2)**2*(dB1)**2+(0.0074/(A1)**2)**2*(dA1)**2+(1/(B1)-1/(A1))**2*(0.0002)**2)*10**4
C2=(0.0092/B2-0.0074/A2)*(10**4)
dC2=np.sqrt((0.0092/(B2)**2)**2*(dB2)**2+(0.0074/(A2)**2)**2*(dA2)**2+(1/(B2)-1/(A2))**2*(0.0002)**2)*10**4
C3=(0.0092/B3-0.0074/A3)*(10**4)
dC3=np.sqrt((0.0092/(B3)**2)**2*(dB3)**2+(0.0074/(A3)**2)**2*(dA3)**2+(1/(B3)-1/(A3))**2*(0.0002)**2)*10**4

D=np.sum(A/dA**2)/np.sum(1/dA**2)
dD=np.sqrt(1/np.sum(1/dA**2))
D1=np.sum(A1/dA1**2)/np.sum(1/dA1**2)
dD1=np.sqrt(1/np.sum(1/dA1**2))
D2=np.sum(A2/dA2**2)/np.sum(1/dA2**2)
dD2=np.sqrt(1/np.sum(1/dA2**2))
D3=np.sum(A3/dA3**2)/np.sum(1/dA3**2)
dD3=np.sqrt(1/np.sum(1/dA3**2))

E=['Höhere\nTemperatur\nmit Vakuum','Höhere\nTemperatur\nmit Vakuum','Höhere\nTemperatur\nmit Vakuum']
E1=['Höhere\nTemperatur\nmit Vakuum\nMessung 2','Höhere\nTemperatur\nmit Vakuum\nMessung 2','Höhere\nTemperatur\nmit Vakuum\nMessung 2','Höhere\nTemperatur\nmit Vakuum\nMessung 2']
E2=['Höhere\nTemperatur\nohne Vakuum','Höhere\nTemperatur\nohne Vakuum','Höhere\nTemperatur\nohne Vakuum','Höhere\nTemperatur\nohne Vakuum','Höhere\nTemperatur\nohne Vakuum','Höhere\nTemperatur\nohne Vakuum']
E3=['Niedrige\nTemperatur\nmit Vakuum','Niedrige\nTemperatur\nmit Vakuum','Niedrige\nTemperatur\nmit Vakuum']
F=['Höhere\nTemperatur\nmit Vakuum']
F1=['Höhere\nTemperatur\nmit Vakuum\nMessung 2']
F2=['Höhere\nTemperatur\nohne Vakuum']
F3=['Niedrige\nTemperatur\nmit Vakuum']
#E=[1.38,1.38,1.38,1.4,1.4,1.4,1.4,1.42,1.42,1.42,1.42,1.375,1.375,1.375,1.39,1.39,1.39,1.38,1.38,1.38,1.365,1.365,1.365,1.365,1.37,1.37,1.37,1.36,1.36,1.36,1.41,1.505,1.505,1.505,1.505,1.505,1.52,1.52,1.52,1.52]
#curve-fit-program
#popt,pcov = curve_fit(func,A,B1,p0=[0.000001,0,7])
#errors = np.sqrt(np.diag(pcov))
#print('Steigung: ' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5))+ '\n' + 'y-Achse: ' + str(popt[1].round(5)) + '+/-' + str(errors[1].round(5)))
#print('Nochmal komplett: y=' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5)) + '*x+' + str(popt[1].round(5))+ '+/-' + str(errors[1].round(5)))

#creat fit
#xlin = np.linspace(min(A1),max(A1),1000)
#ylin = func(xlin,*popt)

#creat axis and draw function
ax = plt.figure(dpi=350).add_subplot(1,1,1)
#ax.set_facecolor('gainsboro')
plt.errorbar(E,A,yerr=dA, color='royalblue',fmt='.',label='Alle gemessenen Datenpunkte')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
plt.errorbar(E1,A1,yerr=dA1, color='royalblue',fmt='.')#,label='Datenpunkte aus zweiter Messung')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
plt.errorbar(E2,A2,yerr=dA2, color='royalblue',fmt='.')#,label='Datenpunkte aus erster Messung')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
plt.errorbar(E3,A3,yerr=dA3, color='royalblue',fmt='.')#,label='Datenpunkte aus erster Messung')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
plt.errorbar(F,D,yerr=dD, color='crimson',fmt='.',label='Mittelwerte der Datenpunkte')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
plt.errorbar(F1,D1,yerr=dD1, color='crimson',fmt='.')#,label='Datenpunkte aus erster Messung')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
plt.errorbar(F2,D2,yerr=dD2, color='crimson',fmt='.')#,label='Datenpunkte aus erster Messung')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
plt.errorbar(F3,D3,yerr=dD3, color='crimson',fmt='.')#,label='Datenpunkte aus erster Messung')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
#plt.errorbar(x,B, color='firebrick',fmt='+',label='Channel 2')
#plt.errorbar(x,C, color='yellow',fmt='+',label='Channel 3')
#plt.errorbar(x,D, color='orangered',fmt='+',label='Channel 4')
#plt.errorbar(x,(E+1.7), color='navy',fmt='+',label='Channel 1b')
#plt.plot(xlin,ylin,color='firebrick', label='Fit-Kurve: n*exp(-m*x)+d',lw=1.2)

#plt.xlabel('Beschreibung der Messung')
plt.ylabel(r'Wärmeleitfähigkeit / $\frac{W}{m \cdot K}$')#r'TFM / $\frac{cm^{2} \cdot K}{W}$')
plt.legend(loc='best')
plt.grid(True, which='minor',linestyle='--', color='darkgray', lw=0.5)
plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
plt.tight_layout()
plt.savefig("Lambda_Aluminium_oben_mit_und_ohne_Vakuum")

