import numpy as np
from matplotlib import pyplot as plt
import sys

cell = sys.argv[1]

# cell = "1-1783"

data = np.genfromtxt(cell+"/Messung0_"+cell+".txt")

plt.plot(data[:,0])
plt.plot(data[:,2])
plt.plot(data[:,4])
plt.plot(data[:,6])

print(np.mean(data[:,0]),np.mean(data[:,2]),np.mean(data[:,4]),np.mean(data[:,6]))


plt.show()
