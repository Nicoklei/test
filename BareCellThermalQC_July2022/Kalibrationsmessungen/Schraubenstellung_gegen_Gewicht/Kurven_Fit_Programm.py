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

A0=np.array([0,0.5,0.75,1,1.25,1.5,1.75,2,2.25,2.5,2.75,3,3.25,3.5,3.75,4,4.125,4.25,4.375])
C0=np.array([1.917,5.368,7.094,8.82,10.545,12.271,14.859,15.772,17.448,19.432,21.762,23.229,24.35,26.939,29.527,30.821,33.237,37.292,48.509])
B=np.array([0.023,0.046,0.058,0.07,0.083,0.095,0.114,0.12,0.133,0.422,0.164,0.313,0.183,0.202,0.221,0.345,0.246,0.277,0.359])
D=np.array([0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05])

#A=A1[0]-(A1+B1)/2

x = np.array([])
for i in range(0,150):
   x = np.append(x,i)

#curve-fit-program
popt,pcov = curve_fit(func,A0[0:15]*1.5,C0[0:15]*9.80665)
errors = np.sqrt(np.diag(pcov))
print('Steigung: ' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5))+ '\n' + 'y-Achse: ' + str(popt[1].round(5)) + '+/-' + str(errors[1].round(5)))
print('Nochmal komplett: y=' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5)) + '*x+' + str(popt[1].round(5))+ '+/-' + str(errors[1].round(5)))

#creat fit
xlin = np.linspace(min(A0*1.5),6,1000)
ylin = func(xlin,popt[0],popt[1])

#creat axis and draw function
ax = plt.figure(dpi=350).add_subplot(1,1,1)
#ax.set_facecolor('gainsboro')
plt.errorbar(A0*1.5,C0*9.80665,xerr=D*1.5,yerr=B*9.80665, color='royalblue',fmt='.',label='m = (%s +/- %s)N/mm'%(str(popt[0].round(1)),str(errors[0].round(1))))
#plt.errorbar(x,B, color='firebrick',fmt='+',label='Channel 2')
#plt.errorbar(x,C, color='yellow',fmt='+',label='Channel 3')
#plt.errorbar(x,D, color='orangered',fmt='+',label='Channel 4')
#plt.errorbar(x,(E+1.7), color='navy',fmt='+',label='Channel 1b')
plt.plot(xlin,ylin,color='firebrick', label='Fit-Gerade an den linearen Abschnitt',lw=1.2)

plt.xlabel(r'$\Delta$ l/mm')
plt.ylabel('Newton/N')
plt.legend(loc='best')
plt.grid(True, which='minor',linestyle='--', color='darkgray', lw=0.5)
plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
plt.tight_layout()
plt.savefig("Federkonstante")

