# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import numpy as np
#from matplotlib import pyplot as plt
#from scipy.optimize import curve_fit

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c, address=0x48)
bds = ADS.ADS1115(i2c, address=0x49)
cds = ADS.ADS1115(i2c, address=0x4a)
# you can specify an I2C adress instead of the default 0x48
# ads = ADS.ADS1115(i2c, address=0x49)

#text input
name = input("Namen eingeben: ")

#put in the different voltage values
#gain1 = input("Verschiedene Volt bereiche für ADC a mit 1,2,4,8,16 auswählen:")
#gain2 = input("Verschiedene Volt bereiche für ADC b mit 1,2,4,8,16 auswählen:")
#gain3 = input("Verschiedene Volt bereiche für ADC c mit 1,2,4,8,16 auswählen:")


ads.gain = 16 #gain1
bds.gain = 16 #gain2
cds.gain = 16 #gain3

# Create single-ended input on channel 0
achan0 = AnalogIn(ads, ADS.P0)
achan1 = AnalogIn(ads, ADS.P1)
achan2 = AnalogIn(ads, ADS.P2)
achan3 = AnalogIn(ads, ADS.P3)

bchan0 = AnalogIn(bds, ADS.P0)
bchan1 = AnalogIn(bds, ADS.P1)
bchan2 = AnalogIn(bds, ADS.P2)
bchan3 = AnalogIn(bds, ADS.P3)

cchan0 = AnalogIn(cds, ADS.P0)
cchan1 = AnalogIn(cds, ADS.P1)
cchan2 = AnalogIn(cds, ADS.P2)
cchan3 = AnalogIn(cds, ADS.P3)

# Create differential input between channel 0 and 1
# chan = AnalogIn(ads, ADS.P0, ADS.P1)

#Variables
b=0
avarage = 10
counter1=0
counter2=0
counter3=0
counter4=0
counter5=0
counter6=0
counter7=0
counter8=0
counter9=0
counter10=0
counter11=0
counter12=0
counter_rate = 14

#open txt to write in the values
datei = open(name,'a') 

print("{:>5}\t{:>5}".format("raw", "V"))

    # print("{:>5.3f}".format(2*achan0.voltage))
    # print("{:>5.3f}".format(2*achan1.voltage))
    # print("{:>5.3f}".format(2*achan2.voltage))
    # print("{:>5.3f}".format(2*achan3.voltage))
    # print("----------------------------------------------------")
    
    #print("achan0:")
    #print("{:>5}\t{:>5.3f}".format(achan0.value, achan0.voltage))
    #print("{:>5}\t{:>5.3f}".format(achan1.value, achan1.voltage))
    #print("{:>5}\t{:>5.3f}".format(achan2.value, achan2.voltage))
    #print("{:>5}\t{:>5.3f}".format(achan3.value, achan3.voltage))
    #print("----------------------------------------------------")
    #print("{:>5}\t{:>5.3f}".format(bchan0.value, bchan0.voltage))
    #print("{:>5}\t{:>5.3f}".format(bchan1.value, bchan1.voltage))
    #print("{:>5}\t{:>5.3f}".format(bchan2.value, bchan2.voltage))
    #print("{:>5}\t{:>5.3f}".format(bchan3.value, bchan3.voltage))
    #print("----------------------------------------------------")
    #print("{:>5}\t{:>5.3f}".format(cchan0.value, cchan0.voltage))
    #print("{:>5}\t{:>5.3f}".format(cchan1.value, cchan1.voltage))
    #print("{:>5}\t{:>5.3f}".format(cchan2.value, cchan2.voltage))
    #print("{:>5}\t{:>5.3f}".format(cchan3.value, cchan3.voltage))
    #print("----------------------------------------------------")
    
    # iina0, iind0 = 4*achan0.voltage - cchan0.voltage, 4*achan0.voltage -bchan0.voltage
    # iina1, iind1 = 4*achan1.voltage - cchan1.voltage, 4*achan1.voltage -bchan1.voltage
    # iina2, iind2 = 4*achan2.voltage - cchan2.voltage, 4*achan2.voltage -bchan2.voltage
    # iina3, iind3 = 4*achan3.voltage - cchan3.voltage, 4*achan3.voltage -bchan3.voltage

    # print("{:>5.3f}".format(iina0/1))
    # print("{:>5.3f}".format(iind0/0.867))
    # print("----------------------------------------------------")
    # print("{:>5.3f}".format(iina1/1))
    # print("{:>5.3f}".format(iind1/0.867))
    # print("----------------------------------------------------")
    # print("{:>5.3f}".format(iina2/1))
    # print("{:>5.3f}".format(iind2/0.867))
    # print("----------------------------------------------------")
    # print("{:>5.3f}".format(iina3/1))
    # print("{:>5.3f}".format(iind3/0.867))
    # print("----------------------------------------------------")
    # print("----------------------------------------------------")
#while-loops to avarage over and write the data into a txt document
while counter1 < counter_rate: 
    print("achan0:")
    print("{:>5}\t{:>5.3f}".format(achan0.value, achan0.voltage))
    print("----------------------------------------------------")
    
    
    #creat an array with 10 diffrent voltages
    save = np.array([])
    timer = 0
    while timer < avarage:
       save = np.append(save,achan0.voltage)
       time.sleep(0.01)
       timer += 1
    #print(save)
    sigma_var = save-(np.sum(save)/avarage)
    #print(sigma_var)
    sigma = np.sqrt(np.sum(np.square(sigma_var))/avarage)
    #print(sigma)

    #take the average of the 10 values and print it in a .txt
    a = np.array([])
    a = np.append(a,round((np.sum(save)/avarage),3))
    print(a)
    if a!=b:
        datei.write("\n{:>5}\t{:>5.4f}".format(achan0.value,np.sum(save)/avarage) + "\t" + str(sigma.round(7)))
        b=a
        counter1 += 1
    time.sleep(1.9)
    
while counter2 < counter_rate:
    print("achan1:")
    print("{:>5}\t{:>5.3f}".format(achan1.value, achan1.voltage))
    print("----------------------------------------------------")
    
    #creat an array with 10 diffrent voltages
    save = np.array([])
    timer = 0
    while timer < avarage:
       save = np.append(save,achan1.voltage)
       sigma_var = save-(np.sum(save)/avarage)
       sigma = np.sqrt(np.sum(np.square(sigma_var))/(avarage-1))
       time.sleep(0.01)
       timer += 1
    
    #take the average of the 10 values and print it in a .txt
    a = np.array([])
    a = np.append(a,round((np.sum(save)/avarage),3))
    print(a)
    if a!=b:
        datei.write("\n{:>5}\t{:>5.4f}".format(achan1.value,np.sum(save)/avarage) + "\t" + str(sigma.round(7)))
        b=a
        counter2 += 1
    
    time.sleep(1.9)

while counter3 < counter_rate:
    print("achan2:")
    print("{:>5}\t{:>5.3f}".format(achan2.value, achan2.voltage))
    print("----------------------------------------------------")
    
    #creat an array with 10 diffrent voltages
    save = np.array([])
    timer = 0
    while timer < avarage:
       save = np.append(save,achan2.voltage)
       sigma_var = save-(np.sum(save)/avarage)
       sigma = np.sqrt(np.sum(np.square(sigma_var))/avarage)
       time.sleep(0.01)
       timer += 1
    
    #take the average of the 10 values and print it in a .txt
    a = np.array([])
    a = np.append(a,round((np.sum(save)/avarage),3))
    print(a)
    if a!=b:
        datei.write("\n{:>5}\t{:>5.4f}".format(achan2.value,np.sum(save)/avarage) + "\t" + str(sigma.round(7)))
        b=a
        counter3 += 1
    
    time.sleep(1.9)
    
while counter4 < counter_rate:
    print("achan3:")
    print("{:>5}\t{:>5.3f}".format(achan3.value, achan3.voltage))
    print("----------------------------------------------------")
    
    #creat an array with 10 diffrent voltages
    save = np.array([])
    timer = 0
    while timer < avarage:
       save = np.append(save,achan3.voltage)
       sigma_var = save-(np.sum(save)/avarage)
       sigma = np.sqrt(np.sum(np.square(sigma_var))/avarage)
       time.sleep(0.01)
       timer += 1
    
    #take the average of the 10 values and print it in a .txt
    a = np.array([])
    a = np.append(a,round((np.sum(save)/avarage),3))
    print(a)
    if a!=b:
        datei.write("\n{:>5}\t{:>5.4f}".format(achan3.value,np.sum(save)/avarage) + "\t" + str(sigma.round(7)))
        b=a
        counter4 += 1
    
    time.sleep(1.9)

while counter5 < counter_rate:
    print("bchan0:")
    print("{:>5}\t{:>5.3f}".format(bchan0.value, bchan0.voltage))
    print("----------------------------------------------------")
    
    #creat an array with 10 diffrent voltages
    save = np.array([])
    timer = 0
    while timer < avarage:
       save = np.append(save,bchan0.voltage)
       sigma_var = save-(np.sum(save)/avarage)
       sigma = np.sqrt(np.sum(np.square(sigma_var))/avarage)
       time.sleep(0.01)
       timer += 1
    
    #take the average of the 10 values and print it in a .txt
    a = np.array([])
    a = np.append(a,round((np.sum(save)/avarage),3))
    print(a)
    if a!=b:
        datei.write("\n{:>5}\t{:>5.4f}".format(bchan0.value,np.sum(save)/avarage) + "\t" + str(sigma.round(7)))
        b=a
        counter5 += 1
    
    time.sleep(1.9)

while counter6 < counter_rate:
    print("bchan1:")
    print("{:>5}\t{:>5.3f}".format(bchan1.value, bchan1.voltage))
    print("----------------------------------------------------")
    
    #creat an array with 10 diffrent voltages
    save = np.array([])
    timer = 0
    while timer < avarage:
       save = np.append(save,bchan1.voltage)
       sigma_var = save-(np.sum(save)/avarage)
       sigma = np.sqrt(np.sum(np.square(sigma_var))/avarage)
       time.sleep(0.01)
       timer += 1
    
    #take the average of the 10 values and print it in a .txt
    a = np.array([])
    a = np.append(a,round((np.sum(save)/avarage),3))
    print(a)
    if a!=b:
        datei.write("\n{:>5}\t{:>5.4f}".format(bchan1.value,np.sum(save)/avarage) + "\t" + str(sigma.round(7)))
        b=a
        counter6 += 1
    
    time.sleep(1.9)

while counter7 < counter_rate:
    print("bchan2:")
    print("{:>5}\t{:>5.3f}".format(bchan2.value, bchan2.voltage))
    print("----------------------------------------------------")
    
    #creat an array with 10 diffrent voltages
    save = np.array([])
    timer = 0
    while timer < avarage:
       save = np.append(save,bchan2.voltage)
       sigma_var = save-(np.sum(save)/avarage)
       sigma = np.sqrt(np.sum(np.square(sigma_var))/avarage)
       time.sleep(0.01)
       timer += 1
    
    #take the average of the 10 values and print it in a .txt
    a = np.array([])
    a = np.append(a,round((np.sum(save)/avarage),3))
    print(a)
    if a!=b:
        datei.write("\n{:>5}\t{:>5.4f}".format(bchan2.value,np.sum(save)/avarage) + "\t" + str(sigma.round(7)))
        b=a
        counter7 += 1
    
    time.sleep(1.9)

while counter8 < counter_rate:
    print("bchan3:")
    print("{:>5}\t{:>5.3f}".format(bchan3.value, bchan3.voltage))
    print("----------------------------------------------------")
    
    #creat an array with 10 diffrent voltages
    save = np.array([])
    timer = 0
    while timer < avarage:
       save = np.append(save,bchan3.voltage)
       sigma_var = save-(np.sum(save)/avarage)
       sigma = np.sqrt(np.sum(np.square(sigma_var))/avarage)
       time.sleep(0.01)
       timer += 1
    
    #take the average of the 10 values and print it in a .txt
    a = np.array([])
    a = np.append(a,round((np.sum(save)/avarage),3))
    print(a)
    if a!=b:
        datei.write("\n{:>5}\t{:>5.4f}".format(bchan3.value,np.sum(save)/avarage) + "\t" + str(sigma.round(7)))
        b=a
        counter8 += 1
    
    time.sleep(1.9)

while counter9 < counter_rate:
    print("cchan0:")
    print("{:>5}\t{:>5.3f}".format(cchan0.value, cchan0.voltage))
    print("----------------------------------------------------")
    
    #creat an array with 10 diffrent voltages
    save = np.array([])
    timer = 0
    while timer < avarage:
       save = np.append(save,cchan0.voltage)
       sigma_var = save-(np.sum(save)/avarage)
       sigma = np.sqrt(np.sum(np.square(sigma_var))/avarage)
       time.sleep(0.01)
       timer += 1
    
    #take the average of the 10 values and print it in a .txt
    a = np.array([])
    a = np.append(a,round((np.sum(save)/avarage),3))
    print(a)
    if a!=b:
        datei.write("\n{:>5}\t{:>5.4f}".format(cchan0.value,np.sum(save)/avarage) + "\t" + str(sigma.round(7)))
        b=a
        counter9 += 1
    
    time.sleep(1.9)

while counter10 < counter_rate:
    print("cchan1:")
    print("{:>5}\t{:>5.3f}".format(cchan1.value, cchan1.voltage))
    print("----------------------------------------------------")
    
    #creat an array with 10 diffrent voltages
    save = np.array([])
    timer = 0
    while timer < avarage:
       save = np.append(save,cchan1.voltage)
       sigma_var = save-(np.sum(save)/avarage)
       sigma = np.sqrt(np.sum(np.square(sigma_var))/avarage)
       time.sleep(0.01)
       timer += 1
    
    #take the average of the 10 values and print it in a .txt
    a = np.array([])
    a = np.append(a,round((np.sum(save)/avarage),3))
    print(a)
    if a!=b:
        datei.write("\n{:>5}\t{:>5.4f}".format(cchan1.value,np.sum(save)/avarage) + "\t" + str(sigma.round(7)))
        b=a
        counter10 += 1
    
    time.sleep(1.9)
    
while counter11 < counter_rate:
    print("cchan2:")
    print("{:>5}\t{:>5.3f}".format(cchan2.value, cchan2.voltage))
    print("----------------------------------------------------")
    
    #creat an array with 10 diffrent voltages
    save = np.array([])
    timer = 0
    while timer < avarage:
       save = np.append(save,cchan2.voltage)
       sigma_var = save-(np.sum(save)/avarage)
       sigma = np.sqrt(np.sum(np.square(sigma_var))/avarage)
       time.sleep(0.01)
       timer += 1
    
    #take the average of the 10 values and print it in a .txt
    a = np.array([])
    a = np.append(a,round((np.sum(save)/avarage),3))
    print(a)
    if a!=b:
        datei.write("\n{:>5}\t{:>5.4f}".format(cchan2.value,np.sum(save)/avarage) + "\t" + str(sigma.round(7)))
        b=a
        counter11 += 1
    
    time.sleep(1.9)

while counter12 < counter_rate:
    print("cchan3:")
    print("{:>5}\t{:>5.3f}".format(cchan3.value, cchan3.voltage))
    print("----------------------------------------------------")
    
    #creat an array with 10 diffrent voltages
    save = np.array([])
    timer = 0
    while timer < avarage:
       save = np.append(save,cchan3.voltage)
       sigma_var = save-(np.sum(save)/avarage)
       sigma = np.sqrt(np.sum(np.square(sigma_var))/avarage)
       time.sleep(0.01)
       timer += 1
    
    #take the average of the 10 values and print it in a .txt
    a = np.array([])
    a = np.append(a,round((np.sum(save)/avarage),3))
    print(a)
    if a!=b:
        datei.write("\n{:>5}\t{:>5.4f}".format(cchan3.value,np.sum(save)/avarage) + "\t" + str(sigma.round(7)))
        b=a
        counter12 += 1
    
    time.sleep(1.9)


#---------------Curve-Fit---------------#
#define Function
##def func(x,m,n):
##   return x*m+n

#get data(every 15 pairs off data the channal changes to the next. So there are 15 pairs of achan0 data and than 15 of achan1 and so on)
##path_d = datei
##datafile = np.loadtxt(path_d, delimiter='	', unpack=True)
##a,b,db = 0,1,2
##A,B,dB = datafile[a],datafile[b],datafile[db]

#curve-fit-program
##popt,pcov = curve_fit(func,A,B)
##errors = np.sqrt(np.diag(pcov))
##print('Steigung: ' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5))+ '\n' + 'y-Achse: ' + str(popt[1].round(5)) + '+/-' + str(errors[1].round(5)))
##print('Nochmal komplett: y=' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5)) + '*x+' + str(popt[1].round(5))+ '+/-' + str(errors[1].round(5)))

#creat fit
##xlin = np.linspace(A[0],A[-1],100)
##ylin = func(xlin,popt[0],popt[1])

#creat axis and draw function
##ax = plt.figure(figuresize=(8,4.5),dpi=350).add_subplot(1,1,1)
##ax.set_facecolor('gainboro')
##plt.errorbar(A,B,yerr=dB, color='royalblue',fmt='+',label='Datenpunkte')
##plt.plot(xlin,ylin,color='firebrick', label='Fit-Gerade',lw=1.2)

##plt.xlabel('Kanal')
##plt.ylabel('Volt')
##plt.grid(True, which='minor',linestyle='--', color='darkgray', lw=0.5)
##plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
##plt.tight_layout()
##plt.show()





