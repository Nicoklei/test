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
datafile3 = np.loadtxt('0-0055/Messung 1/Gemittelte_Werte_0-0055.txt', delimiter='\t', unpack=True)
A3,dA3,B3,dB3 = datafile3[2],datafile3[3],datafile3[4],datafile3[5]
datafile4 = np.loadtxt('0-0058/Gemittelte_Werte_0-0058.txt', delimiter='\t', unpack=True)
A4,dA4,B4,dB4 = datafile4[2],datafile4[3],datafile4[4],datafile4[5]
datafile5 = np.loadtxt('0-0057/Gemittelte_Werte_0-0057.txt', delimiter='\t', unpack=True)
A5,dA5,B5,dB5 = datafile5[2],datafile5[3],datafile5[4],datafile5[5]
datafile6 = np.loadtxt('0-0059/Gemittelte_Werte_0-0059.txt', delimiter='\t', unpack=True)
A6,dA6,B6,dB6 = datafile6[2],datafile6[3],datafile6[4],datafile6[5]
datafile7 = np.loadtxt('0-0060/Gemittelte_Werte_0-0060.txt', delimiter='\t', unpack=True)
A7,dA7,B7,dB7 = datafile7[2],datafile7[3],datafile7[4],datafile7[5]
datafile8 = np.loadtxt('CERN_09/Messung 2/Gemittelte_Werte_CERN-09.txt', delimiter='\t', unpack=True)
A8,dA8,B8,dB8 = datafile8[2],datafile8[3],datafile8[4],datafile8[5]
datafile9 = np.loadtxt('CERN_21/Gemittelte_Werte_CERN_21.txt', delimiter='\t', unpack=True)
A9,dA9,B9,dB9 = datafile9[2],datafile9[3],datafile9[4],datafile9[5]
datafile10 = np.loadtxt('CERN_21/Gemittelte_Werte_.txt', delimiter='\t', unpack=True)
A10,dA10,B10,dB10 = datafile10[2],datafile10[3],datafile10[4],datafile10[5]
datafile11 = np.loadtxt('0-0056/Gemittelte_Werte_0-0056.txt', delimiter='\t', unpack=True)
A11,dA11,B11,dB11 = datafile11[2],datafile11[3],datafile11[4],datafile11[5]
datafile12 = np.loadtxt('0-0051/Gemittelte_Werte_0-0051.txt', delimiter='\t', unpack=True)
A12,dA12,B12,dB12 = datafile12[2],datafile12[3],datafile12[4],datafile12[5]

datafile13 = np.loadtxt('0-0055/Messung 2/Gemittelte_Werte_0-0055.txt', delimiter='\t', unpack=True)
A13,dA13,B13,dB13 = datafile13[2],datafile13[3],datafile13[4],datafile13[5]
datafile14 = np.loadtxt('0-0060/Messung 2/Gemittelte_Werte_0-0060.txt', delimiter='\t', unpack=True)
A14,dA14,B14,dB14 = datafile14[2],datafile14[3],datafile14[4],datafile14[5]
datafile15 = np.loadtxt('0-0059/Messung 2/Gemittelte_Werte_0-0059.txt', delimiter='\t', unpack=True)
A15,dA15,B15,dB15 = datafile15[2],datafile15[3],datafile15[4],datafile15[5]
datafile16 = np.loadtxt('0-0058/Messung 2/Gemittelte_Werte_0-0058.txt', delimiter='\t', unpack=True)
A16,dA16,B16,dB16 = datafile16[2],datafile16[3],datafile16[4],datafile16[5]
datafile17 = np.loadtxt('0-0057/Messung 2/Gemittelte_Werte_0-0057.txt', delimiter='\t', unpack=True)
A17,dA17,B17,dB17 = datafile17[2],datafile17[3],datafile17[4],datafile17[5]
datafile18 = np.loadtxt('0-0056/Messung 2/Gemittelte_Werte_0-0056.txt', delimiter='\t', unpack=True)
A18,dA18,B18,dB18 = datafile18[2],datafile18[3],datafile18[4],datafile18[5]
datafile19 = np.loadtxt('0-0054/Messung 2/Gemittelte_Werte_0-0054.txt', delimiter='\t', unpack=True)
A19,dA19,B19,dB19 = datafile19[2],datafile19[3],datafile19[4],datafile19[5]
datafile20 = np.loadtxt('0-0053/Messung 2/Gemittelte_Werte_0-0053.txt', delimiter='\t', unpack=True)
A20,dA20,B20,dB20 = datafile20[2],datafile20[3],datafile20[4],datafile20[5]
datafile21 = np.loadtxt('0-0052/Messung 2/Gemittelte_Werte_0-0052.txt', delimiter='\t', unpack=True)
A21,dA21,B21,dB21 = datafile21[2],datafile21[3],datafile21[4],datafile21[5]
datafile22 = np.loadtxt('0-0051/Messung 2/Gemittelte_Werte_0-0051.txt', delimiter='\t', unpack=True)
A22,dA22,B22,dB22 = datafile22[2],datafile22[3],datafile22[4],datafile22[5]
datafile23 = np.loadtxt('CERN_09/Messung 3/Gemittelte_Werte_CERN-09.txt', delimiter='\t', unpack=True)
A23,dA23,B23,dB23 = datafile23[2],datafile23[3],datafile23[4],datafile23[5]


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
C12=(0.0092/B12-0.0074/A12)*(10**4)
dC12=np.sqrt((0.0092/(B12)**2)**2*(dB12)**2+(0.0074/(A12)**2)**2*(dA12)**2+(1/(B12)-1/(A12))**2*(0.0002)**2)*10**4

C13=(0.0092/B13-0.0074/A13)*(10**4)
dC13=np.sqrt((0.0092/(B13)**2)**2*(dB13)**2+(0.0074/(A13)**2)**2*(dA13)**2+(1/(B13)-1/(A13))**2*(0.0002)**2)*10**4
C14=(0.0092/B14-0.0074/A14)*(10**4)
dC14=np.sqrt((0.0092/(B14)**2)**2*(dB14)**2+(0.0074/(A14)**2)**2*(dA14)**2+(1/(B14)-1/(A14))**2*(0.0002)**2)*10**4
C15=(0.0092/B15-0.0074/A15)*(10**4)
dC15=np.sqrt((0.0092/(B15)**2)**2*(dB15)**2+(0.0074/(A15)**2)**2*(dA15)**2+(1/(B15)-1/(A15))**2*(0.0002)**2)*10**4
C16=(0.0092/B16-0.0074/A16)*(10**4)
dC16=np.sqrt((0.0092/(B16)**2)**2*(dB16)**2+(0.0074/(A16)**2)**2*(dA16)**2+(1/(B16)-1/(A16))**2*(0.0002)**2)*10**4
C17=(0.0092/B17-0.0074/A17)*(10**4)
dC17=np.sqrt((0.0092/(B17)**2)**2*(dB17)**2+(0.0074/(A17)**2)**2*(dA17)**2+(1/(B17)-1/(A17))**2*(0.0002)**2)*10**4
C18=(0.0092/B18-0.0074/A18)*(10**4)
dC18=np.sqrt((0.0092/(B18)**2)**2*(dB18)**2+(0.0074/(A18)**2)**2*(dA18)**2+(1/(B18)-1/(A18))**2*(0.0002)**2)*10**4
C19=(0.0092/B19-0.0074/A19)*(10**4)
dC19=np.sqrt((0.0092/(B19)**2)**2*(dB19)**2+(0.0074/(A19)**2)**2*(dA19)**2+(1/(B19)-1/(A19))**2*(0.0002)**2)*10**4
C20=(0.0092/B20-0.0074/A20)*(10**4)
dC20=np.sqrt((0.0092/(B20)**2)**2*(dB20)**2+(0.0074/(A20)**2)**2*(dA20)**2+(1/(B20)-1/(A20))**2*(0.0002)**2)*10**4
C21=(0.0092/B21-0.0074/A21)*(10**4)
dC21=np.sqrt((0.0092/(B21)**2)**2*(dB21)**2+(0.0074/(A21)**2)**2*(dA21)**2+(1/(B21)-1/(A21))**2*(0.0002)**2)*10**4
C22=(0.0092/B22-0.0074/A22)*(10**4)
dC22=np.sqrt((0.0092/(B22)**2)**2*(dB22)**2+(0.0074/(A22)**2)**2*(dA22)**2+(1/(B22)-1/(A22))**2*(0.0002)**2)*10**4
C23=(0.0092/B23-0.0074/A23)*(10**4)
dC23=np.sqrt((0.0092/(B23)**2)**2*(dB23)**2+(0.0074/(A23)**2)**2*(dA23)**2+(1/(B23)-1/(A23))**2*(0.0002)**2)*10**4



D=[C12[0],C12[1],C12[2],C[0],C[1],C[2],C[3],C1[0],C1[1],C1[2],C1[3],C2[0],C2[1],C2[2],C3[0],C3[1],C3[2],C11[0],C11[1],C11[2],C5[0],C5[1],C5[2],C5[3],C4[0],C4[1],C4[2],C6[0],C6[1],C6[2],C7,C8[0],C8[1],C8[2],C8[3],C8[4],C9[2]]
dD=[dC12[0],dC12[1],dC12[2],dC[0],dC[1],dC[2],dC[3],dC1[0],dC1[1],dC1[2],dC1[3],dC2[0],dC2[1],dC2[2],dC3[0],dC3[1],dC3[2],dC11[0],dC11[1],dC11[2],dC5[0],dC5[1],dC5[2],dC5[3],dC4[0],dC4[1],dC4[2],dC6[0],dC6[1],dC6[2],dC7,dC8[0],dC8[1],dC8[2],dC8[3],dC8[4],dC9[2]]

D1=[C10[0],C10[1],C10[2],C13[0],C13[1],C13[2],C14[0],C14[1],C14[2],C14[3],C15[0],C15[1],C15[2],C16[0],C16[1],C16[2],C16[3],C16[4],C17[0],C17[1],C17[2],C18[0],C18[1],C18[2],C19[0],C19[1],C19[2],C20[0],C20[1],C20[2],C21[0],C21[1],C21[2],C21[3],C21[4],C21[5],C22[0],C22[1],C22[2],C23[0],C23[1],C23[2]]
dD1=[dC10[0],dC10[1],dC10[2],dC13[0],dC13[1],dC13[2],dC14[0],dC14[1],dC14[2],dC14[3],dC15[0],dC15[1],dC15[2],dC16[0],dC16[1],dC16[2],dC16[3],dC16[4],dC17[0],dC17[1],dC17[2],dC18[0],dC18[1],dC18[2],dC19[0],dC19[1],dC19[2],dC20[0],dC20[1],dC20[2],dC21[0],dC21[1],dC21[2],dC21[3],dC21[4],dC21[5],dC22[0],dC22[1],dC22[2],dC23[0],dC23[1],dC23[2]]

E=['51','51','51','52','52','52','52','53','53','53','53','54','54','54','55','55','55','56','56','56','57','57','57','57','58','58','58','59','59','59','60','CERN\n09','CERN\n09','CERN\n09','CERN\n09','CERN\n09','CERN\n21']
E1=['CERN\n21','CERN\n21','CERN\n21','55','55','55','60','60','60','60','59','59','59','58','58','58','58','58','57','57','57','56','56','56','54','54','54','53','53','53','52','52','52','52','52','52','51','51','51','CERN\n09','CERN\n09','CERN\n09']
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
#plt.errorbar(x,B, color='firebrick',fmt='+',label='Channel 2')
#plt.errorbar(x,C, color='yellow',fmt='+',label='Channel 3')
#plt.errorbar(x,D, color='orangered',fmt='+',label='Channel 4')
#plt.errorbar(x,(E+1.7), color='navy',fmt='+',label='Channel 1b')
#plt.plot(xlin,ylin,color='firebrick', label='Fit-Kurve: n*exp(-m*x)+d',lw=1.2)

plt.xlabel('Seriennummern der Cells')
plt.ylabel(r'TFM / $\frac{cm^{2} \cdot K}{W}$')
plt.legend(loc='best')
plt.grid(True, which='minor',linestyle='--', color='darkgray', lw=0.5)
plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
plt.tight_layout()
plt.savefig("TFM_aller_Cells")

