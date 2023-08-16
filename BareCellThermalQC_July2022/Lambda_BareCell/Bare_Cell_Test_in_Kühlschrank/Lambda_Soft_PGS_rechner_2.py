import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

#---------------Curve-Fit---------------#
#define Function
def func(x,m,n,d):
   return n*np.exp(-m*x)+d

#get data(every 15 pairs off data the channal changes to the next. So there are 15 pairs of achan0 data and than 15 of achan1 and so on)
#path_d = 'Lambda Messungen/Messung_Lambda_PGS_22_08.txt'
datafile = np.loadtxt('0-0052/Gemittelte_Werte_0-0052.txt', delimiter='\t', unpack=True)
A,dA,B,dB = datafile[2],datafile[3],datafile[4],datafile[5]
datafile1 = np.loadtxt('0-0053/Gemittelte_Werte_0-0053.txt', delimiter='\t', unpack=True)
A1,dA1,B1,dB1 = datafile1[2],datafile1[3],datafile1[4],datafile1[5]
datafile2 = np.loadtxt('0-0054/Gemittelte_Werte_0-0054.txt', delimiter='\t', unpack=True)
A2,dA2,B2,dB2 = datafile2[2],datafile2[3],datafile2[4],datafile2[5]
datafile3 = np.loadtxt('0-0055/Gemittelte_Werte_0-0055.txt', delimiter='\t', unpack=True)
A3,dA3,B3,dB3 = datafile3[2],datafile3[3],datafile3[4],datafile3[5]
datafile4 = np.loadtxt('0-0058/Gemittelte_Werte_0-0058.txt', delimiter='\t', unpack=True)
A4,dA4,B4,dB4 = datafile4[2],datafile4[3],datafile4[4],datafile4[5]
datafile5 = np.loadtxt('0-0057/Gemittelte_Werte_0-0057.txt', delimiter='\t', unpack=True)
A5,dA5,B5,dB5 = datafile5[2],datafile5[3],datafile5[4],datafile5[5]
datafile6 = np.loadtxt('0-0059/Gemittelte_Werte_0-0059.txt', delimiter='\t', unpack=True)
A6,dA6,B6,dB6 = datafile6[2],datafile6[3],datafile6[4],datafile6[5]
datafile7 = np.loadtxt('0-0060/Gemittelte_Werte_0-0060.txt', delimiter='\t', unpack=True)
A7,dA7,B7,dB7 = datafile7[2],datafile7[3],datafile7[4],datafile7[5]
datafile11 = np.loadtxt('0-0056/Gemittelte_Werte_0-0056.txt', delimiter='\t', unpack=True)
A11,dA11,B11,dB11 = datafile11[2],datafile11[3],datafile11[4],datafile11[5]
datafile12 = np.loadtxt('0-0051/Gemittelte_Werte_0-0051.txt', delimiter='\t', unpack=True)
A12,dA12,B12,dB12 = datafile12[2],datafile12[3],datafile12[4],datafile12[5]


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
C11=(0.0092/B11-0.0074/A11)*(10**4)
dC11=np.sqrt((0.0092/(B11)**2)**2*(dB11)**2+(0.0074/(A11)**2)**2*(dA11)**2+(1/(B11)-1/(A11))**2*(0.0002)**2)*10**4
C12=(0.0092/B12-0.0074/A12)*(10**4)
dC12=np.sqrt((0.0092/(B12)**2)**2*(dB12)**2+(0.0074/(A12)**2)**2*(dA12)**2+(1/(B12)-1/(A12))**2*(0.0002)**2)*10**4



D=[np.sum(C12/dC12**2)/np.sum(1/dC12**2),np.sum(C/dC**2)/np.sum(1/dC**2),np.sum(C1/dC1**2)/np.sum(1/dC1**2),np.sum(C2/dC2**2)/np.sum(1/dC2**2),np.sum(C3/dC3**2)/np.sum(1/dC3**2),np.sum(C11/dC11**2)/np.sum(1/dC11**2),np.sum(C5/dC5**2)/np.sum(1/dC5**2),np.sum(C4/dC4**2)/np.sum(1/dC4**2),np.sum(C6/dC6**2)/np.sum(1/dC6**2),np.sum(C7/dC7**2)/np.sum(1/dC7**2)]
dD=[np.sqrt(1/np.sum(1/dC12**2)),np.sqrt(1/np.sum(1/dC**2)),np.sqrt(1/np.sum(1/dC1**2)),np.sqrt(1/np.sum(1/dC2**2)),np.sqrt(1/np.sum(1/dC3**2)),np.sqrt(1/np.sum(1/dC11**2)),np.sqrt(1/np.sum(1/dC5**2)),np.sqrt(1/np.sum(1/dC4**2)),np.sqrt(1/np.sum(1/dC6**2)),np.sqrt(1/np.sum(1/dC7**2))]


E=['51','52','53','54','55','56','57','58','59','60']
E1=['55','60','59','58','57','56','54','53','52','51']
#E=[1.38,1.38,1.38,1.4,1.4,1.4,1.4,1.42,1.42,1.42,1.42,1.375,1.375,1.375,1.39,1.39,1.39,1.38,1.38,1.38,1.365,1.365,1.365,1.365,1.37,1.37,1.37,1.36,1.36,1.36,1.41,1.505,1.505,1.505,1.505,1.505,1.52,1.52,1.52,1.52]
#curve-fit-program
#popt,pcov = curve_fit(func,A,B1,p0=[0.000001,0,7])
#errors = np.sqrt(np.diag(pcov))
#print('Steigung: ' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5))+ '\n' + 'y-Achse: ' + str(popt[1].round(5)) + '+/-' + str(errors[1].round(5)))
#print('Nochmal komplett: y=' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5)) + '*x+' + str(popt[1].round(5))+ '+/-' + str(errors[1].round(5)))

datei = open('Bare_Cell_TFM_Data_controlled_temperature','w')

datei.write(
   str('Bare Cell')+'\t'+str('TFM')+'\t'+str('error')+'\n'+
   str('0-0051')+'\t'+str(round(D[0],3))+'\t'+str(round(dD[0],3))+'\n'+
   str('0-0052')+'\t'+str(round(D[1],3))+'\t'+str(round(dD[1],3))+'\n'+
   str('0-0053')+'\t'+str(round(D[2],3))+'\t'+str(round(dD[2],3))+'\n'+
   str('0-0054')+'\t'+str(round(D[3],3))+'\t'+str(round(dD[3],3))+'\n'+
   str('0-0055')+'\t'+str(round(D[4],3))+'\t'+str(round(dD[4],3))+'\n'+
   str('0-0056')+'\t'+str(round(D[5],3))+'\t'+str(round(dD[5],3))+'\n'+
   str('0-0057')+'\t'+str(round(D[6],3))+'\t'+str(round(dD[6],3))+'\n'+
   str('0-0058')+'\t'+str(round(D[7],3))+'\t'+str(round(dD[7],3))+'\n'+
   str('0-0059')+'\t'+str(round(D[8],3))+'\t'+str(round(dD[8],3))+'\n'+
   str('0-0060')+'\t'+str(round(D[9],3))+'\t'+str(round(dD[9],3))+'\n'
)

datei.close()


#creat fit
#xlin = np.linspace(min(A1),max(A1),1000)
#ylin = func(xlin,*popt)

#creat axis and draw function
ax = plt.figure(dpi=350).add_subplot(1,1,1)
#ax.set_facecolor('gainsboro')
plt.errorbar(E,D,yerr=dD, color='royalblue',fmt='.',label='Datenpunkte aus erster Messung')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
#plt.plot(xlin,ylin,color='firebrick', label='Fit-Kurve: n*exp(-m*x)+d',lw=1.2)

plt.xlabel('Seriennummern der Cells')
plt.ylabel(r'TFM / $\frac{cm^{2} \cdot K}{W}$')
plt.legend(loc='best')
plt.grid(True, which='minor',linestyle='--', color='darkgray', lw=0.5)
plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
plt.tight_layout()
plt.savefig("TFM_aller_Cells_Mittelwerte")

