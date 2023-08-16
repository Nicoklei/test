from termios import FF1
import numpy as np
import time
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtWidgets import(QApplication, QCheckBox, QComboBox, QDateEdit, QDateTimeEdit, QDial, QDoubleSpinBox, QFontComboBox, QLabel, QLCDNumber, QLineEdit, QMainWindow, QProgressBar, QPushButton, QRadioButton, QSlider, QSpinBox, QTimeEdit, QVBoxLayout,QHBoxLayout,QGridLayout,QStackedLayout, QWidget, QDialog, QDialogButtonBox)
from PyQt5.QtGui import QPalette, QColor
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import sys
from random import choice
import adc_main, adc_utils
from basil.dut import Dut


def start_kalibration():
			dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
			dut.init()
			d = dut["PowerSupply"]
			d.set_channel(1)	
			d.on()

			#---------------Curve-Fit---------------#
			#define Function
			def func(x,m,n):
				return x*m+n

			gain_a = 1

			gain_b = 1

			gain_c = 0
			
			data=[gain_a,gain_b,gain_c,1]
			gain_d = gain_b

			A = adc_main.main("-c", data)

			v_values = 201
			voltages_array=np.array([])


			datei = open("Kalibration_ADC1_%sV_ADC2_%sV_ADC3_%sV_ADC4_%sV_neu.txt"%(gain_a,gain_b,gain_c,gain_d),'w')

			for i in range(v_values):
					time.sleep(0.05)
					d.set_voltage(i/100)
					voltages_array=np.append(voltages_array,i/100)
					time.sleep(0.5)
					data = [0,0,0,1]
					A = adc_main.main("-c", data)
					datei.write(str(A[0][0]) + '\t'+ str(A[0][1]) + '\t'+ str(A[0][2]) + '\t'+ str(A[0][3]) + '\t' + str(A[1][0]) + '\t'+ str(A[1][1]) + '\t'+ str(A[1][2]) + '\t'+ str(A[1][3]) +  '\t' + str(A[2][0]) + '\t'+ str(A[2][1]) + '\t'+ str(A[2][2]) + '\t'+ str(A[2][3]) + '\t' + str(A[3][0]) + '\t'+ str(A[3][1]) + '\t'+ str(A[3][2]) + '\t'+ str(A[3][3]) + '\t' + str(A[4][0]) + '\t' + str(A[4][1]) + '\t'+ str(A[4][2]) + '\t'+ str(A[4][3]) + '\t' + str(A[5][0]) + '\t'+ str(A[5][1]) + '\t'+ str(A[5][2]) + '\t'+ str(A[5][3]) + '\t' + str(A[6][0]) + '\t'+ str(A[6][1]) + '\t'+ str(A[6][2]) + '\t'+ str(A[6][3]) + '\t' + str(A[7][0]) + '\t'+ str(A[7][1]) + '\t'+ str(A[7][2]) + '\t'+ str(A[7][3]) + '\n')#+ str(A[6][0]) + '\t'+ str(A[6][1]) + '\t'+ str(A[6][2]) + '\t'+ str(A[6][3]) + '\t' + str(A[7][0]) + '\t'+ str(A[7][1]) + '\t'+ str(A[7][2]) + '\t'+ str(A[7][3]) + '\t' + str(A[8][0]) + '\t'+ str(A[8][1]) + '\t'+ str(A[8][2]) + '\t'+ str(A[8][3]) + '\t' + str(A[9][0]) + '\t'+ str(A[9][1]) + '\t'+ str(A[9][2]) + '\t'+ str(A[9][3]) + '\n')
					time.sleep(0.05)
					print(i,v_values)
			datei.close()

			datafile = np.loadtxt("Kalibration_ADC1_%sV_ADC2_%sV_ADC3_%sV_ADC4_%sV_neu.txt"%(gain_a,gain_b,gain_c,gain_d), delimiter='\t', unpack=True)

			run_new = 0

			for name in [1,2,3,4]:
				
				run = 0
				while run<2:

					A = datafile[(run+run_new*2)*4]
					B = datafile[2+(run+run_new*2)*4]
					dA = datafile[1+(run+run_new*2)*4]
					dB = datafile[3+(run+run_new*2)*4]	
	
					x = np.array([])
					for i in range(0,v_values+1):
						x = np.append(x,i)


					#curve-fit-program
					popt,pcov = curve_fit(func,voltages_array,B)
					errors = np.sqrt(np.diag(pcov))
					#print('Steigung: ' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5))+ '\t' + 'y-Achse: ' + str(popt[1].round(5)) + '+/-' + str(errors[1].round(5)))
					#print('Nochmal komplett: y=' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5)) + '*x+' + str(popt[1].round(5))+ '+/-' + str(errors[1].round(5)) + '\n')
					#datei.write(str(popt[0].round(5)) + '\t' + str(errors[0].round(5))+ '\t' + str(popt[1].round(5)) + '\t' + str(errors[1].round(5)) + '\n')

					#creat fit
					xlin = np.linspace(min(voltages_array), max(voltages_array),1000)
					ylin = func(xlin,popt[0],popt[1])

					#creat axis and draw function
					ax = plt.figure(dpi=350).add_subplot(1,1,1)

					plt.errorbar(voltages_array,B,xerr=0.001,yerr=dB, color='royalblue',fmt='+',label='m = %s +/- %s \nn = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5))))
					plt.plot(xlin,ylin,color='firebrick', label='Fit-Gerade',lw=1.2)
	
					plt.xlabel('Volt Power Supply/V')
					plt.ylabel('ADC Values')
					plt.grid(True, which='minor',linestyle='--', color='darkgray', lw=0.5)
					plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
					plt.legend(loc='best')	
					plt.tight_layout()
					#plt.savefig('./Bilder%.3f/ADC%dchannal%d'%(name,run_new+1,run+1))
					print(run,run_new,name)
					if run==0:
						plt.savefig('./Neue_Kali/ADC%schannal%d_gegen_channal%d_neu'%(name,run_new+1,run+1))
					else:
						plt.savefig('./Neue_Kali/ADC%schannal%d_gegen_channal%d_neu'%(name,run_new+1,run+2))
					run += 1
				run_new += 1
			d.off()
			

gain_a = 2

gain_b = 2

gain_c = 1
			
data=[gain_a,gain_b,gain_c,0]
gain_d = gain_b

A = adc_main.main("-c", data)

start_kalibration()
