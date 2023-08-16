import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

#---------------Curve-Fit---------------#
#define Function
def func(x,m,n,d):
   return n*np.exp(-m*x)+d

#get data(every 15 pairs off data the channal changes to the next. So there are 15 pairs of achan0 data and than 15 of achan1 and so on)

all_TFM = np.array([])
all_TFM_error = np.array([])
all_TFM1 = np.array([])
all_TFM_error1 = np.array([])

Bare_Cells = ['0-0292','0-0303','0-0320','0-0323','0-0334','0-0342']
#Bare_Cells1 = ['Batch1/0-0111','Batch1/0-0112','Batch1/0-0114','Batch1/0-0115','Batch1/0-0116','Batch1/0-0118','Batch1/0-0119','Batch1/0-0120','Batch1/0-0122','Batch1/0-0123','Batch1/0-0124','Batch1/0-0125','Batch1/0-0127','Batch1/0-0128','Batch1/0-0130']

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

#for serial_number in Bare_Cells1:
#   path_d = ('%s/Gemittelte_Werte_%s.txt')%(serial_number,serial_number[7:13])
#   datafile = np.loadtxt(path_d, delimiter='\t', unpack=True)
#   a,da,b,db,c,dc,d,dd = 0,1,4,5,2,3,6,7
#   A,dA,B,dB,C,dC,D,dD = datafile[a],datafile[da],datafile[b],datafile[db],datafile[c],datafile[dc],datafile[d],datafile[dd]


   #A1=(9.809*A/(0.0001*np.pi))*10**(-3)
   #dA1=(9.809/(0.0001*np.pi))*dA*10**(-3)
#   B1=(0.0092/B-0.0076/C)*(10**4)
#   dB1=np.sqrt((0.0092/(B)**2)**2*(dB)**2+(0.0076/(C)**2)**2*(dC)**2+(1/(B)-1/(C))**2*(0.0005)**2)*10**4

#   all_TFM1 = np.append(all_TFM1,B1)
#   all_TFM_error1 = np.append(all_TFM_error1,dB1)

#creat axis and draw function
ax = plt.figure(dpi=350).add_subplot(1,1,1)
#ax.set_facecolor('gainsboro')
plt.errorbar(Bare_Cells,all_TFM,yerr=all_TFM_error, color='royalblue',fmt='.',label='Datapoints')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
#plt.errorbar(Bare_Cells,all_TFM1,yerr=all_TFM_error1, color='crimson',fmt='.',label='Datapoints after cycling')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
#plt.plot(xlin,ylin,color='firebrick', label=r'Fit-Kurve: $n\cdot e^{-m\cdot x}+d$',lw=1.2)


plt.xlabel('Bare Cell serial number')
ax.tick_params(axis='x', labelsize=6)
plt.ylabel(r'TFM / $\frac{cm^{2} \cdot K}{W}$')
plt.legend(loc='best')
plt.grid(True, which='minor',linestyle='--', color='darkgray', lw=0.5)
plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
plt.tight_layout()
plt.savefig("Batch_%s-%s"%(Bare_Cells[0],Bare_Cells[-1]))

