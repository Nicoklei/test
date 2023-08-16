import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import warnings

def red_chisquare(meas, model, meas_err, model_popt):
    """
    Implements the reduced chisquare according to https://en.wikipedia.org/wiki/Reduced_chi-squared_statistic
    Parameters
    ----------
    meas: list, np.array
        Measurement data
    model: list, np.array
        Model data which aims to describe measurement data
    meas_err: list, np.array
        Measurement uncertainty
    model_popt: list, np.array
        Optimized model parameters; only needed for getting degree of freedom (a.k.a len(model_popt))
    
    Returns
    -------
    float: reduced chisquare
    """

    return np.sum(np.square((meas - model) / meas_err)) / (len(meas_err) - len(model_popt) - 1.0)


def fit_basic(fit_func, x, y, p0, y_err=None, return_pcov=False, **fit_kwargs):
    """
    Simple function that takes data as well as error and optimizes *fit_func* to
    it using non-linear least-squares fit provided by scipy.optimize.curve_fit.
    Additional *fit_kwargs* are passed to curve_fit directly
    fit_func: callable
        Function/model whose parameters are to be optimized to describe the *y* data
    x: list, np.array
        Input data x
    y: list, np.array
        Input data y
    y_err: list, np.array
        Uncertainties (1 sigma) on y input data
    p0: list, np.array
        Estimator of starting parameters for fitting routine
    return_pcov: bool
        Whether to append the covariance matrix of the fit parameters to the returned tuple
    Returns
    -------
    tuple: popt, perr, red_chisquare or popt, perr, red_chisquare, pcov 
    """

    if p0 is None:
        warnings.warn("The *curve_fit* routine relies on proper starting parameters *p0* to ensure convergance.", Warning)

    # We are using curve_fit; absolute_sigma=True indicates sigma has unit
    popt, pcov = curve_fit(f=fit_func, xdata=x, ydata=y, sigma=y_err, absolute_sigma=True, p0=p0, **fit_kwargs)

    # Calculate fit errors
    perr = np.sqrt(np.diag(pcov))

    # Calculate reduced chisquare
    red_chi_2 = red_chisquare(meas=y, model=fit_func(x, *popt), meas_err=y_err, model_popt=popt)

    return (popt, perr, red_chi_2) if not return_pcov else (popt, perr, red_chi_2, pcov)


#---------------Curve-Fit---------------#
#define Function
def func(x,m,n):
   return 5.670*10**(-8)*(x**4*m-n)

a,da,b,db,c = 0,1,2,3,16
datafile = np.loadtxt('Messung0_Black_body_20.txt', delimiter='\t', unpack=True)
A,dA,B,dB,C,Temp=datafile[a],datafile[da],datafile[b],datafile[db],datafile[c],datafile[4]
datafile1 = np.loadtxt('Messung1_Black_body_20.txt', delimiter='\t', unpack=True)
A1,dA1,B1,dB1,C1,Temp1=datafile1[a],datafile1[da],datafile1[b],datafile1[db],datafile1[c],datafile1[4]
datafile2 = np.loadtxt('Messung2_Black_body_20.txt', delimiter='\t', unpack=True)
A2,dA2,B2,dB2,C2,Temp2=datafile2[a],datafile2[da],datafile2[b],datafile2[db],datafile2[c],datafile2[4]
datafile3 = np.loadtxt('Messung3_Black_body_20.txt', delimiter='\t', unpack=True)
A3,dA3,B3,dB3,C3,Temp3=datafile3[a],datafile3[da],datafile3[b],datafile3[db],datafile3[c],datafile3[4]
datafile4 = np.loadtxt('Messung4_Black_body_20.txt', delimiter='\t', unpack=True)
A4,dA4,B4,dB4,C4,Temp4=datafile4[a],datafile4[da],datafile4[b],datafile4[db],datafile4[c],datafile4[4]
datafile5 = np.loadtxt('Messung5_Black_body_20.txt', delimiter='\t', unpack=True)
A5,dA5,B5,dB5,C5,Temp5=datafile5[a],datafile5[da],datafile5[b],datafile5[db],datafile5[c],datafile5[4]
datafile6 = np.loadtxt('Messung6_Black_body_20.txt', delimiter='\t', unpack=True)
A6,dA6,B6,dB6,C6,Temp6=datafile6[a],datafile6[da],datafile6[b],datafile6[db],datafile6[c],datafile6[4]
datafile8 = np.loadtxt('Vollständige_Temp_Kurve_.txt', delimiter='\t', unpack=True)
A8,dA8,B8,dB8,C8,TempV=datafile8[a],datafile8[da],datafile8[b],datafile8[db],datafile8[c],datafile8[4]


A=np.sum(A/dA**2)/np.sum(1/dA**2)
dA=1/np.sum(1/dA**2)
B=np.sum(B/dB**2)/np.sum(1/dB**2)
dB=1/np.sum(1/dB**2)
C=np.sum(C)/len(C)

A1=np.sum(A1/dA1**2)/np.sum(1/dA1**2)
dA1=1/np.sum(1/dA1**2)
B1=np.sum(B1/dB1**2)/np.sum(1/dB1**2)
dB1=1/np.sum(1/dB1**2)
C1=np.sum(C1)/len(C1)

A2=np.sum(A2/dA2**2)/np.sum(1/dA2**2)
dA2=1/np.sum(1/dA2**2)
B2=np.sum(B2/dB2**2)/np.sum(1/dB2**2)
dB2=1/np.sum(1/dB2**2)
C2=np.sum(C2)/len(C2)

A3=np.sum(A3/dA3**2)/np.sum(1/dA3**2)
dA3=1/np.sum(1/dA3**2)
B3=np.sum(B3/dB3**2)/np.sum(1/dB3**2)
dB3=1/np.sum(1/dB3**2)
C3=np.sum(C3)/len(C3)

A4=np.sum(A4/dA4**2)/np.sum(1/dA4**2)
dA4=1/np.sum(1/dA4**2)
B4=np.sum(B4/dB4**2)/np.sum(1/dB4**2)
dB4=1/np.sum(1/dB4**2)
C4=np.sum(C4)/len(C4)

A5=np.sum(A5/dA5**2)/np.sum(1/dA5**2)
dA5=1/np.sum(1/dA5**2)
B5=np.sum(B5/dB5**2)/np.sum(1/dB5**2)
dB5=1/np.sum(1/dB5**2)
C5=np.sum(C5)/len(C5)

A6=np.sum(A6/dA6**2)/np.sum(1/dA6**2)
dA6=1/np.sum(1/dA6**2)
B6=np.sum(B6/dB6**2)/np.sum(1/dB6**2)
dB6=1/np.sum(1/dB6**2)
C6=np.sum(C6)/len(C6)

A8=A8[0]
dA8=dA8[0]
B8=B8[0]
dB8=dB8[0]
C8=C8[0]



D = np.array([(A8+B8)/2,(A+B)/2,(A1+B1)/2,(A2+B2)/2,(A3+B3)/2,(A4+B4)/2,(A5+B5)/2,(A6+B6)/2])
dD = [(dA8+dB8)/2+0.5,(dA+dB)/2+0.5,(dA1+dB1)/2+0.5,(dA2+dB2)/2+0.5,(dA3+dB3)/2+0.5,(dA4+dB4)/2+0.5,(dA5+dB5)/2+0.5,(dA6+dB6)/2+0.5]
E = [C8,C,C1,C2,C3,C4,C5,C6]
dE = [0.015,0.044,0.02,0.0313,0.077,0.0598,0.1,0.25]
dE = [C8*0.01+0.01,C*0.01+0.01,C1*0.01+0.01,C2*0.01+0.01,C3*0.01+0.01,C4*0.01+0.01,C5*0.01+0.01,C6*0.01+0.01]
datei1 = open('Leistung_und_Temp_für_20.txt','a')
datei1.write(str(D[0])+'\t'+str(dD[0])+'\t'+str(E[0])+'\t'+str(dE[0])+'\t'+str(TempV[0])+
'\n'+str(D[1])+'\t'+str(dD[1])+'\t'+str(E[1])+'\t'+str(dE[1])+'\t'+str(Temp[0])+
'\n'+str(D[2])+'\t'+str(dD[2])+'\t'+str(E[2])+'\t'+str(dE[2])+'\t'+str(Temp1[0])+
'\n'+str(D[3])+'\t'+str(dD[3])+'\t'+str(E[3])+'\t'+str(dE[3])+'\t'+str(Temp2[0])+
'\n'+str(D[4])+'\t'+str(dD[4])+'\t'+str(E[4])+'\t'+str(dE[4])+'\t'+str(Temp3[0])+
'\n'+str(D[5])+'\t'+str(dD[5])+'\t'+str(E[5])+'\t'+str(dE[5])+'\t'+str(Temp4[0])+
'\n'+str(D[6])+'\t'+str(dD[6])+'\t'+str(E[6])+'\t'+str(dE[6])+'\t'+str(Temp5[0])+
'\n'+str(D[7])+'\t'+str(dD[7])+'\t'+str(E[7])+'\t'+str(dE[7])+'\t'+str(Temp6[0])
)


popt,pcov,chi = fit_basic(func,D+273.15,E,p0=[0.01,70000000],y_err=dE)
errors = np.sqrt(np.diag(pcov))
#creat fit
xlin = np.linspace(min(D+273.15),max(D+273.15),10000)
ylin = func(xlin,*popt)


#creat axis and draw function
ax = plt.figure(dpi=350).add_subplot(1,1,1)
#ax.set_facecolor('gainsboro')
plt.errorbar(D+273.15,E,xerr=dD,yerr=dE, color='royalblue',fmt='.',label='m = (%s +/- %s)m² \nn = (%s +/- %s)m² \nchi²= %s'%(str(popt[0].round(5)),str(pcov[0].round(5)),str((popt[1].round(1)/(273.15+TempV[0])**4).round(5)),str((pcov[1].round(1)/(273.15+TempV[0])**4).round(5)),str(chi.round(2))))
#plt.errorbar(x,B, color='firebrick',fmt='+',label='Channel 2')
#plt.errorbar(x,C, color='yellow',fmt='+',label='Channel 3')
#plt.errorbar(x,D, color='orangered',fmt='+',label='Channel 4')
#plt.errorbar(x,(E+1.7), color='navy',fmt='+',label='Channel 1b')
plt.plot(xlin,ylin,color='firebrick', label=r'Fit-Kurve: $\sigma (x^4 m-n)$',lw=1.2)


plt.xlabel('Temperatur / °K')
plt.ylabel('Leistung / W')
plt.legend(loc='best')
plt.grid(True, which='minor',linestyle='--', color='darkgray', lw=0.5)
plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
plt.tight_layout()
plt.savefig("Fläche_aus_Leistung_20")

