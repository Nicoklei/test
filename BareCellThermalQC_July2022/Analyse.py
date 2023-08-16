#Analyse
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



datafile = np.loadtxt("Kalibration_ADC1_%sV_ADC2_%sV_ADC3_%sV_ADC4_%sV_neu.txt"%(1,1,1,1), delimiter='\t', unpack=True)
A,B,C,D = datafile[2],datafile[10],datafile[18],datafile[26]


all_jumps = np.array([])
all_jumps1 = np.array([])
all_jumps2 = np.array([])
all_jumps3 = np.array([])

for i in range(9):
    jump = A[i+1]-A[i]
    all_jumps = np.append(all_jumps,jump)
    jump1 = B[i+1]-B[i]
    all_jumps1 = np.append(all_jumps1,jump1)
    jump2 = C[i+1]-C[i]
    all_jumps2 = np.append(all_jumps2,jump2)
    jump3 = D[i+1]-D[i]
    all_jumps3 = np.append(all_jumps3,jump3)

plt.hist(all_jumps,35)
plt.savefig('./Neue_Kali/Jumps/ADC1_ADC_count_jumps')
plt.show()
plt.hist(all_jumps1,35)
plt.savefig('./Neue_Kali/Jumps/ADC2_ADC_count_jumps')
plt.show()
plt.hist(all_jumps2,35)
plt.savefig('./Neue_Kali/Jumps/ADC3_ADC_count_jumps')
plt.show()
plt.hist(all_jumps3,35)
plt.savefig('./Neue_Kali/Jumps/ADC4_ADC_count_jumps')


