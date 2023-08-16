from lzma import FILTER_LZMA2
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import quad

#---------------Curve-Fit---------------#
#define Function
def func(x,m,n):
   return m*x+n

#get data(every 15 pairs off data the channal changes to the next. So there are 15 pairs of achan0 data and than 15 of achan1 and so on)
#path_d = 'Lambda Messungen/Messung_Lambda_PGS_22_08.txt'
datafile1 = np.loadtxt('Gemittelte_Werte_CERN09_-20.txt', delimiter='\t', unpack=True)
A1,dA1,B1,dB1 = datafile1[2],datafile1[3],datafile1[4],datafile1[5]


data1 = np.loadtxt('Messung0_CERN09_-20.txt', delimiter='\t', unpack=True)
E1,dE1,F1,dF1,G1,dG1,H1,dH1=data1[0],data1[1],data1[2],data1[3],data1[4],data1[5],data1[6],data1[7]
data2 = np.loadtxt('Messung1_CERN09_-20.txt', delimiter='\t', unpack=True)
E2,dE2,F2,dF2,G2,dG2,H2,dH2=data2[0],data2[1],data2[2],data2[3],data2[4],data2[5],data2[6],data2[7]
data3 = np.loadtxt('Messung2_CERN09_-20.txt', delimiter='\t', unpack=True)
E3,dE3,F3,dF3,G3,dG3,H3,dH3=data3[0],data3[1],data3[2],data3[3],data3[4],data3[5],data3[6],data3[7]
data4 = np.loadtxt('Messung3_CERN09_-20.txt', delimiter='\t', unpack=True)
E4,dE4,F4,dF4,G4,dG4,H4,dH4=data4[0],data4[1],data4[2],data4[3],data4[4],data4[5],data4[6],data4[7]
data5 = np.loadtxt('Messung4_CERN09_-20.txt', delimiter='\t', unpack=True)
E5,dE5,F5,dF5,G5,dG5,H5,dH5=data5[0],data5[1],data5[2],data5[3],data5[4],data5[5],data5[6],data5[7]
data6 = np.loadtxt('Messung-1_CERN09_-20.txt', delimiter='\t', unpack=True)
E6,dE6,F6,dF6,G6,dG6,H6,dH6=data6[0],data6[1],data6[2],data6[3],data6[4],data6[5],data6[6],data6[7]

#data1 = np.loadtxt('1Messung/Messung1_CERN-09_Lambda_abhängigkeit_von_Ziel_Temp1.txt', delimiter='\t', unpack=True)
#E1,dE1,F1,dF1,G1,dG1,H1,dH1 = np.append(E1,data1[0]),np.append(dE1,data1[1]),np.append(F1,data1[2]),np.append(dF1,data1[3]),np.append(G1,data1[4]),np.append(dG1,data1[5]),np.append(H1,data1[6]),np.append(dH1,data1[7])
#data2 = np.loadtxt('2Messung/Messung1_CERN-09_Lambda_abhängigkeit_von_Ziel_Temp2.txt', delimiter='\t', unpack=True)
#E2,dE2,F2,dF2,G2,dG2,H2,dH2 = np.append(E2,data2[0]),np.append(dE2,data2[1]),np.append(F2,data2[2]),np.append(dF2,data2[3]),np.append(G2,data2[4]),np.append(dG2,data2[5]),np.append(H2,data2[6]),np.append(dH2,data2[7])
#data3 = np.loadtxt('3Messung/Messung1_CERN-09_Lambda_abhängigkeit_von_Ziel_Temp3.txt', delimiter='\t', unpack=True)
#E3,dE3,F3,dF3,G3,dG3,H3,dH3 = np.append(E3,data3[0]),np.append(dE3,data3[1]),np.append(F3,data3[2]),np.append(dF3,data3[3]),np.append(G3,data3[4]),np.append(dG3,data3[5]),np.append(H3,data3[6]),np.append(dH3,data3[7])
#data4 = np.loadtxt('4Messung/Messung1_CERN-09_Lambda_abhängigkeit_von_Ziel_Temp4.txt', delimiter='\t', unpack=True)
#E4,dE4,F4,dF4,G4,dG4,H4,dH4 = np.append(E4,data4[0]),np.append(dE4,data4[1]),np.append(F4,data4[2]),np.append(dF4,data4[3]),np.append(G4,data4[4]),np.append(dG4,data4[5]),np.append(H4,data4[6]),np.append(dH4,data4[7])
#data5 = np.loadtxt('5Messung/Messung1_CERN-09_Lambda_abhängigkeit_von_Ziel_Temp5.txt', delimiter='\t', unpack=True)
#E5,dE5,F5,dF5,G5,dG5,H5,dH5 = np.append(E5,data5[0]),np.append(dE5,data5[1]),np.append(F5,data5[2]),np.append(dF5,data5[3]),np.append(G5,data5[4]),np.append(dG5,data5[5]),np.append(H5,data5[6]),np.append(dH5,data5[7])
#data6 = np.loadtxt('6Messung/Messung1_CERN-09_Lambda_abhängigkeit_von_Ziel_Temp6.txt', delimiter='\t', unpack=True)
#E6,dE6,F6,dF6,G6,dG6,H6,dH6 = np.append(E6,data6[0]),np.append(dE6,data6[1]),np.append(F6,data6[2]),np.append(dF6,data6[3]),np.append(G6,data6[4]),np.append(dG6,data6[5]),np.append(H6,data6[6]),np.append(dH6,data6[7])

I1=(np.sum(E1)/len(E1)+np.sum(F1)/len(F1)+np.sum(G1)/len(G1)+np.sum(H1)/len(H1))/4
I2=(np.sum(E2)/len(E2)+np.sum(F2)/len(F2)+np.sum(G2)/len(G2)+np.sum(H2)/len(H2))/4
I3=(np.sum(E3)/len(E3)+np.sum(F3)/len(F3)+np.sum(G3)/len(G3)+np.sum(H3)/len(H3))/4
I4=(np.sum(E4)/len(E4)+np.sum(F4)/len(F4)+np.sum(G4)/len(G4)+np.sum(H4)/len(H4))/4
I5=(np.sum(E5)/len(E5)+np.sum(F5)/len(F5)+np.sum(G5)/len(G5)+np.sum(H5)/len(H5))/4
I6=(np.sum(E6)/len(E6)+np.sum(F6)/len(F6)+np.sum(G6)/len(G6)+np.sum(H6)/len(H6))/4

dI1=np.sqrt(1/(1/(np.sqrt((1/np.sum(1/dE1**2))))**2+1/(np.sqrt((1/np.sum(1/dF1**2))))**2+1/(np.sqrt((1/np.sum(1/dG1**2))))**2+1/(np.sqrt((1/np.sum(1/dH1**2))))**2))
dI2=np.sqrt(1/(1/(np.sqrt((1/np.sum(1/dE2**2))))**2+1/(np.sqrt((1/np.sum(1/dF2**2))))**2+1/(np.sqrt((1/np.sum(1/dG2**2))))**2+1/(np.sqrt((1/np.sum(1/dH2**2))))**2))
dI3=np.sqrt(1/(1/(np.sqrt((1/np.sum(1/dE3**2))))**2+1/(np.sqrt((1/np.sum(1/dF3**2))))**2+1/(np.sqrt((1/np.sum(1/dG3**2))))**2+1/(np.sqrt((1/np.sum(1/dH3**2))))**2))
dI4=np.sqrt(1/(1/(np.sqrt((1/np.sum(1/dE4**2))))**2+1/(np.sqrt((1/np.sum(1/dF4**2))))**2+1/(np.sqrt((1/np.sum(1/dG4**2))))**2+1/(np.sqrt((1/np.sum(1/dH4**2))))**2))
dI5=np.sqrt(1/(1/(np.sqrt((1/np.sum(1/dE5**2))))**2+1/(np.sqrt((1/np.sum(1/dF5**2))))**2+1/(np.sqrt((1/np.sum(1/dG5**2))))**2+1/(np.sqrt((1/np.sum(1/dH5**2))))**2))
dI6=np.sqrt(1/(1/(np.sqrt((1/np.sum(1/dE6**2))))**2+1/(np.sqrt((1/np.sum(1/dF6**2))))**2+1/(np.sqrt((1/np.sum(1/dG6**2))))**2+1/(np.sqrt((1/np.sum(1/dH6**2))))**2))

sigma=5.67*10**(-8)
A=0.0115*2
Tout=-20

J1=sigma*(A*(273.15+I1)**4-0.00932*2*(273.15+Tout)**4)
J2=sigma*(A*(273.15+I2)**4-0.00932*2*(273.15+Tout)**4)
J3=sigma*(A*(273.15+I3)**4-0.00932*2*(273.15+Tout)**4)
J4=sigma*(A*(273.15+I4)**4-0.00932*2*(273.15+Tout)**4)
J5=sigma*(A*(273.15+I5)**4-0.00932*2*(273.15+Tout)**4)
J6=sigma*(A*(273.15+I6)**4-0.00932*2*(273.15+Tout)**4)

M1=[(np.sum(E1)/len(E1)-np.sum(F1)/len(F1))/5,(np.sum(E2)/len(E2)-np.sum(F2)/len(F2))/5,(np.sum(E3)/len(E3)-np.sum(F3)/len(F3))/5,(np.sum(E4)/len(E4)-np.sum(F4)/len(F4))/5,(np.sum(E5)/len(E5)-np.sum(F5)/len(F5))/5,(np.sum(E6)/len(E6)-np.sum(F6)/len(F6))/5]
M2=[(np.sum(G1)/len(G1)-np.sum(H1)/len(H1))/5,(np.sum(G2)/len(G2)-np.sum(H2)/len(H2))/5,(np.sum(G3)/len(G3)-np.sum(H3)/len(H3))/5,(np.sum(G4)/len(G4)-np.sum(H4)/len(H4))/5,(np.sum(G5)/len(G5)-np.sum(H5)/len(H5))/5,(np.sum(G6)/len(G6)-np.sum(H6)/len(H6))/5]
N1=[np.sum(F1)/len(F1),np.sum(F2)/len(F2),np.sum(F3)/len(F3),np.sum(F4)/len(F4),np.sum(F5)/len(F5),np.sum(F6)/len(F6)]
N2=[np.sum(H1)/len(H1),np.sum(H2)/len(H2),np.sum(H3)/len(H3),np.sum(H4)/len(H4),np.sum(H5)/len(H5),np.sum(H6)/len(H6)]

def wärm(x,m,n):
   sigma=5.67*10**(-8)
   A = np.pi
   return sigma*A*(273.15+m*x+n)**4

def wärm1(x,m,n):
   sigma=5.67*10**(-8)
   A = 4*5.21
   return sigma*A*(273.15+m*x+n)**4

A=5.21**2-1**2*np.pi

#L1 = quad(wärm2, -0.34, 7.7, args=(M1[0],N1[0]))+quad(wärm2, -2.7, 5.34, args=(M2[0],N2[0]))+quad(wärm3, 7.7, 8.2, args=(M1[0],N1[0]))+quad(wärm3, -3.2, -2.7, args=(M2[0],N2[0]))
#O1 = sigma*A*((273.15+M2[0]*-2.7+N2[0])**4-(273.15+23)**4)+sigma*A*((273.15+M1[0]*7.7+N1[0])**4-(273.15+23)**4)+sigma*A*((273.15+M2[0]*-3.2+N2[0])**4-(273.15+23)**4)+sigma*A*((273.15+M1[0]*8.2+N1[0])**4-(273.15+23)**4)
#L2 = quad(wärm, -0.34, 7.7, args=(M1[1],N1[1]))+quad(wärm, -2.7, 5.34, args=(M2[1],N2[1]))+quad(wärm1, 7.7, 8.2, args=(M1[1],N1[1]))+quad(wärm1, -3.2, -2.7, args=(M2[1],N2[1]))
#O2 = sigma*(A*(273.15+M2[1]*-2.7+N2[1])**4-93.2*(273.15+23)**4)+sigma*(A*(273.15+M1[1]*7.7+N1[1])**4-93.2*(273.15+23)**4)+sigma*(A*(273.15+M2[1]*-3.2+N2[1])**4-93.2*(273.15+23)**4)+sigma*(A*(273.15+M1[1]*8.2+N1[1])**4-93.2*(273.15+23)**4)
#L3 = quad(wärm, -0.34, 7.7, args=(M1[2],N1[2]))+quad(wärm, -2.7, 5.34, args=(M2[2],N2[2]))+quad(wärm1, 7.7, 8.2, args=(M1[2],N1[2]))+quad(wärm1, -3.2, -2.7, args=(M2[2],N2[2]))
#O3 = sigma*(A*(273.15+M2[2]*-2.7+N2[2])**4-93.2*(273.15+23)**4)+sigma*(A*(273.15+M1[2]*7.7+N1[2])**4-93.2*(273.15+23)**4)+sigma*(A*(273.15+M2[2]*-3.2+N2[2])**4-93.2*(273.15+23)**4)+sigma*(A*(273.15+M1[2]*8.2+N1[2])**4-93.2*(273.15+23)**4)
#L4 = quad(wärm, -0.34, 7.7, args=(M1[3],N1[3]))+quad(wärm, -2.7, 5.34, args=(M2[3],N2[3]))+quad(wärm1, 7.7, 8.2, args=(M1[3],N1[3]))+quad(wärm1, -3.2, -2.7, args=(M2[3],N2[3]))
#O4 = sigma*(A*(273.15+M2[3]*-2.7+N2[3])**4-93.2*(273.15+23)**4)+sigma*(A*(273.15+M1[3]*7.7+N1[3])**4-93.2*(273.15+23)**4)+sigma*(A*(273.15+M2[3]*-3.2+N2[3])**4-93.2*(273.15+23)**4)+sigma*(A*(273.15+M1[3]*8.2+N1[3])**4-93.2*(273.15+23)**4)
#L5 = quad(wärm, -0.34, 7.7, args=(M1[4],N1[4]))+quad(wärm, -2.7, 5.34, args=(M2[4],N2[4]))+quad(wärm1, 7.7, 8.2, args=(M1[4],N1[4]))+quad(wärm1, -3.2, -2.7, args=(M2[4],N2[4]))
#O5 = sigma*(A*(273.15+M2[4]*-2.7+N2[4])**4-93.2*(273.15+23)**4)+sigma*(A*(273.15+M1[4]*7.7+N1[4])**4-93.2*(273.15+23)**4)+sigma*(A*(273.15+M2[4]*-3.2+N2[4])**4-93.2*(273.15+23)**4)+sigma*(A*(273.15+M1[4]*8.2+N1[4])**4-93.2*(273.15+23)**4)
#L6 = quad(wärm, -0.34, 7.7, args=(M1[5],N1[5]))+quad(wärm, -2.7, 5.34, args=(M2[5],N2[5]))+quad(wärm1, 7.7, 8.2, args=(M1[5],N1[5]))+quad(wärm1, -3.2, -2.7, args=(M2[5],N2[5]))
#O6 = sigma*(A*(273.15+M2[5]*-2.7+N2[5])**4-93.2*(273.15+23)**4)+sigma*(A*(273.15+M1[5]*7.7+N1[5])**4-93.2*(273.15+23)**4)+sigma*(A*(273.15+M2[5]*-3.2+N2[5])**4-93.2*(273.15+23)**4)+sigma*(A*(273.15+M1[5]*8.2+N1[5])**4-93.2*(273.15+23)**4)
#L7 = quad(wärm, -0.34, 7.7, args=(M1[6],N1[6]))+quad(wärm, -2.7, 5.34, args=(M2[6],N2[6]))+quad(wärm1, 7.7, 8.2, args=(M1[6],N1[6]))+quad(wärm1, -3.2, -2.7, args=(M2[6],N2[6]))
#O7 = sigma*(A*(273.15+M2[6]*-2.7+N2[6])**4-93.2*(273.15+23)**4)+sigma*(A*(273.15+M1[6]*7.7+N1[6])**4-93.2*(273.15+23)**4)+sigma*(A*(273.15+M2[6]*-3.2+N2[6])**4-93.2*(273.15+23)**4)+sigma*(A*(273.15+M1[6]*8.2+N1[6])**4-93.2*(273.15+23)**4)
#L8 = quad(wärm, -0.34, 7.7, args=(M1[7],N1[7]))+quad(wärm, -2.7, 5.34, args=(M2[7],N2[7]))+quad(wärm1, 7.7, 8.2, args=(M1[7],N1[7]))+quad(wärm1, -3.2, -2.7, args=(M2[7],N2[7]))
#O8 = sigma*(A*(273.15+M2[7]*-2.7+N2[7])**4-93.2*(273.15+23)**4)+sigma*(A*(273.15+M1[7]*7.7+N1[7])**4-93.2*(273.15+23)**4)+sigma*(A*(273.15+M2[7]*-3.2+N2[7])**4-93.2*(273.15+23)**4)+sigma*(A*(273.15+M1[7]*8.2+N1[7])**4-93.2*(273.15+23)**4)
#print(L1[0]/10000,L1[2]/10000,L1[4]/10000,L1[6]/10000,O1/10000,sigma*(273.15+24)**4/10000,sigma*93.2*(273.15+24)**4/10000)


L1= quad(wärm, -0.34, 7.7, args=(M1[0],N1[0]))+quad(wärm, -2.7, 5.34, args=(M2[0],N2[0]))+quad(wärm1, 7.7, 8.2, args=(M1[0],N1[0]))+quad(wärm1, -3.2, -2.7, args=(M2[0],N2[0]))
O1 = sigma*(A*(273.15+M2[0]*-2.7+N2[0])**4)+sigma*(A*(273.15+M1[0]*7.7+N1[0])**4)+sigma*(A*(273.15+M2[0]*-3.2+N2[0])**4)+sigma*(A*(273.15+M1[0]*8.2+N1[0])**4)
L2 = quad(wärm, -0.34, 7.7, args=(M1[1],N1[1]))+quad(wärm, -2.7, 5.34, args=(M2[1],N2[1]))+quad(wärm1, 7.7, 8.2, args=(M1[1],N1[1]))+quad(wärm1, -3.2, -2.7, args=(M2[1],N2[1]))
O2 = sigma*(A*(273.15+M2[1]*-2.7+N2[1])**4)+sigma*(A*(273.15+M1[1]*7.7+N1[1])**4)+sigma*(A*(273.15+M2[1]*-3.2+N2[1])**4)+sigma*(A*(273.15+M1[1]*8.2+N1[1])**4)
L3 = quad(wärm, -0.34, 7.7, args=(M1[2],N1[2]))+quad(wärm, -2.7, 5.34, args=(M2[2],N2[2]))+quad(wärm1, 7.7, 8.2, args=(M1[2],N1[2]))+quad(wärm1, -3.2, -2.7, args=(M2[2],N2[2]))
O3 = sigma*(A*(273.15+M2[2]*-2.7+N2[2])**4)+sigma*(A*(273.15+M1[2]*7.7+N1[2])**4)+sigma*(A*(273.15+M2[2]*-3.2+N2[2])**4)+sigma*(A*(273.15+M1[2]*8.2+N1[2])**4)
L4 = quad(wärm, -0.34, 7.7, args=(M1[3],N1[3]))+quad(wärm, -2.7, 5.34, args=(M2[3],N2[3]))+quad(wärm1, 7.7, 8.2, args=(M1[3],N1[3]))+quad(wärm1, -3.2, -2.7, args=(M2[3],N2[3]))
O4 = sigma*(A*(273.15+M2[3]*-2.7+N2[3])**4)+sigma*(A*(273.15+M1[3]*7.7+N1[3])**4)+sigma*(A*(273.15+M2[3]*-3.2+N2[3])**4)+sigma*(A*(273.15+M1[3]*8.2+N1[3])**4)
L5 = quad(wärm, -0.34, 7.7, args=(M1[4],N1[4]))+quad(wärm, -2.7, 5.34, args=(M2[4],N2[4]))+quad(wärm1, 7.7, 8.2, args=(M1[4],N1[4]))+quad(wärm1, -3.2, -2.7, args=(M2[4],N2[4]))
O5 = sigma*(A*(273.15+M2[4]*-2.7+N2[4])**4)+sigma*(A*(273.15+M1[4]*7.7+N1[4])**4)+sigma*(A*(273.15+M2[4]*-3.2+N2[4])**4)+sigma*(A*(273.15+M1[4]*8.2+N1[4])**4)
L6 = quad(wärm, -0.34, 7.7, args=(M1[5],N1[5]))+quad(wärm, -2.7, 5.34, args=(M2[5],N2[5]))+quad(wärm1, 7.7, 8.2, args=(M1[5],N1[5]))+quad(wärm1, -3.2, -2.7, args=(M2[5],N2[5]))
O6 = sigma*(A*(273.15+M2[5]*-2.7+N2[5])**4)+sigma*(A*(273.15+M1[5]*7.7+N1[5])**4)+sigma*(A*(273.15+M2[5]*-3.2+N2[5])**4)+sigma*(A*(273.15+M1[5]*8.2+N1[5])**4)

print(L1[0]/10000,L1[2]/10000,L1[4]/10000,L1[6]/10000,O1/10000,sigma*93.2*(273.15+Tout)**4/10000)

print(((L1[0]+L1[2]+L1[4]+L1[6]+O1)-sigma*93.2*2*(273.15+Tout)**4)/10000,J1)
print(((L2[0]+L2[2]+L2[4]+L2[6]+O2)-sigma*93.2*2*(273.15+Tout)**4)/10000,J2)
print(((L3[0]+L3[2]+L3[4]+L3[6]+O3)-sigma*93.2*2*(273.15+Tout)**4)/10000,J3)
print(((L4[0]+L4[2]+L4[4]+L4[6]+O4)-sigma*93.2*2*(273.15+Tout)**4)/10000,J4)
print(((L5[0]+L5[2]+L5[4]+L5[6]+O5)-sigma*93.2*2*(273.15+Tout)**4)/10000,J5)
print(((L6[0]+L6[2]+L6[4]+L6[6]+O6)-sigma*93.2*2*(273.15+Tout)**4)/10000,J6)

K1=(11.727-((L1[0]+L1[2]+L1[4]+L1[6]+O1)-sigma*93.2*2*(273.15+Tout)**4)/10000)*0.05/(0.01**2*np.pi*(np.sum(E1)/len(E1)-np.sum(F1)/len(F1)))
K2=(11.727-((L2[0]+L2[2]+L2[4]+L2[6]+O2)-sigma*93.2*2*(273.15+Tout)**4)/10000)*0.05/(0.01**2*np.pi*(np.sum(E2)/len(E2)-np.sum(F2)/len(F2)))
K3=(11.727-((L3[0]+L3[2]+L3[4]+L3[6]+O3)-sigma*93.2*2*(273.15+Tout)**4)/10000)*0.05/(0.01**2*np.pi*(np.sum(E3)/len(E3)-np.sum(F3)/len(F3)))
K4=(11.727-((L4[0]+L4[2]+L4[4]+L4[6]+O4)-sigma*93.2*2*(273.15+Tout)**4)/10000)*0.05/(0.01**2*np.pi*(np.sum(E4)/len(E4)-np.sum(F4)/len(F4)))
K5=(11.727-((L5[0]+L5[2]+L5[4]+L5[6]+O5)-sigma*93.2*2*(273.15+Tout)**4)/10000)*0.05/(0.01**2*np.pi*(np.sum(E5)/len(E5)-np.sum(F5)/len(F5)))
K6=(11.727-((L6[0]+L6[2]+L6[4]+L6[6]+O6)-sigma*93.2*2*(273.15+Tout)**4)/10000)*0.05/(0.01**2*np.pi*(np.sum(E6)/len(E6)-np.sum(F6)/len(F6)))

dK1=0.05/(0.01**2*np.pi*(np.sum(E1)/len(E1)-np.sum(F1)/len(F1)))*((L1[0]+L1[2]+L1[4]+L1[6]+O1)-sigma*93.2*2*(273.15+Tout)**4)/10000*0.2
dK2=0.05/(0.01**2*np.pi*(np.sum(E2)/len(E2)-np.sum(F2)/len(F2)))*((L2[0]+L2[2]+L2[4]+L2[6]+O2)-sigma*93.2*2*(273.15+Tout)**4)/10000*0.2
dK3=0.05/(0.01**2*np.pi*(np.sum(E3)/len(E3)-np.sum(F3)/len(F3)))*((L3[0]+L3[2]+L3[4]+L3[6]+O3)-sigma*93.2*2*(273.15+Tout)**4)/10000*0.2
dK4=0.05/(0.01**2*np.pi*(np.sum(E4)/len(E4)-np.sum(F4)/len(F4)))*((L4[0]+L4[2]+L4[4]+L4[6]+O4)-sigma*93.2*2*(273.15+Tout)**4)/10000*0.2
dK5=0.05/(0.01**2*np.pi*(np.sum(E5)/len(E5)-np.sum(F5)/len(F5)))*((L5[0]+L5[2]+L5[4]+L5[6]+O5)-sigma*93.2*2*(273.15+Tout)**4)/10000*0.2
dK6=0.05/(0.01**2*np.pi*(np.sum(E6)/len(E6)-np.sum(F6)/len(F6)))*((L6[0]+L6[2]+L6[4]+L6[6]+O6)-sigma*93.2*2*(273.15+Tout)**4)/10000*0.2

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
plt.errorbar(I1,A1[0],xerr=dI1,yerr=dA1[0], color='crimson',fmt='.',label='Mittelwerte der aus der Messung erhaltenen Datenpunkte')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
plt.errorbar(I2,A1[1],xerr=dI2,yerr=dA1[1], color='crimson',fmt='.')#,label='Datenpunkte aus zweiter Messung')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
plt.errorbar(I3,A1[2],xerr=dI3,yerr=dA1[2], color='crimson',fmt='.')#,label='Datenpunkte aus erster Messung')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
plt.errorbar(I4,A1[3],xerr=dI4,yerr=dA1[3], color='crimson',fmt='.')#,label='Datenpunkte aus erster Messung')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
plt.errorbar(I5,A1[4],xerr=dI5,yerr=dA1[4], color='crimson',fmt='.')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
plt.errorbar(I6,A1[5],xerr=dI6,yerr=dA1[5], color='crimson',fmt='.')#,label='Datenpunkte aus erster Messung')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))

plt.errorbar(I1,K1,xerr=dI1,yerr=dK1, color='royalblue',fmt='.',label='Um Strahlungsleistung Korrigierte Datenpunkte')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
plt.errorbar(I2,K2,xerr=dI2,yerr=dK2, color='royalblue',fmt='.')#,label='Datenpunkte aus zweiter Messung')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
plt.errorbar(I3,K3,xerr=dI3,yerr=dK3, color='royalblue',fmt='.')#,label='Datenpunkte aus erster Messung')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
plt.errorbar(I4,K4,xerr=dI4,yerr=dK4, color='royalblue',fmt='.')#,label='Datenpunkte aus erster Messung')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
plt.errorbar(I5,K5,xerr=dI5,yerr=dK5, color='royalblue',fmt='.')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))
plt.errorbar(I6,K6,xerr=dI6,yerr=dK6, color='royalblue',fmt='.')#,label='Datenpunkte aus erster Messung')#'m = %s +/- %s \nn = %s +/- %s \nd = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5)),str(popt[2].round(5)),str(errors[2].round(5))))

#plt.errorbar(x,B, color='firebrick',fmt='+',label='Channel 2')
#plt.errorbar(x,C, color='yellow',fmt='+',label='Channel 3')
#plt.errorbar(x,D, color='orangered',fmt='+',label='Channel 4')
#plt.errorbar(x,(E+1.7), color='navy',fmt='+',label='Channel 1b')
#plt.plot(xlin,ylin,color='firebrick', label='Fit-Kurve: n*exp(-m*x)+d',lw=1.2)

plt.xlabel('Mittlere Temperatur beider Kalorimeter / °C')
plt.ylabel(r'Wärmeleitfähigkeit / $\frac{W}{m \cdot K}$')#r'TFM / $\frac{cm^{2} \cdot K}{W}$')
plt.legend(loc='best')
plt.grid(True, which='minor',linestyle='--', color='darkgray', lw=0.5)
plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
plt.tight_layout()
plt.savefig("Lambda_oben_CERN-09_gegen_Temp_mit_korr_-20°C")

