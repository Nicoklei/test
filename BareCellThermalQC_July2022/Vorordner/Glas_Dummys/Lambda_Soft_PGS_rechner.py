import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

#---------------Curve-Fit---------------#
#define Function
def func(x,m,n):
   return m*x+n

#get data(every 15 pairs off data the channal changes to the next. So there are 15 pairs of achan0 data and than 15 of achan1 and so on)

all_TFM = np.array([])
all_TFM_error = np.array([])
all_TFM1 = np.array([])
all_TFM_error1 = np.array([])
all_TFM2 = np.array([])
all_TFM_error2 = np.array([])
all_TFM3 = np.array([])
all_TFM_error3 = np.array([])

Bare_Cells = ['Glas_Dummy_A1','Glas_Dummy_A9','Glas_Dummy_B7','Glas_Dummy_C9']
Bare_Cells1 = ['Glas_Dummy_A1_1','Glas_Dummy_A9_1','Glas_Dummy_B7_1','Glas_Dummy_C9_1']
Bare_Cells2 = ['Glas_Dummy_A1_2','Glas_Dummy_A9_2','Glas_Dummy_B7_2','Glas_Dummy_C9_2']
Bare_Cells3 = ['Glas_Dummy_A1_3','Glas_Dummy_A9_3','Glas_Dummy_B7_3','Glas_Dummy_C9_3']

for serial_number in Bare_Cells:
   path_d = ('%s/Gemittelte_Werte_%s.txt')%(serial_number,serial_number)
   datafile = np.loadtxt(path_d, delimiter='\t', unpack=True)
   a,da,b,db,c,dc,d,dd = 0,1,4,5,2,3,6,7
   A,dA,B,dB,C,dC,D,dD = datafile[a],datafile[da],datafile[b],datafile[db],datafile[c],datafile[dc],datafile[d],datafile[dd]


   #A1=(9.809*A/(0.0001*np.pi))*10**(-3)
   #dA1=(9.809/(0.0001*np.pi))*dA*10**(-3)
   B1=(0.0092/B-0.0076/C)*(10**4)
   dB1=np.sqrt((0.0092/(B)**2)**2*(dB)**2+(0.0076/(C)**2)**2*(dC)**2+(1/(B)-1/(C))**2*(0.0005)**2)*10**4

   all_TFM = np.append(all_TFM,B1)
   all_TFM_error = np.append(all_TFM_error,dB1)

for serial_number in Bare_Cells1:
   path_d = ('%s/Gemittelte_Werte_%s.txt')%(serial_number,serial_number)
   datafile = np.loadtxt(path_d, delimiter='\t', unpack=True)
   a,da,b,db,c,dc,d,dd = 0,1,4,5,2,3,6,7
   A,dA,B,dB,C,dC,D,dD = datafile[a],datafile[da],datafile[b],datafile[db],datafile[c],datafile[dc],datafile[d],datafile[dd]


   #A1=(9.809*A/(0.0001*np.pi))*10**(-3)
   #dA1=(9.809/(0.0001*np.pi))*dA*10**(-3)
   B1=(0.0092/B-0.0076/C)*(10**4)
   dB1=np.sqrt((0.0092/(B)**2)**2*(dB)**2+(0.0076/(C)**2)**2*(dC)**2+(1/(B)-1/(C))**2*(0.0005)**2)*10**4

   all_TFM1 = np.append(all_TFM1,B1)
   all_TFM_error1 = np.append(all_TFM_error1,dB1)

for serial_number in Bare_Cells2:
   path_d = ('%s/Gemittelte_Werte_%s.txt')%(serial_number,serial_number)
   datafile = np.loadtxt(path_d, delimiter='\t', unpack=True)
   a,da,b,db,c,dc,d,dd = 0,1,4,5,2,3,6,7
   A,dA,B,dB,C,dC,D,dD = datafile[a],datafile[da],datafile[b],datafile[db],datafile[c],datafile[dc],datafile[d],datafile[dd]


   #A1=(9.809*A/(0.0001*np.pi))*10**(-3)
   #dA1=(9.809/(0.0001*np.pi))*dA*10**(-3)
   B1=(0.0092/B-0.0076/C)*(10**4)
   dB1=np.sqrt((0.0092/(B)**2)**2*(dB)**2+(0.0076/(C)**2)**2*(dC)**2+(1/(B)-1/(C))**2*(0.0005)**2)*10**4

   all_TFM2 = np.append(all_TFM2,B1)
   all_TFM_error2 = np.append(all_TFM_error2,dB1)

for serial_number in Bare_Cells3:
   path_d = ('%s/Gemittelte_Werte_%s.txt')%(serial_number,serial_number)
   datafile = np.loadtxt(path_d, delimiter='\t', unpack=True)
   a,da,b,db,c,dc,d,dd = 0,1,4,5,2,3,6,7
   A,dA,B,dB,C,dC,D,dD = datafile[a],datafile[da],datafile[b],datafile[db],datafile[c],datafile[dc],datafile[d],datafile[dd]


   #A1=(9.809*A/(0.0001*np.pi))*10**(-3)
   #dA1=(9.809/(0.0001*np.pi))*dA*10**(-3)
   B1=(0.0092/B-0.0076/C)*(10**4)
   dB1=np.sqrt((0.0092/(B)**2)**2*(dB)**2+(0.0076/(C)**2)**2*(dC)**2+(1/(B)-1/(C))**2*(0.0005)**2)*10**4

   all_TFM3 = np.append(all_TFM3,B1)
   all_TFM_error3 = np.append(all_TFM_error3,dB1)

#creat axis and draw function
ax = plt.figure(dpi=350).add_subplot(1,1,1)
#ax.set_facecolor('gainsboro')
#plt.errorbar(Bare_Cells,all_TFM,yerr=all_TFM_error, color='royalblue',fmt='.',label='Datenpunkte erste Messung')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
#plt.errorbar(Bare_Cells,all_TFM1,yerr=all_TFM_error1, color='crimson',fmt='.',label='Datenpunkte zweite Messung')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
#plt.errorbar(Bare_Cells,all_TFM2,yerr=all_TFM_error2, color='navy',fmt='.',label='Datenpunkte dritte Messung')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
#plt.errorbar(Bare_Cells,all_TFM3,yerr=all_TFM_error3, color='hotpink',fmt='.',label='Datenpunkte vierte Messung')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))


combined_TFM_A1 = (all_TFM[0]+all_TFM1[0]+all_TFM2[0]+all_TFM3[0])/4
combined_TFM_A9 = (all_TFM[1]+all_TFM1[1]+all_TFM2[1]+all_TFM3[1])/4
combined_TFM_B7 = (all_TFM[2]+all_TFM1[2]+all_TFM2[2]+all_TFM3[2])/4
combined_TFM_C9 = (all_TFM[3]+all_TFM1[3]+all_TFM2[3]+all_TFM3[3])/4

combined_TFM = np.array([combined_TFM_A1,combined_TFM_A9,combined_TFM_B7,combined_TFM_C9])

all_TFM_error_combined = np.array([np.sqrt(1/(1/all_TFM_error[0]**2+1/all_TFM_error1[0]**2+1/all_TFM_error2[0]**2+1/all_TFM_error3[0]**2)),np.sqrt(1/(1/all_TFM_error[1]**2+1/all_TFM_error1[1]**2+1/all_TFM_error2[1]**2+1/all_TFM_error3[1]**2)),np.sqrt(1/(1/all_TFM_error[2]**2+1/all_TFM_error1[2]**2+1/all_TFM_error2[2]**2+1/all_TFM_error3[2]**2)),np.sqrt(1/(1/all_TFM_error[3]**2+1/all_TFM_error1[3]**2+1/all_TFM_error2[3]**2+1/all_TFM_error3[3]**2))])

area = np.array([0,0.246,0.05775,0.3296875])
area_err = np.array([0,0.0039,0.0017,0.0044])

popt,pcov = curve_fit(func,area,combined_TFM, sigma=all_TFM_error_combined)
errors = np.sqrt(np.diag(pcov))


#creat fit
xlin = np.linspace(min(area),max(area),10000)
ylin = func(xlin,popt[0],popt[1])


plt.errorbar(area,combined_TFM,xerr=area_err,yerr=all_TFM_error_combined, color='royalblue',fmt='.',label=r"m = (%s +/- %s)$\frac{K}{W}$" "\n" r"n = (%s +/- %s)$\frac{cm^{2} \cdot K}{W}$"%(str(popt[0].round(2)),str(errors[0].round(2)),str(popt[1].round(2)),str(errors[1].round(2))))

plt.plot(xlin,ylin,color='crimson', label=r'Curve fit: $m \cdot x + n$',lw=1.2)

plt.xlabel(r'Area of missing glue / $cm^{2}$')
ax.tick_params(axis='x', labelsize=6)
plt.ylabel(r'TFM / $\frac{cm^{2} \cdot K}{W}$')
plt.legend(loc='best')
plt.grid(True, which='minor',linestyle='--', color='darkgray', lw=0.5)
plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
plt.tight_layout()
plt.savefig("Batch_%s-%s_area"%(Bare_Cells[0],Bare_Cells[-1]))

