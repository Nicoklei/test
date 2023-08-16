import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

N=0
n=14
start=n-1
run = 0
#---------------Curve-Fit---------------#
#define Function
def func(x,m,n):
   return x*m+n

#get data(every 15 pairs off data the channal changes to the next. So there are 15 pairs of achan0 data and than 15 of achan1 and so on)
path_d = 'Kalibration_0.256V.txt'
datafile = np.loadtxt(path_d, delimiter='	', unpack=True)
a,b,db = 0,1,2
A1,B1,dB1 = datafile[a],datafile[b],datafile[db]

while run<12:
	
	
	A = A1[N:start+N]
	B = B1[N:start+N]
	dB = dB1[N:start+N]

	#curve-fit-program
	popt,pcov = curve_fit(func,A,B)
	errors = np.sqrt(np.diag(pcov))
	print('Steigung: ' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5))+ '\t' + 'y-Achse: ' + str(popt[1].round(5)) + '+/-' + str(errors[1].round(5)))
	print('Nochmal komplett: y=' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5)) + '*x+' + str(popt[1].round(5))+ '+/-' + str(errors[1].round(5)) + '\n')

	#creat fit
	xlin = np.linspace(0, max(A),100)
	ylin = func(xlin,popt[0],popt[1])

	#creat axis and draw function
	ax = plt.figure(dpi=350).add_subplot(1,1,1)

	plt.errorbar(A,B,yerr=dB, color='royalblue',fmt='+',label='Datenpunkte')
	plt.plot(xlin,ylin,color='firebrick', label='Fit-Gerade',lw=1.2)

	plt.xlabel('ADC')
	plt.ylabel('Volt')
	plt.grid(True, which='minor',linestyle='--', color='darkgray', lw=0.5)
	plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
	plt.legend(loc='best')	
	plt.tight_layout()
	plt.savefig('./Bilder0.256/channal%d'%(run+1))
	

	N = N+n
	run +=1
