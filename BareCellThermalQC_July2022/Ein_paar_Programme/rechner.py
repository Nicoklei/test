import numpy as np
import math
import uncertainties.unumpy as unp
from uncertainties import ufloat

x= ufloat(0.01,0.0001)

R1=ufloat(100,1)
R2=ufloat(99.633963,0.00324)
S1=ufloat(1.7,0.0)
S0=ufloat(3.3,0.0)

#T=((-3.9083*10**(-3)*100+math.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(R1*(S1/(S0-S1))))))/(2*(-5.775*10**(-7)*100)))
#print(T)

U=R1*S1/(S0-S1)
U1=R2*S1/(S0-S1)

print(U)
print(U1)
