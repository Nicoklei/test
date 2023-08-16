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
def func(x,m):
   return 5.670*10**(-8)*m*(x**4-(273.15-40)**4)
def func1(x,m):
   return 5.670*10**(-8)*m*(x**4-(273.15-20)**4)
def func2(x,m):
   return 5.670*10**(-8)*m*(x**4-(273.15-0)**4)
def func3(x,m):
   return 5.670*10**(-8)*m*(x**4-(273.15+20)**4)


a,da,b,db = 0,1,2,3
datafile = np.loadtxt('Leistung_und_Temp_für_-40.txt', delimiter='\t', unpack=True)
A,dA,B,dB=datafile[a],datafile[da],datafile[b],datafile[db]
datafile1 = np.loadtxt('Leistung_und_Temp_für_-20.txt', delimiter='\t', unpack=True)
A1,dA1,B1,dB1=datafile1[a],datafile1[da],datafile1[b],datafile1[db]
datafile2 = np.loadtxt('Leistung_und_Temp_für_0.txt', delimiter='\t', unpack=True)
A2,dA2,B2,dB2=datafile2[a],datafile2[da],datafile2[b],datafile2[db]
datafile3 = np.loadtxt('Leistung_und_Temp_für_20.txt', delimiter='\t', unpack=True)
A3,dA3,B3,dB3=datafile3[a],datafile3[da],datafile3[b],datafile3[db]

#A=A-A[0]
#A1=A1-A1[0]
#A2=A2-A2[0]
#A3=A3-A3[0]

popt,pcov,chi = fit_basic(func,A+273.15,B,p0=[0.0115],y_err=dB)
#creat fit
xlin = np.linspace(min(A+273.15),max(A+273.15),10000)
ylin = func(xlin,*popt)

popt1,pcov1,chi1 = fit_basic(func1,A1+273.15,B1,p0=[0.0115],y_err=dB1)
#creat fit
xlin1 = np.linspace(min(A1+273.15),max(A1+273.15),10000)
ylin1 = func1(xlin1,*popt1)

popt2,pcov2,chi2 = fit_basic(func2,A2+273.15,B2,p0=[0.0115],y_err=dB2)
#creat fit
xlin2 = np.linspace(min(A2+273.15),max(A2+273.15),10000)
ylin2 = func2(xlin2,*popt2)

popt3,pcov3,chi3 = fit_basic(func3,A3+273.15,B3,p0=[0.0115],y_err=dB3)
#creat fit
xlin3 = np.linspace(min(A3+273.15),max(A3+273.15),10000)
ylin3 = func3(xlin3,*popt3)



#creat axis and draw function
ax = plt.figure(dpi=350).add_subplot(1,1,1)
#ax.set_facecolor('gainsboro')
plt.errorbar(A+273.15,B,xerr=dA,yerr=dB, color='royalblue',fmt='.',label=r'-40° $\sigma \cdot m(x⁴-T_{aussen}⁴)$   m = (%s +/- %s)m² chi²= %s'%(str(popt[0].round(5)),str(pcov[0].round(5)),str(chi.round(2))))
plt.errorbar(A1+273.15,B1,xerr=dA1,yerr=dB1, color='navy',fmt='.',label='-20° m = (%s +/- %s)m² \nchi²= %s'%(str(popt1[0].round(5)),str(pcov1[0].round(5)),str(chi1.round(2))))
plt.errorbar(A2+273.15,B2,xerr=dA2,yerr=dB2, color='crimson',fmt='.',label='0° m = (%s +/- %s)m² \nchi²= %s'%(str(popt2[0].round(5)),str(pcov2[0].round(5)),str(chi2.round(2))))
plt.errorbar(A3+273.15,B3,xerr=dA3,yerr=dB3, color='firebrick',fmt='.',label='20° m = (%s +/- %s)m² \nchi²= %s'%(str(popt3[0].round(5)),str(pcov3[0].round(5)),str(chi3.round(2))))
#plt.errorbar(x,B, color='firebrick',fmt='+',label='Channel 2')
#plt.errorbar(x,C, color='yellow',fmt='+',label='Channel 3')
#plt.errorbar(x,D, color='orangered',fmt='+',label='Channel 4')
#plt.errorbar(x,(E+1.7), color='navy',fmt='+',label='Channel 1b')
plt.plot(xlin,ylin,color='royalblue', lw=1.2)
plt.plot(xlin1,ylin1,color='navy', lw=1.2)
plt.plot(xlin2,ylin2,color='crimson', lw=1.2)
plt.plot(xlin3,ylin3,color='firebrick', lw=1.2)


plt.xlabel('Temperatur / °K')
plt.ylabel('Leistung / W')
plt.legend(loc='best')
plt.grid(True, which='minor',linestyle='--', color='darkgray', lw=0.5)
plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
plt.tight_layout()
plt.savefig("Fläche_aus_Leistung_feste_Temp_1")

