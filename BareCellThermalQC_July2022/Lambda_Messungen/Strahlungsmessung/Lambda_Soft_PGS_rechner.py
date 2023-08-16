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

#get data(every 15 pairs off data the channal changes to the next. So there are 15 pairs of achan0 data and than 15 of achan1 and so on)
a,da,b,db,c = 0,1,2,3,16
datafile = np.loadtxt('Vakuum_zwischen_Stäben/Messung2_Vakuum_zwischen_Stäben.txt', delimiter='\t', unpack=True)
A,dA,B,dB,C=datafile[a],datafile[da],datafile[b],datafile[db],datafile[c]
datafile1 = np.loadtxt('Vakuum_zwischen_Stäben1/Messung2_Vakuum_zwischen_Stäben1.txt', delimiter='\t', unpack=True)
A1,dA1,B1,dB1,C1=datafile1[a],datafile1[da],datafile1[b],datafile1[db],datafile1[c]
datafile2 = np.loadtxt('Vakuum_zwischen_Stäben2/Messung1_Vakuum_zwischen_Stäben2.txt', delimiter='\t', unpack=True)
A2,dA2,B2,dB2,C2=datafile2[a],datafile2[da],datafile2[b],datafile2[db],datafile2[c]
datafile3 = np.loadtxt('Vakuum_zwischen_Stäben3/Messung1_Vakuum_zwischen_Stäben3.txt', delimiter='\t', unpack=True)
A3,dA3,B3,dB3,C3=datafile3[a],datafile3[da],datafile3[b],datafile3[db],datafile3[c]
datafile4 = np.loadtxt('Vakuum_zwischen_Stäben4/Messung1_Vakuum_zwischen_Stäben4.txt', delimiter='\t', unpack=True)
A4,dA4,B4,dB4,C4=datafile4[a],datafile4[da],datafile4[b],datafile4[db],datafile4[c]
datafile5 = np.loadtxt('Vakuum_zwischen_Stäben5/Messung1_Vakuum_zwischen_Stäben5.txt', delimiter='\t', unpack=True)
A5,dA5,B5,dB5,C5=datafile5[a],datafile5[da],datafile5[b],datafile5[db],datafile5[c]
datafile6 = np.loadtxt('Vakuum_zwischen_Stäben6/Messung1_Vakkum_zwischen_Stäben6.txt', delimiter='\t', unpack=True)
A6,dA6,B6,dB6,C6=datafile6[a],datafile6[da],datafile6[b],datafile6[db],datafile6[c]
datafile7 = np.loadtxt('Vakuum_zwischen_Stäben7/Messung1_Vakkum_zwischen_Stäben7.txt', delimiter='\t', unpack=True)
A7,dA7,B7,dB7,C7=datafile7[a],datafile7[da],datafile7[b],datafile7[db],datafile7[c]


A=np.sum(A)/len(A)
#dA=np.sum(dA)/len(dA)
B=np.sum(B)/len(B)
dB=np.sum(dB)/len(dB)
C=np.sum(C)/len(C)

A1=np.sum(A1)/len(A1)
#dA1=np.sum(dA1)/len(dA1)
B1=np.sum(B1)/len(B1)
dB1=np.sum(dB1)/len(dB1)
C1=np.sum(C1)/len(C1)

A2=np.sum(A2)/len(A2)
#dA2=np.sum(dA2)/len(dA2)
B2=np.sum(B2)/len(B2)
dB2=np.sum(dB2)/len(dB2)
C2=np.sum(C2)/len(C2)

A3=np.sum(A3)/len(A3)
#dA3=np.sum(dA3)/len(dA3)
B3=np.sum(B3)/len(B3)
dB3=np.sum(dB3)/len(dB3)
C3=np.sum(C3)/len(C3)

A4=np.sum(A4)/len(A4)
#dA4=np.sum(dA4)/len(dA4)
B4=np.sum(B4)/len(B4)
dB4=np.sum(dB4)/len(dB4)
C4=np.sum(C4)/len(C4)

A5=np.sum(A5)/len(A5)
#dA5=np.sum(dA5)/len(dA5)
B5=np.sum(B5)/len(B5)
dB5=np.sum(dB5)/len(dB5)
C5=np.sum(C5)/len(C5)

A6=np.sum(A6)/len(A6)
#dA6=np.sum(dA6)/len(dA6)
B6=np.sum(B6)/len(B6)
dB6=np.sum(dB6)/len(dB6)
C6=np.sum(C6)/len(C6)

A7=np.sum(A7)/len(A7)
#dA7=np.sum(dA7)/len(dA7)
B7=np.sum(B7)/len(B7)
dB7=np.sum(dB7)/len(dB7)
C7=np.sum(C7)/len(C7)



D = np.array([A,A1,A3,A4,A5,A6,A7])
dD = [dA[0],dA1[0],dA3[0],dA4[0],dA5[0],dA6[0],dA7[0]]
E = [C,C1,C3,C4,C5,C6,C7]
dE = [0.044,0.02,0.0313,0.077,0.0598,0.096,0.12]

#curve-fit-program
popt,pcov = curve_fit(func,D+273.15,E,sigma=dE)
errors = np.sqrt(np.diag(pcov))
#creat fit
xlin = np.linspace(min(D+273.15),max(D+273.15),1000)
ylin = func(xlin,*popt)

popt,pcov,chi = fit_basic(func,D+273.15,E,p0=[0,0],y_err=dE)


#creat axis and draw function
ax = plt.figure(dpi=350).add_subplot(1,1,1)
#ax.set_facecolor('gainsboro')
plt.errorbar(D+273.15,E,xerr=dD,yerr=dE, color='royalblue',fmt='.',label='m = (%s +/- %s)m² \nn = (%s +/- %s)T⁴m² \nchi²= %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(1)),str(errors[1].round(1)),str(chi.round(2))))
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
plt.savefig("Fläche_aus_Leistung_Fehler")

