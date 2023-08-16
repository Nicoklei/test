import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

#---------------Curve-Fit---------------#
#define Function
def func(x,m,n,d):
   return n*np.exp(-m*x)+d

#get data(every 15 pairs off data the channal changes to the next. So there are 15 pairs of achan0 data and than 15 of achan1 and so on)
#path_d = 'Lambda Messungen/Messung_Lambda_PGS_22_08.txt'
datafile = np.loadtxt('90_Grad_gegen_Uhrzeigersinn1/Gemittelte_Werte_0-0054_ohne_Soft-PGS_90_Grad_gedreht.txt', delimiter='\t', unpack=True)
A,dA,B,dB = datafile[2],datafile[3],datafile[4],datafile[5]
datafile1 = np.loadtxt('90_Grad_gegen_Uhrzeigersinn2/Gemittelte_Werte_0-0054_ohne_Soft-PGS_90_Grad_gedreht.txt', delimiter='\t', unpack=True)
A1,dA1,B1,dB1 = datafile1[2],datafile1[3],datafile1[4],datafile1[5]
datafile2 = np.loadtxt('90_Grad_gegen_Uhrzeigersinn3/Gemittelte_Werte_0-0054_ohne_Soft-PGS_90_Grad_gedreht.txt', delimiter='\t', unpack=True)
A2,dA2,B2,dB2 = datafile2[2],datafile2[3],datafile2[4],datafile2[5]
datafile3 = np.loadtxt('180_Grad_gegen_Uhrzeigersinn1/Gemittelte_Werte_0-0054_ohne_Soft-PGS_180_Grad_gedreht.txt', delimiter='\t', unpack=True)
A3,dA3,B3,dB3 = datafile3[2],datafile3[3],datafile3[4],datafile3[5]
datafile4 = np.loadtxt('180_Grad_gegen_Uhrzeigersinn2/Gemittelte_Werte_0-0054_ohne_Soft-PGS_180_Grad_gedreht.txt', delimiter='\t', unpack=True)
A4,dA4,B4,dB4 = datafile4[2],datafile4[3],datafile4[4],datafile4[5]
datafile5 = np.loadtxt('180_Grad_gegen_Uhrzeigersinn3/Gemittelte_Werte_0-0054_ohne_Soft-PGS_180_Grad_gedreht.txt', delimiter='\t', unpack=True)
A5,dA5,B5,dB5 = datafile5[2],datafile5[3],datafile5[4],datafile5[5]
datafile6 = np.loadtxt('270_Grad_gegen_Uhrzeigersinn1/Gemittelte_Werte_0-0054_ohne_Soft-PGS_270_Grad_gedreht.txt', delimiter='\t', unpack=True)
A6,dA6,B6,dB6 = datafile6[2],datafile6[3],datafile6[4],datafile6[5]
datafile7 = np.loadtxt('270_Grad_gegen_Uhrzeigersinn2/Gemittelte_Werte_0-0054_ohne_Soft-PGS_270_Grad_gedreht.txt', delimiter='\t', unpack=True)
A7,dA7,B7,dB7 = datafile7[2],datafile7[3],datafile7[4],datafile7[5]
datafile8 = np.loadtxt('270_Grad_gegen_Uhrzeigersinn3/Gemittelte_Werte_0-0054_ohne_Soft-PGS_270_Grad_gedreht.txt', delimiter='\t', unpack=True)
A8,dA8,B8,dB8 = datafile8[2],datafile8[3],datafile8[4],datafile8[5]
datafile9 = np.loadtxt('zum_Raum1/Gemittelte_Werte_0-0054_ohne_Soft-PGS_zum_Raum.txt', delimiter='\t', unpack=True)
A9,dA9,B9,dB9 = datafile9[2],datafile9[3],datafile9[4],datafile9[5]
datafile10 = np.loadtxt('zum_Raum2/Gemittelte_Werte_0-0054_ohne_Soft-PGS_zum_Raum.txt', delimiter='\t', unpack=True)
A10,dA10,B10,dB10 = datafile10[2],datafile10[3],datafile10[4],datafile10[5]
datafile11 = np.loadtxt('zum_Raum3/Gemittelte_Werte_0-0054_ohne_Soft-PGS_zum_Raum.txt', delimiter='\t', unpack=True)
A11,dA11,B11,dB11 = datafile11[2],datafile11[3],datafile11[4],datafile11[5]


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
C4=(0.0092/B4-0.0074/A4)*(10**4)
dC4=np.sqrt((0.0092/(B4)**2)**2*(dB4)**2+(0.0074/(A4)**2)**2*(dA4)**2+(1/(B4)-1/(A4))**2*(0.0002)**2)*10**4
C5=(0.0092/B5-0.0074/A5)*(10**4)
dC5=np.sqrt((0.0092/(B5)**2)**2*(dB5)**2+(0.0074/(A5)**2)**2*(dA5)**2+(1/(B5)-1/(A5))**2*(0.0002)**2)*10**4
C6=(0.0092/B6-0.0074/A6)*(10**4)
dC6=np.sqrt((0.0092/(B6)**2)**2*(dB6)**2+(0.0074/(A6)**2)**2*(dA6)**2+(1/(B6)-1/(A6))**2*(0.0002)**2)*10**4
C7=(0.0092/B7-0.0074/A7)*(10**4)
dC7=np.sqrt((0.0092/(B7)**2)**2*(dB7)**2+(0.0074/(A7)**2)**2*(dA7)**2+(1/(B7)-1/(A7))**2*(0.0002)**2)*10**4
C8=(0.0092/B8-0.0074/A8)*(10**4)
dC8=np.sqrt((0.0092/(B8)**2)**2*(dB8)**2+(0.0074/(A8)**2)**2*(dA8)**2+(1/(B8)-1/(A8))**2*(0.0002)**2)*10**4
C9=(0.0092/B9-0.0074/A9)*(10**4)
dC9=np.sqrt((0.0092/(B9)**2)**2*(dB9)**2+(0.0074/(A9)**2)**2*(dA9)**2+(1/(B9)-1/(A9))**2*(0.0002)**2)*10**4
C10=(0.0092/B10-0.0074/A10)*(10**4)
dC10=np.sqrt((0.0092/(B10)**2)**2*(dB10)**2+(0.0074/(A10)**2)**2*(dA10)**2+(1/(B10)-1/(A10))**2*(0.0002)**2)*10**4
C11=(0.0092/B11-0.0074/A11)*(10**4)
dC11=np.sqrt((0.0092/(B11)**2)**2*(dB11)**2+(0.0074/(A11)**2)**2*(dA11)**2+(1/(B11)-1/(A11))**2*(0.0002)**2)*10**4


D = np.array([])
dD = np.array([])
D1 = np.array([])
dD1 = np.array([])
D2 = np.array([])
dD2 = np.array([])

D = np.append(D,np.sum(C9/dC9**2)/np.sum(1/dC9**2))
dD= np.append(dD,np.sqrt(1/np.sum(1/dC9**2)))
D1 = np.append(D1,np.sum(C10/dC10**2)/np.sum(1/dC10**2))
dD1= np.append(dD1,np.sqrt(1/np.sum(1/dC10**2)))
D2 = np.append(D2,np.sum(C11/dC11**2)/np.sum(1/dC11**2))
dD2= np.append(dD2,np.sqrt(1/np.sum(1/dC11**2)))
D = np.append(D,np.sum(C/dC**2)/np.sum(1/dC**2))
dD= np.append(dD,np.sqrt(1/np.sum(1/dC**2)))
D1 = np.append(D1,np.sum(C1/dC1**2)/np.sum(1/dC1**2))
dD1= np.append(dD1,np.sqrt(1/np.sum(1/dC1**2)))
D2 = np.append(D2,np.sum(C2/dC2**2)/np.sum(1/dC2**2))
dD2= np.append(dD2,np.sqrt(1/np.sum(1/dC2**2)))
D = np.append(D,np.sum(C3/dC3**2)/np.sum(1/dC3**2))
dD= np.append(dD,np.sqrt(1/np.sum(1/dC3**2)))
D1 = np.append(D1,np.sum(C4/dC4**2)/np.sum(1/dC4**2))
dD1= np.append(dD1,np.sqrt(1/np.sum(1/dC4**2)))
D2 = np.append(D2,np.sum(C5/dC5**2)/np.sum(1/dC5**2))
dD2= np.append(dD2,np.sqrt(1/np.sum(1/dC5**2)))
D = np.append(D,np.sum(C6/dC6**2)/np.sum(1/dC6**2))
dD= np.append(dD,np.sqrt(1/np.sum(1/dC6**2)))
D1 = np.append(D1,np.sum(C7/dC7**2)/np.sum(1/dC7**2))
dD1= np.append(dD1,np.sqrt(1/np.sum(1/dC7**2)))
D2 = np.append(D2,np.sum(C8/dC8**2)/np.sum(1/dC8**2))
dD2= np.append(dD2,np.sqrt(1/np.sum(1/dC8**2)))



E = ['0°','90°','180°','270°']
E1 = ['0°','90°','180°','270°']#['0°','0°','90°','90°','180°','180°','270°','270°']
E2 = ['0°','90°','180°','270°']#['0°','0°','90°','90°','180°','180°','270°','270°']


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
plt.errorbar(E,D,yerr=dD, color='royalblue',fmt='.',label='Datenpunkte aus erster Messung')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
plt.errorbar(E1,D1,yerr=dD1, color='crimson',fmt='.',label='Datenpunkte aus zweiter Messung')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
plt.errorbar(E2,D2,yerr=dD2, color='navy',fmt='.',label='Datenpunkte aus dritter Messung')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
#plt.errorbar(x,B, color='firebrick',fmt='+',label='Channel 2')
#plt.errorbar(x,C, color='yellow',fmt='+',label='Channel 3')
#plt.errorbar(x,D, color='orangered',fmt='+',label='Channel 4')
#plt.errorbar(x,(E+1.7), color='navy',fmt='+',label='Channel 1b')
#plt.plot(xlin,ylin,color='firebrick', label='Fit-Kurve: n*exp(-m*x)+d',lw=1.2)

plt.xlabel('Drehung der Cell 0-0054')
plt.ylabel(r'TFM / $\frac{cm^{2} \cdot K}{W}$')
plt.legend(loc='best')
plt.grid(True, which='minor',linestyle='--', color='darkgray', lw=0.5)
plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
plt.tight_layout()
plt.savefig("TFM_0-0054_gedreht")

