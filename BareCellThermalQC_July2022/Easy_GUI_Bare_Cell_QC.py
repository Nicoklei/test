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
from PyQt5.QtCore import pyqtSlot,QRunnable,QThreadPool, QObject, pyqtSignal
import os
import shutil
import threading


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)

class Worker(QRunnable):
	'''
	Worker thread
	'''
	def __init__(self, fn, *args, **kwargs):
		super(Worker, self).__init__()
		# Store constructor arguments (re-used for processing)
		self.fn = fn
		self.args = args
		self.kwargs = kwargs
		self.signals = WorkerSignals()

	@pyqtSlot()
	def run(self):
		'''
		1.5 second pause
		'''
		#print("Thread start")
		time.sleep(1.5)
		#print("Thread complete")
		self.signals.finished.emit()



class MainWindow(QMainWindow):

	def __init__(self):
		super().__init__()

		self.setWindowTitle("Datenauslese")
		
		#----------Layouts----------#
		layout = QGridLayout()

		layout00 = QVBoxLayout()
		layout001 = QHBoxLayout()
		layout002 = QHBoxLayout()
		layout003 = QHBoxLayout()
		layout004 = QHBoxLayout()
		layout005 = QHBoxLayout()
		layout006 = QHBoxLayout()
		layout007 = QHBoxLayout()
		layout008 = QHBoxLayout()
		layout009 = QHBoxLayout()
		layout0010 = QHBoxLayout()
		layout0011 = QHBoxLayout()
		layout0012 = QHBoxLayout()

		layout10 = QVBoxLayout()
		layout101 = QHBoxLayout()
		layout102 = QHBoxLayout()
		layout103 = QHBoxLayout()
		layout104 = QHBoxLayout()
		layout105 = QHBoxLayout()
		layout106 = QHBoxLayout()
		layout107 = QHBoxLayout()
		layout108 = QHBoxLayout()
		layout109 = QHBoxLayout()
		layout1010 = QHBoxLayout()
		layout1011 = QHBoxLayout()
		layout1012 = QHBoxLayout()
		layout1013 = QHBoxLayout()
		layout1014 = QHBoxLayout()
		layout1015 = QHBoxLayout()
		layout1016 = QHBoxLayout()


		layout01 = QVBoxLayout()

		layout11 = QVBoxLayout()

		#Variables
		global gain_a
		gain_a=2
		global gain_b
		gain_b=2
		global gain_c
		gain_c=1
		global voltage_1
		voltage_1=0
		global voltage_2
		voltage_2=0
		global current_1
		current_1=2
		global current_2
		current_2=2
		global thick
		thick = 0.0074+0.0018
		global serial_number
		global measurment_run
		measurment_run = 0
		global values_graph1
		values_graph1=np.array([])
		global values_graph2
		values_graph2=np.array([])
		global values_graph3
		values_graph3=np.array([])
		global values_graph4
		values_graph4=np.array([])
		global x_values_graph
		x_values_graph = np.array([])
		global x_values_graph_messung
		x_values_graph_messung = np.array([])
		global values_graph_messung1
		values_graph_messung1 = np.array([])
		global values_graph_messung2
		values_graph_messung2 = np.array([])
		global values_graph_messung3
		values_graph_messung3 = np.array([])
		global values_graph_messung4
		values_graph_messung4 = np.array([])
		global measurment_run_extra
		measurment_run_extra = 0
		global TFM_test_21
		TFM_test_21 = 0.00
		
		##without hardware comment out##
		data = [2,2,1,0]
		A = adc_main.main("-c", data)

		global v_values
		v_values=np.array([])

		#--------------add Widgets--------------#
		####sector00####

		## Changing Labels
		self.widgetl00L1 = QLabel("Starte Peltier-Element")
		self.widgetl00L2 = QLabel("Starte Heizspirale")
		self.widgetl00L3 = QLabel("Jetzige Spannung: 0.000")
		self.widgetl00L4 = QLabel("Jetzige Spannung: 0.000")
		self.widgetl00L5 = QLabel("Pc und Pi \nsind verbunden")
		self.widgetl00L6 = QLabel("Knopf drücken um Range zu ändern.\nAnsonsten wird die vorherige oder \ndie Standart Range verwendet")
		self.widgetl00L7 = QLabel()
		self.widgetl00L8 = QLabel("Jetziger Strom: 0.000")
		self.widgetl00L9 = QLabel("Jetziger Strom: s0.000")

		## Not changing Labels
		widgetl00L1 = QLabel("Bare Cell QC Setup Auslesesystem")
		widgetl00L2 = QLabel("Range ADC1 (Temperaturmessung oben):")
		widgetl00L3 = QLabel("Range ADC2 (Temperaturmessung unten):")
		widgetl00L4 = QLabel("Range ADC3:")
		widgetl00L5 = QLabel("Anzahl der \nMessungen")
		widgetl00L6 = QLabel("Dicke des Materials \nzwischen Aluminium Stäben:")
		widgetl00L7 = QLabel("Name Testobjekt:")
		widgetl00L8 = QLabel("Peltier-Element Steuerung")
		widgetl00L9 = QLabel("Heizspirale Steuerung")
		widgetl00L10 = QLabel("Einstellungen zur Messung eines DUT")
		widgetl00L11 = QLabel("Messungen")	
		widgetl00L12 = QLabel("Vergleichstest 21 starten \noder Vergleichswert eingeben:")		

		## Buttons
		self.widgetPB2 = QPushButton("Messung Starten")
		self.widgetPB3 = QPushButton("Verbindung Testen")
		self.widgetPB4 = QPushButton("Range setzen")
		self.widgetPB6 = QPushButton("Spannung setzen")
		self.widgetPB7 = QPushButton("Spannung setzen")
		self.widgetPB8 = QPushButton("Strom setzen")
		self.widgetPB9 = QPushButton("Strom setzen")
		self.widgetPB10 = QPushButton("Messreihe weiterführen und gleichen Ordner weiterverwenden")
		self.widgetPB11 = QPushButton("Graph Leeren")
		self.widgetPB12 = QPushButton("Programm starten")
		self.widgetPB13 = QPushButton("Vergleichstest 21 starten")

		## Other functions
		widget00SB1 = QSpinBox()
		widget00SB2 = QSpinBox()
		widgetS1 = QSlider()	

		widget00CB1 = QComboBox()
		widget00CB2 = QComboBox()
		widget00CB3 = QComboBox()

		widget00SB3 = QSpinBox()

		widget00DSB1 = QDoubleSpinBox()
		widget00DSB2 = QDoubleSpinBox()
		widget00DSB3 = QDoubleSpinBox()
		self.widget00DSB4 = QDoubleSpinBox()

		widget00ChB1 = QCheckBox()
		widget00ChB2 = QCheckBox()

		widget00LE1 = QLineEdit()
			

		####sector10####

		## Changing Labels
		self.widgetl10L1 = QLabel()
		self.widgetl10L2 = QLabel()
		self.widgetl10L3 = QLabel()
		self.widgetl10L4 = QLabel()
		self.widgetl10L5 = QLabel()
		self.widgetl10L6 = QLabel()
		self.widgetl10L7 = QLabel()
		self.widgetl10L8 = QLabel()
		self.widgetl10L9 = QLabel()
		self.widgetl10L10 = QLabel()
		self.widgetl10L11 = QLabel()
		self.widgetl10L12 = QLabel()
		self.widgetl10L13 = QLabel()
		self.widgetl10L14 = QLabel()
		self.widgetl10L15 = QLabel()
		self.widgetl10L16 = QLabel()

		## Not changing Labels
		widgetl10L1 = QLabel("Temperatursensor oben / °C:")
		widgetl10L2 = QLabel("Temperatursensor mitte oben / °C:")
		widgetl10L3 = QLabel("Temperatursensor mitte unten / °C:")
		widgetl10L4 = QLabel("Temperatursensor unten / °C:")
		widgetl10L5 = QLabel("Gewicht auf Device / kg:")
		widgetl10L6 = QLabel("Spannung Temperatursensoren:")
		widgetl10L7 = QLabel("Lambda oben:")
		widgetl10L8 = QLabel("Lambda mitte:")
		widgetl10L9 = QLabel("Lambda unten:")
		widgetl10L15 = QLabel("Wärmewiderstand oben:")
		widgetl10L16 = QLabel("Wärmewiderstand mitte:")
		widgetl10L17 = QLabel("Wärmewiderstand unten:")
		widgetl10L18 = QLabel("Wärmewiderstand DUT:")
		widgetl10L10 = QLabel("Vorheriges Ergebnis Lambda oben:")
		widgetl10L11 = QLabel("Vorheriges Ergebnis Lambda mitte:")
		widgetl10L12 = QLabel("Vorheriges Ergebnis Lambda unten:")
		widgetl10L13 = QLabel("Messwerte")

		####sector01####

		## Functions to plot the graph
		self.widget01G = pg.PlotWidget()
		self.widget01G.setBackground('w')
		self.widget01G.addLegend()
		self.widget01G.showGrid(x=True, y=True)

		####sector11####

		self.widgetl11L17 = QLabel()
				
		#-------add functions to Widgets-------# 
		####sector00####
		widgetS1.valueChanged.connect(self.value_change)

		font6 = widgetl00L8.font()
		font6.setPointSize(11)
		font10 = widgetl00L1.font()
		font10.setPointSize(15)
		widgetl00L1.setFont(font10)
		widgetl00L8.setFont(font6)
		widgetl00L9.setFont(font6)
		widgetl00L10.setFont(font6)
		widgetl00L11.setFont(font6)
		widgetl10L5.setFont(font6)
		self.widgetl10L5.setFont(font6)
  
		font11 = self.widgetl00L7.font()
		font11.setPointSize(12)
		self.widgetl00L7.setFont(font11)

		##without hardware comment out##
		dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
		dut.init()
		d = dut["PowerSupply"]
		d.set_channel(1)
		time.sleep(0.05)
		vol = d.get_target_voltage()

		widget00SB1.setSuffix("mV")
		widget00SB1.setMinimum(0)
		widget00SB1.setMaximum(32000)
		widget00SB1.setValue(int(float(vol)*1000))
		widget00SB1.valueChanged.connect(self.start_peltier)
		
		##without hardware comment out##
		d.set_channel(2)
		time.sleep(0.05)
		vol = d.get_target_voltage()

		widget00SB2.setSuffix("mV")
		widget00SB2.setMinimum(0)
		widget00SB2.setMaximum(32000)
		widget00SB2.setValue(int(float(vol)*1000))
		widget00SB2.valueChanged.connect(self.start_spirale)

		self.widgetPB2.clicked.connect(self.start_messurment)
		self.widgetPB3.clicked.connect(self.test_connection)
		self.widgetPB4.clicked.connect(self.set_data)
		self.widgetPB6.clicked.connect(self.set_voltage1)
		self.widgetPB7.clicked.connect(self.set_voltage2)
		self.widgetPB8.clicked.connect(self.set_current1)
		self.widgetPB9.clicked.connect(self.set_current2)
		self.widgetPB10.clicked.connect(self.new_messurment_series)
		self.widgetPB11.clicked.connect(self.clear_graph)
		self.widgetPB12.clicked.connect(self.oh_no)
		self.widgetPB13.clicked.connect(self.TFM_test_21_func)

		widget00CB1.NoInsert
		widget00CB1.addItems(["2,048V", "4,096V", "1,024V", "0,512V", "0,256V"])
		widget00CB1.currentIndexChanged.connect(self.index_changed_a)
		widget00CB2.NoInsert
		widget00CB2.addItems(["2,048V", "4,096V", "1,024V", "0,512V", "0,256V"])
		widget00CB2.currentIndexChanged.connect(self.index_changed_b)
		widget00CB3.NoInsert
		widget00CB3.addItems(["4,096V", "2,048V", "1,024V", "0,512V", "0,256V"])
		widget00CB3.currentIndexChanged.connect(self.index_changed_c)

		widget00SB3.setMinimum(0)
		widget00SB3.setMaximum(500)
		widget00SB3.valueChanged.connect(self.messurment_frequency)
		widget00SB3.setValue(100)

		widget00DSB1.setMinimum(0.000)
		widget00DSB1.setMaximum(15)
		widget00DSB1.valueChanged.connect(self.strom_peltier)
		widget00DSB1.setValue(6)
		widget00DSB1.setSuffix("A")
		widget00DSB2.setMinimum(0.000)
		widget00DSB2.setMaximum(3)
		widget00DSB2.valueChanged.connect(self.strom_heater)
		widget00DSB2.setValue(3)
		widget00DSB2.setSuffix("A")
		widget00DSB3.valueChanged.connect(self.thickness)
		widget00DSB3.setValue(1.80)
		widget00DSB3.setSuffix("mm")
		self.widget00DSB4.setMinimum(0.00)
		self.widget00DSB4.setMaximum(4.00)
		self.widget00DSB4.valueChanged.connect(self.TFM_comparison)
		self.widget00DSB4.setSuffix("cm²K/W")

		widget00ChB1.stateChanged.connect(self.on_off_peltier)
		widget00ChB2.stateChanged.connect(self.on_off_spirale)

		widget00LE1.textEdited.connect(self.text_edited)

		####sector10####
		font2 = widgetl10L13.font()
		font2.setPointSize(11)
		widgetl10L13.setFont(font2)


		####sector01####

		####sector11####
		font7 = self.widgetl11L17.font()
		font7.setPointSize(18)
		self.widgetl11L17.setFont(font7)


		#---------add Widgets into Layouts---------#
		#sector00
		layout00.addWidget(widgetl00L1)

		#layout003.addWidget(self.widgetl00L5)
		#layout003.addWidget(self.widgetPB3)
		#layout00.addLayout(layout003)

		layout00.addWidget(self.widgetPB12)
  
		layout00.addWidget(widgetl00L8)
		widgetl00L8.setContentsMargins(0,12,0,0)
		layout006.addWidget(self.widgetl00L1)
		layout006.addWidget(widget00ChB1)
		layout00.addLayout(layout006)

		#layout001.addWidget(widget00SB1)
		#layout001.addWidget(self.widgetPB6)
		layout00.addWidget(self.widgetl00L3)
		#layout00.addLayout(layout001)

		#layout008.addWidget(widget00DSB1)
		#layout008.addWidget(self.widgetPB8)
		layout00.addWidget(self.widgetl00L8)
		#layout00.addLayout(layout008)

		layout00.addWidget(widgetl00L9)
		widgetl00L9.setContentsMargins(0,12,0,0)
		layout007.addWidget(self.widgetl00L2)
		layout007.addWidget(widget00ChB2)
		layout00.addLayout(layout007)

		#layout002.addWidget(widget00SB2)
		#layout002.addWidget(self.widgetPB7)
		layout00.addWidget(self.widgetl00L4)
		#layout00.addLayout(layout002)

		#layout009.addWidget(widget00DSB2)
		#layout009.addWidget(self.widgetPB9)
		layout00.addWidget(self.widgetl00L9)
		#layout00.addLayout(layout009)

		layout00.addWidget(widgetl00L10)
		widgetl00L10.setContentsMargins(0,12,0,0)
		layout0010.addWidget(widgetl00L6)
		layout0010.addWidget(widget00DSB3)
		layout00.addLayout(layout0010)

		layout0011.addWidget(widgetl00L7)
		layout0011.addWidget(widget00LE1)
		layout00.addLayout(layout0011)

		#layout005.addWidget(widgetl00L5)
		#layout005.addWidget(widget00SB3)
		#layout00.addLayout(layout005)
		
		layout00.addWidget(self.widgetPB10)
		layout00.addWidget(self.widgetPB11)

		layout00.addWidget(widgetl00L11)
		widgetl00L11.setContentsMargins(0,12,0,0)

		#layout00.addWidget(widgetl00L2)
		#layout00.addWidget(widget00CB1)
		#layout00.addWidget(widgetl00L3)
		#layout00.addWidget(widget00CB2)
		#layout00.addWidget(widgetl00L4)
		#layout00.addWidget(widget00CB3)

		#layout004.addWidget(self.widgetl00L6)
		#layout004.addWidget(self.widgetPB4)
		#layout00.addLayout(layout004)

		layout0012.addWidget(widgetl00L12)
		layout0012.addWidget(self.widgetPB13)
		layout0012.addWidget(self.widget00DSB4)
		layout00.addLayout(layout0012)

		layout00.addWidget(self.widgetPB2)
		layout00.addWidget(self.widgetl00L7)

	
		#sector10
		layout00.addWidget(widgetl10L13)

		#layout101.addWidget(widgetl10L1)
		#layout101.addWidget(self.widgetl10L1)
		#layout10.addLayout(layout101)

		#layout102.addWidget(widgetl10L2)
		#layout102.addWidget(self.widgetl10L2)
		#layout10.addLayout(layout102)

		#layout103.addWidget(widgetl10L3)
		#layout103.addWidget(self.widgetl10L3)
		#layout10.addLayout(layout103)

		#layout104.addWidget(widgetl10L4)
		#layout104.addWidget(self.widgetl10L4)
		#layout10.addLayout(layout104)

		layout105.addWidget(widgetl10L5)
		layout105.addWidget(self.widgetl10L5)
		layout00.addLayout(layout105)

		#layout106.addWidget(widgetl10L6)
		#layout106.addWidget(self.widgetl10L6)
		#layout10.addLayout(layout106)

		#layout107.addWidget(widgetl10L7)
		#layout107.addWidget(self.widgetl10L7)
		#layout10.addLayout(layout107)

		#layout108.addWidget(widgetl10L8)
		#layout108.addWidget(self.widgetl10L8)
		#layout10.addLayout(layout108)

		#layout109.addWidget(widgetl10L9)
		#layout109.addWidget(self.widgetl10L9)
		#layout10.addLayout(layout109)

		# layout1010.addWidget(widgetl10L10)
		# layout1010.addWidget(self.widgetl10L10)
		# layout10.addLayout(layout1010)

		# layout1011.addWidget(widgetl10L11)
		# layout1011.addWidget(self.widgetl10L11)
		# layout10.addLayout(layout1011)

		# layout1012.addWidget(widgetl10L12)
		# layout1012.addWidget(self.widgetl10L12)
		# layout10.addLayout(layout1012)

		# layout1013.addWidget(widgetl10L15)
		# layout1013.addWidget(self.widgetl10L13)
		# layout10.addLayout(layout1013)

		# layout1014.addWidget(widgetl10L16)
		# layout1014.addWidget(self.widgetl10L14)
		# layout10.addLayout(layout1014)

		# layout1015.addWidget(widgetl10L17)
		# layout1015.addWidget(self.widgetl10L15)
		# layout10.addLayout(layout1015)

		#layout1016.addWidget(widgetl10L18)
		#layout1016.addWidget(self.widgetl10L16)
		#layout00.addLayout(layout1016)


		#sector01
		layout01.addWidget(self.widget01G)

		#sector11
		layout00.addWidget(self.widgetl11L17)

		#----------add Layouts into Grid----------#
	
		layout.addLayout(layout00, 0, 0)
		layout.addLayout(layout10, 1, 0)
		layout.addLayout(layout01, 0, 1)
		layout.addLayout(layout11, 1, 1)

		layout00.setContentsMargins(0,0,0,0)
		layout10.setContentsMargins(0,0,0,0)
		layout01.setContentsMargins(0,0,0,0)
		#layout11.setContentsMargins(0,0,0,0)
		layout.setContentsMargins(5,5,5,5)
		layout.setSpacing(2)

		widget = QWidget()
		widget.setLayout(layout)
		self.setMinimumSize(1200,1050)
		self.setCentralWidget(widget)

		#----------Timer----------#
		##without hardware comment out##
		#self.timer = QTimer()
		#self.timer.start(1)
		#self.timer.timeout.connect(self.update_spirale_peltier)
		
		self.threadpool = QThreadPool()
		
		



	def TFM_comparison(self,i):
		global TFM_test_21
		TFM_test_21 = i


	def oh_no(self):
		#zeitanfang = time.time()
		worker = Worker(self.oh_no)
		self.threadpool.start(worker)
		#print("start")
		worker.signals.finished.connect(self.update_spirale_peltier)
		worker.signals.finished.connect(self.oh_no)
		#zeitende = time.time()
		#print(zeitende-zeitanfang)


	def clear_graph(self):
		self.widget01G.clear()
		global values_graph1
		values_graph1=np.array([])
		global values_graph2
		values_graph2=np.array([])
		global values_graph3
		values_graph3=np.array([])
		global values_graph4
		values_graph4=np.array([])

		global x_values_graph
		x_values_graph = np.array([])


	def new_messurment_series(self):
		global measurment_run_extra
		global measurment_run
		measurment_run = measurment_run_extra
		self.widgetl00L7.setText("Messung kann gestartet werden")
		#try:
		#	shutil.copy('Vorordner/Vollständige_Temp_Kurve_.txt', 'Vorordner/%s/Vollständige_Temp_Kurve_.txt'%(serial_number))
		#	os.remove('Vorordner/Vollständige_Temp_Kurve_.txt')
		#except:
		#	self.widgetl00L7.setText("Datei konnte nicht verschoben werden")

	def text_edited(self,s):
		global serial_number
		serial_number = s

	def thickness(self,i):
		global thick
		thick=0.0074+i/1000

	def set_current1(self):
		dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
		dut.init()
		d = dut["PowerSupply"]
		d.set_channel(1)
		time.sleep(0.05)
		d.set_current(current_1)
		time.sleep(0.1)

	def set_current2(self):
		dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
		dut.init()
		d = dut["PowerSupply"]
		d.set_channel(2)
		time.sleep(0.05)
		d.set_current(current_2)
		time.sleep(0.1)

	def set_voltage1(self):
		dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
		dut.init()
		d = dut["PowerSupply"]
		d.set_channel(1)
		time.sleep(0.05)
		d.set_voltage(voltage_1/1000)
		time.sleep(0.1)

	def set_voltage2(self):
		dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
		dut.init()
		d = dut["PowerSupply"]
		d.set_channel(2)
		time.sleep(0.05)
		d.set_voltage(voltage_2/1000)
		time.sleep(0.1)


	def update_spirale_peltier(self):
		zeitanfang = time.time()
		dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
		dut.init()
		d = dut["PowerSupply"]
		d.set_channel(1)
		time.sleep(0.05)
		vol = d.get_voltage()
		time.sleep(0.05)
		cur = d.get_current()
		self.widgetl00L3.setText("Jetzige Spannung: " + str(vol))
		self.widgetl00L8.setText("Jetziger Strom: " + str(cur))
		time.sleep(0.05)
		d.set_channel(2)
		time.sleep(0.05)
		vol = d.get_voltage()
		time.sleep(0.05)
		cur = d.get_current()
		self.widgetl00L4.setText("Jetzige Spannung: " + str(vol))
		self.widgetl00L9.setText("Jetziger Strom: " + str(cur))
		data = [1,1,1,1]
		A = adc_main.main("-c", data)

		#name1 = 'Vorordner/Rohdaten.txt'
		#datei1 = open(name1,'a')
		#datei1.write(str(A) + '\n')
		#datei1.close()

		f1=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*(-5.775*10**(-7))*((100*(A[0][0]/(A[5][0]-A[0][0])))-100))))*np.sqrt((A[0][0]/(A[5][0]-A[0][0]))**2*0.00324**2+((100*(A[0][0]/(A[5][0]-A[0][0])**2))**2*(A[5][1])**2)+((100*(A[5][0]/(A[0][0]-A[5][0])**2)))**2*(A[0][1])**2)+0.05
		f2=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*-5.775*10**(-7)*((100*(A[1][0]/(A[5][0]-A[1][0])))-100))))*np.sqrt((A[1][0]/(A[5][0]-A[1][0]))**2*0.00324**2+((100*(A[1][0]/(A[5][0]-A[1][0])**2))**2*(A[5][1])**2)+((100*(A[5][0]/(A[1][0]-A[5][0])**2)))**2*(A[1][1])**2)+0.05
		f3=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*-5.775*10**(-7)*((100*(A[2][0]/(A[5][0]-A[2][0])))-100))))*np.sqrt((A[2][0]/(A[5][0]-A[2][0]))**2*0.00324**2+((100*(A[2][0]/(A[5][0]-A[2][0])**2))**2*(A[5][1])**2)+((100*(A[5][0]/(A[2][0]-A[5][0])**2)))**2*(A[2][1])**2)+0.05
		f4=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*-5.775*10**(-7)*((100*(A[3][0]/(A[5][0]-A[3][0])))-100))))*np.sqrt((A[3][0]/(A[5][0]-A[3][0]))**2*0.00324**2+((100*(A[3][0]/(A[5][0]-A[3][0])**2))**2*(A[5][1])**2)+((100*(A[5][0]/(A[3][0]-A[5][0])**2)))**2*(A[3][1])**2)+0.05
	
		T1=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(100*(A[0][0]/(A[5][0]-A[0][0]))))))/(2*(-5.775*10**(-7)*100)))
		T2=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(100*(A[1][0]/(A[5][0]-A[1][0]))))))/(2*(-5.775*10**(-7)*100)))
		T3=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(99.62*(A[2][0]/(A[5][0]-A[2][0]))))))/(2*(-5.775*10**(-7)*100)))
		T4=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(99.95*(A[3][0]/(A[5][0]-A[3][0]))))))/(2*(-5.775*10**(-7)*100)))


		self.widget01G.clear()
		global values_graph1
		values_graph1 = np.append(values_graph1,(T1))
		global values_graph2
		values_graph2 = np.append(values_graph2,(T2))
		global values_graph3
		values_graph3 = np.append(values_graph3,(T3))
		global values_graph4
		values_graph4 = np.append(values_graph4,(T4))

		if (-0.05 < (np.mean(values_graph1[-24:-15])-np.mean(values_graph1[-8:-1])) < 0.05) and (-0.05 < (np.mean(values_graph2[-24:-15])-np.mean(values_graph2[-8:-1])) < 0.05) and (-0.05 < (np.mean(values_graph3[-24:-15])-np.mean(values_graph3[-8:-1])) < 0.05) and (-0.05 < (np.mean(values_graph4[-24:-15])-np.mean(values_graph4[-8:-1])) < 0.05):
			self.widgetl00L7.setText("Temperatur Equilibrium vorhanden")
		else:
			self.widgetl00L7.setText("Messung sollte nicht gestartet werden. Equilibrium nicht vorhanden")

		global x_values_graph
		x_values_graph = np.append(x_values_graph,len(values_graph1))

		self.widget01G.setTitle("Temperatur Verlauf", color='b')
		self.widget01G.setLabel('left','Temperatur (°C)', color='b')
		self.widget01G.setLabel('bottom', 'Datenpunkte / 5s', color='b')
		self.widget01G.plot(x_values_graph,values_graph1, pen=(0,0,0), name ='Sensor oben')
		self.widget01G.plot(x_values_graph,values_graph2, pen='b', name ='Sensor mitte oben')
		self.widget01G.plot(x_values_graph,values_graph3, pen='g', name ='Sensor mitte unten')
		self.widget01G.plot(x_values_graph,values_graph4, pen='r', name ='Sensor unten')
		
		if T1 >= 60:
			d.set_channel(1)
			time.sleep(0.05)
			d.off()
			time.sleep(0.05)
			d.set_channel(2)
			time.sleep(0.05)
			d.off()
		if T4 >= 30:
			d.set_channel(1)
			time.sleep(0.05)
			d.off()
			time.sleep(0.05)
			d.set_channel(2)
			time.sleep(0.05)
			d.off()

		#zeitende = time.time()
		#print(zeitende-zeitanfang)

		self.widgetl10L5.setText(str(round(((A[4][0]*1000-1.55639)/2.31754),2))+'\t'+str(round((np.sqrt((1/2.31754)**2*(A[4][1]*1000)**2+(A[4][0]*1000/2.31754**2)**2*0.01692**2+(1/2.31754)**2*0.4216**2)),2)))

		name = 'Produktion/Vollständige_Temp_Kurve_.txt'
		datei = open(name,'a')


		datei.write(str(round(T1,6))+'\t'+str(round(f1,6))
		+'\t'+str(round(T2,6))+'\t'+str(round(f2,6))
		+'\t'+str(round(T3,6))+'\t'+str(round(f3,6))
		+'\t'+str(round(T4,6))+'\t'+str(round(f4,6))
		+'\t'+str(round(((A[4][0]*1000-1.55639)/2.31754),4))+'\t'+str(round((np.sqrt((1/2.31754)**2*(A[4][1]*1000)**2+(A[4][0]*1000/2.31754**2)**2*0.01692**2+(1/2.31754)**2*0.4216**2)),4))
		+'\t'+str((float(cur)*float(vol))/(T1-T2)*0.05/(0.0001*np.pi))+'\t'+str((np.sqrt(((float(cur)*float(vol))/(T1-T2)**2*0.05/(0.0001*np.pi))**2*(f1**2+f2**2))))
		+'\t'+str((float(cur)*float(vol))/(T2-T3)*thick/(0.0001*np.pi))+'\t'+str((np.sqrt(((float(cur)*float(vol))/(T2-T3)**2*thick/(0.0001*np.pi))**2*(f2**2+f3**2))))
		+'\t'+str((float(cur)*float(vol))/(T3-T4)*0.05/(0.0001*np.pi))+'\t'+str((np.sqrt(((float(cur)*float(vol))/(T3-T4)**2*0.05/(0.0001*np.pi))**2*(f3**2+f4**2))))
		+'\t'+str(float(cur)*float(vol))
		+'\n')

		datei.close()
		#zeitende = time.time()
		#print(zeitende-zeitanfang)


	def value_change(self, i):
		self.widgetl10L1.setText(str(i))

	def start_peltier(self, i):
		global voltage_1
		voltage_1 = i

	def strom_peltier(self, i):
		global current_1
		current_1 = i

	def strom_heater(self, i):
		global current_2
		current_2 = i

	def on_off_peltier(self, i):
		if i == 0:
			self.widgetl00L1.setText("Peltier-Element aus")
			dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
			dut.init()
			d = dut["PowerSupply"]
			d.set_channel(1)
			time.sleep(0.1)
			d.off()
		elif i == 2:
			self.widgetl00L1.setText("Peltier-Element an")
			dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
			dut.init()
			d = dut["PowerSupply"]
			d.set_channel(1)
			time.sleep(0.1)
			d.on()

	def start_spirale(self, i):
		global voltage_2
		voltage_2 = i

	def on_off_spirale(self, i):
		if i == 0:
			self.widgetl00L2.setText("Heizspirale aus")
			dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
			dut.init()
			d = dut["PowerSupply"]
			d.set_channel(2)
			time.sleep(0.1)
			d.off()
		elif i == 2:
			self.widgetl00L2.setText("Heizspirale an")
			dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
			dut.init()
			d = dut["PowerSupply"]
			d.set_channel(2)
			time.sleep(0.1)
			d.on()


	def messurment_frequency(self, i):
		global how_often
		how_often = i


	def index_changed_a(self, i):
		global gain_a
		gain = i
		if gain == 0:
			gain_a = 2
		elif gain == 1:
			gain_a = 1
		elif gain == 2:
			gain_a = 4
		elif gain == 3:
			gain_a = 8
		elif gain == 4:
			gain_a = 16

	def index_changed_b(self, i):
		global gain_b
		gain = i
		if gain == 0:
			gain_b = 2
		elif gain == 1:
			gain_b = 1
		elif gain == 2:
			gain_b = 4
		elif gain == 3:
			gain_b = 8
		elif gain == 4:
			gain_b = 16

	def index_changed_c(self, i):
		global gain_c
		gain = i
		if gain == 0:
			gain_c = 1
		elif gain == 1:
			gain_c = 2
		elif gain == 2:
			gain_c = 4
		elif gain == 3:
			gain_c = 8
		elif gain == 4:
			gain_c = 16


	def test_connection(self):
		try:
			data = [2,2,1,0]
			A = adc_main.main("-c", data)
			self.widgetl00L5.setText("Pc und Pi \nsind verbunden")
		except:
			self.widgetl00L5.setText("Konnte keine Verbindung herstellen. \nStarte \"ads_main.py -s\" auf dem Pi \noder \"ads_main.py -c\" auf dem Pc")


	def set_data(self):
		try:
			data = [gain_a,gain_b,gain_c,0]
			A = adc_main.main("-c", data)
			self.widgetl00L6.setText("Neue Range wurde \nerfolgreich gesetzt")
		except:
			self.widgetl00L6.setText("Das setzen der Range hat nicht \nfunktioniert. Verbindung testen")

	def TFM_test_21_func(self):
		global TFM_test_21

		QApplication.processEvents()
		self.widgetl11L17.setText("Test 21 Messung begonnen.\nBitte warte, dies dauert einige Minuten")
		QApplication.processEvents()
		go = 0

		lam1 = []
		lam2 = []
		lam3 = []
		var_lam1 = []
		var_lam2 = []
		var_lam3 = []

		while go < 49:
			dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
			dut.init()
			d = dut["PowerSupply"]
			d.set_channel(2)
			time.sleep(0.05)
			vol = d.get_voltage()
			time.sleep(0.05)
			cur = d.get_current()

			print(go)
			data = [1,1,1,1]
			A = adc_main.main("-c", data)

			f1 = 1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*(-5.775*10**(-7))*((100*(A[0][0]/(A[5][0]-A[0][0])))-100))))*np.sqrt((A[0][0]/(A[5][0]-A[0][0]))**2*0.00324**2+((100*(A[0][0]/(A[5][0]-A[0][0])**2))**2*(A[5][1])**2)+((100*(A[5][0]/(A[0][0]-A[5][0])**2)))**2*(A[0][1])**2)+0.05
			f2 = 1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*-5.775*10**(-7)*((100*(A[1][0]/(A[5][0]-A[1][0])))-100))))*np.sqrt((A[1][0]/(A[5][0]-A[1][0]))**2*0.00324**2+((100*(A[1][0]/(A[5][0]-A[1][0])**2))**2*(A[5][1])**2)+((100*(A[5][0]/(A[1][0]-A[5][0])**2)))**2*(A[1][1])**2)+0.05
			f3 = 1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*-5.775*10**(-7)*((100*(A[2][0]/(A[5][0]-A[2][0])))-100))))*np.sqrt((A[2][0]/(A[5][0]-A[2][0]))**2*0.00324**2+((100*(A[2][0]/(A[5][0]-A[2][0])**2))**2*(A[5][1])**2)+((100*(A[5][0]/(A[2][0]-A[5][0])**2)))**2*(A[2][1])**2)+0.05
			f4 = 1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*-5.775*10**(-7)*((100*(A[3][0]/(A[5][0]-A[3][0])))-100))))*np.sqrt((A[3][0]/(A[5][0]-A[3][0]))**2*0.00324**2+((100*(A[3][0]/(A[5][0]-A[3][0])**2))**2*(A[5][1])**2)+((100*(A[5][0]/(A[3][0]-A[5][0])**2)))**2*(A[3][1])**2)+0.05
	
			T1 = ((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(100*(A[0][0]/(A[5][0]-A[0][0]))))))/(2*(-5.775*10**(-7)*100)))
			T2 = ((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(100*(A[1][0]/(A[5][0]-A[1][0]))))))/(2*(-5.775*10**(-7)*100)))
			T3 = ((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(99.62*(A[2][0]/(A[5][0]-A[2][0]))))))/(2*(-5.775*10**(-7)*100)))
			T4 = ((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(99.95*(A[3][0]/(A[5][0]-A[3][0]))))))/(2*(-5.775*10**(-7)*100)))

			lam1 = np.append(lam1,(float(cur)*float(vol))/(T1-T2)*0.05/(0.0001*np.pi))
			lam2 = np.append(lam2,(float(cur)*float(vol))/(T2-T3)*thick/(0.0001*np.pi))
			lam3 = np.append(lam3,(float(cur)*float(vol))/(T3-T4)*0.05/(0.0001*np.pi))
			var_lam1 = np.append(var_lam1,np.sqrt(((float(cur)*float(vol))/(T1-T2)**2*0.05/(0.0001*np.pi))**2*(f1**2+f2**2)))
			var_lam2 = np.append(var_lam2,np.sqrt(((float(cur)*float(vol))/(T2-T3)**2*thick/(0.0001*np.pi))**2*(f2**2+f3**2)))
			var_lam3 = np.append(var_lam3,np.sqrt(((float(cur)*float(vol))/(T3-T4)**2*0.05/(0.0001*np.pi))**2*(f3**2+f4**2)))
			go += 1

		print(len(lam3),len(var_lam3))
		lambda1=np.sum(lam1/var_lam1**2)/np.sum(1/var_lam1**2)
		lambda2=np.sum(lam2/var_lam2**2)/np.sum(1/var_lam2**2)
		lambda3=np.sum(lam3/var_lam3**2)/np.sum(1/var_lam3**2)
		QApplication.processEvents()
		self.widgetl10L10.setText(str(round(lambda1,2))+'\t'+str(round(np.sqrt(1/np.sum(1/var_lam1**2)),2)))
		self.widgetl10L11.setText(str(round(lambda2,2))+'\t'+str(round(np.sqrt(1/np.sum(1/var_lam2**2)),2)))
		self.widgetl10L12.setText(str(round(lambda3,2))+'\t'+str(round(np.sqrt(1/np.sum(1/var_lam3**2)),2)))
		

		TFM_test_21 = (0.0092/lambda2-0.0076/lambda1)*(10**4)
		TFM_error = np.sqrt((0.0092/(lambda2)**2)**2*(np.sqrt(1/np.sum(1/var_lam2**2)))**2+(0.0076/(lambda1)**2)**2*(np.sqrt(1/np.sum(1/var_lam1**2)))**2+(1/(lambda2)-1/(lambda1))**2*(0.0005)**2)*10**4

		self.widget00DSB4.setValue(TFM_test_21.round(2))
		print('TFM test 21:' + str(TFM_test_21.round(2)) + '+/-' + str(TFM_error.round(2)))

		QApplication.processEvents()
		self.widgetl11L17.setText("Test 21 Messung abgeschlossen")
		QApplication.processEvents()



	def start_messurment(self):
		global measurment_run
		global measurment_run_extra
		global serial_number
		global TFM_test_21

		if TFM_test_21 == 0.00:
			QApplication.processEvents()
			self.widgetl11L17.setText("Keine Vergleichs TFM angegeben oder gemessen.\nMessung wird nicht durchgeführt.\nSollte eine Messung ohne Vergleichs TFM durchgeführt\nwerden, bitte 0.01cm²K/W eintragen")
			return 0

		QApplication.processEvents()
		self.widgetl11L17.setText("Neue Messung begonnen.\nBitte warten, dies dauert einige Minuten")
		QApplication.processEvents()

		try:
			os.mkdir("Produktion/%s"%(serial_number))
		except:
			pass
		go = 0
		datei = open('Produktion/%s/Messung%s_%s.txt'%(serial_number,measurment_run,serial_number),'w')
		datei1 = open('Produktion/Vollständige_Temp_Kurve_.txt','a')
		while go < how_often:
			dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
			dut.init()
			d = dut["PowerSupply"]
			d.set_channel(2)
			time.sleep(0.05)
			vol = d.get_voltage()
			time.sleep(0.05)
			cur = d.get_current()

			print(go)
			data = [1,1,1,1]
			A = adc_main.main("-c", data)


			f1=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*(-5.775*10**(-7))*((100*(A[0][0]/(A[5][0]-A[0][0])))-100))))*np.sqrt((A[0][0]/(A[5][0]-A[0][0]))**2*0.00324**2+((100*(A[0][0]/(A[5][0]-A[0][0])**2))**2*(A[5][1])**2)+((100*(A[5][0]/(A[0][0]-A[5][0])**2)))**2*(A[0][1])**2)+0.05
			f2=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*-5.775*10**(-7)*((100*(A[1][0]/(A[5][0]-A[1][0])))-100))))*np.sqrt((A[1][0]/(A[5][0]-A[1][0]))**2*0.00324**2+((100*(A[1][0]/(A[5][0]-A[1][0])**2))**2*(A[5][1])**2)+((100*(A[5][0]/(A[1][0]-A[5][0])**2)))**2*(A[1][1])**2)+0.05
			f3=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*-5.775*10**(-7)*((100*(A[2][0]/(A[5][0]-A[2][0])))-100))))*np.sqrt((A[2][0]/(A[5][0]-A[2][0]))**2*0.00324**2+((100*(A[2][0]/(A[5][0]-A[2][0])**2))**2*(A[5][1])**2)+((100*(A[5][0]/(A[2][0]-A[5][0])**2)))**2*(A[2][1])**2)+0.05
			f4=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*-5.775*10**(-7)*((100*(A[3][0]/(A[5][0]-A[3][0])))-100))))*np.sqrt((A[3][0]/(A[5][0]-A[3][0]))**2*0.00324**2+((100*(A[3][0]/(A[5][0]-A[3][0])**2))**2*(A[5][1])**2)+((100*(A[5][0]/(A[3][0]-A[5][0])**2)))**2*(A[3][1])**2)+0.05
	
			T1=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(100*(A[0][0]/(A[5][0]-A[0][0]))))))/(2*(-5.775*10**(-7)*100)))
			T2=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(100*(A[1][0]/(A[5][0]-A[1][0]))))))/(2*(-5.775*10**(-7)*100)))
			T3=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(99.62*(A[2][0]/(A[5][0]-A[2][0]))))))/(2*(-5.775*10**(-7)*100)))
			T4=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(99.95*(A[3][0]/(A[5][0]-A[3][0]))))))/(2*(-5.775*10**(-7)*100)))


			datei.write(str((T1))+'\t'+str((f1))
			+'\t'+str((T2))+'\t'+str((f2))
			+'\t'+str((T3))+'\t'+str((f3))
			+'\t'+str((T4))+'\t'+str((f4))
			+'\t'+str(round(((A[4][0]*1000-1.55639)/2.31754),4))+'\t'+str(round((np.sqrt((1/2.31754)**2*(A[4][1]*1000)**2+(A[4][0]*1000/2.31754**2)**2*0.01692**2+(1/2.31754)**2*0.4216**2)),4))
			+'\t'+str(((float(cur)*float(vol))/(T1-T2)*0.05/(0.0001*np.pi)))+'\t'+str((np.sqrt(((float(cur)*float(vol))/(T1-T2)**2*0.05/(0.0001*np.pi))**2*(f1**2+f2**2))))
			+'\t'+str(((float(cur)*float(vol))/(T2-T3)*thick/(0.0001*np.pi)))+'\t'+str((np.sqrt(((float(cur)*float(vol))/(T2-T3)**2*thick/(0.0001*np.pi))**2*(f2**2+f3**2))))
			+'\t'+str(((float(cur)*float(vol))/(T3-T4)*0.05/(0.0001*np.pi)))+'\t'+str((np.sqrt(((float(cur)*float(vol))/(T3-T4)**2*0.05/(0.0001*np.pi))**2*(f3**2+f4**2))))
			+'\t'+str(float(cur)*float(vol))
			+'\n')
			datei1.write(str(round(T1,6))+'\t'+str(round(f1,6))
			+'\t'+str(round(T2,6))+'\t'+str(round(f2,6))
			+'\t'+str(round(T3,6))+'\t'+str(round(f3,6))
			+'\t'+str(round(T4,6))+'\t'+str(round(f4,6))
			+'\t'+str(round(((A[4][0]*1000-1.55639)/2.31754),4))+'\t'+str(round((np.sqrt((1/2.31754)**2*(A[4][1]*1000)**2+(A[4][0]*1000/2.31754**2)**2*0.01692**2+(1/2.31754)**2*0.4216**2)),4))
			+'\t'+str((float(cur)*float(vol))/(T1-T2)*0.05/(0.0001*np.pi))+'\t'+str((np.sqrt(((float(cur)*float(vol))/(T1-T2)**2*0.05/(0.0001*np.pi))**2*(f1**2+f2**2))))
			+'\t'+str((float(cur)*float(vol))/(T2-T3)*thick/(0.0001*np.pi))+'\t'+str((np.sqrt(((float(cur)*float(vol))/(T2-T3)**2*thick/(0.0001*np.pi))**2*(f2**2+f3**2))))
			+'\t'+str((float(cur)*float(vol))/(T3-T4)*0.05/(0.0001*np.pi))+'\t'+str((np.sqrt(((float(cur)*float(vol))/(T3-T4)**2*0.05/(0.0001*np.pi))**2*(f3**2+f4**2))))
			+'\t'+str(float(cur)*float(vol))
			+'\n')

			self.widgetl10L5.setText(str(round(((A[4][0]*1000-1.55639)/2.31754),2))+'\t'+str(round((np.sqrt((1/2.31754)**2*(A[4][1]*1000)**2+(A[4][0]*1000/2.31754**2)**2*0.01692**2+(1/2.31754)**2*0.4216**2)),2)))
			time.sleep(0.05)
			go += 1

		datei1.close()
		datei.close()

		#---------------Plot_Messung---------------#

		# Load data
		datafile = np.loadtxt('Produktion/%s/Messung%s_%s.txt'%(serial_number,measurment_run,serial_number), delimiter='\t', unpack=True)
		a,da,b,db,c,dc,d,dd = 0,1,2,3,4,5,6,7
		A,dA,B,dB,C,dC,D,dD = datafile[a],datafile[da],datafile[b],datafile[db],datafile[c],datafile[dc],datafile[d],datafile[dd]

		# Creat timescale
		x = np.array([])
		for i in range(0,len(A)):
			x = np.append(x,i)

		ax = plt.figure(dpi=350).add_subplot(1,1,1)

		# Creat axis and draw function
		plt.errorbar(x,A,yerr=dA, color='royalblue',fmt='.',label='Temperatur oben')
		plt.errorbar(x,B,yerr=dB, color='firebrick',fmt='.',label='Temperatur mitte oben')
		plt.errorbar(x,C,yerr=dC, color='yellow',fmt='.',label='Temperatur mitte unten')
		plt.errorbar(x,D,yerr=dD, color='orangered',fmt='.',label='Temperatur unten')

		# Some adjustments to the plot
		plt.xlabel('Datenpunkt/5s')
		plt.ylabel('Temperatur / °C')
		plt.legend(loc='best')
		plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
		plt.tight_layout()
		plt.savefig('Produktion/%s/Messung%s_%s.png'%(serial_number,measurment_run,serial_number))

		# Creat the document where Lambda, errors and other values are stored
		datei = open('Produktion/%s/Gemittelte_Werte_%s.txt'%(serial_number,serial_number),'a')

		lam1, lam2, lam3=datafile[10],datafile[12],datafile[14]
		var_lam1, var_lam2, var_lam3=datafile[11],datafile[13],datafile[15]
		weigth, dweigth=datafile[8],datafile[9]
		lambda1=np.sum(lam1/var_lam1**2)/np.sum(1/var_lam1**2)
		lambda2=np.sum(lam2/var_lam2**2)/np.sum(1/var_lam2**2)
		lambda3=np.sum(lam3/var_lam3**2)/np.sum(1/var_lam3**2)
		self.widgetl10L10.setText(str(round(lambda1,2))+'\t'+str(round(np.sqrt(1/np.sum(1/var_lam1**2)),2)))
		self.widgetl10L11.setText(str(round(lambda2,2))+'\t'+str(round(np.sqrt(1/np.sum(1/var_lam2**2)),2)))
		self.widgetl10L12.setText(str(round(lambda3,2))+'\t'+str(round(np.sqrt(1/np.sum(1/var_lam3**2)),2)))
		

		TFM=(0.0092/lambda2-0.0076/lambda1)*(10**4)
		TFM_error=np.sqrt((0.0092/(lambda2)**2)**2*(np.sqrt(1/np.sum(1/var_lam2**2)))**2+(0.0076/(lambda1)**2)**2*(np.sqrt(1/np.sum(1/var_lam1**2)))**2+(1/(lambda2)-1/(lambda1))**2*(0.0005)**2)*10**4


		datei.write('Gewicht' +'\t'+ 'err' +'\t'+ 'lambda_1' +'\t'+ 'err' +'\t'+ 'lambda_2' +'\t'+ 'err' +'\t'+ 'lambda_3' +'\t'+ 'err' +'\t'+ 'TFM_DUT' +'\t'+ 'err' +'\t'+ 'TFM_test_21'
		+'\n'+str(weigth[1])+'\t'+str(dweigth[1])
		+'\t'+str((lambda1.round(3)))+'\t'+str((np.sqrt(1/np.sum(1/var_lam1**2))).round(3))
		+'\t'+str((lambda2).round(3))+'\t'+str((np.sqrt(1/np.sum(1/var_lam2**2))).round(3))
		+'\t'+str((lambda3).round(3))+'\t'+str((np.sqrt(1/np.sum(1/var_lam3**2))).round(3))
		+'\t'+str(TFM.round(2))+'\t'+str(TFM_error.round(2))
		+'\t'+str(TFM_test_21)
		+'\n')

		datei.close()


		#---------------Plot_complet_temp_curve---------------#

		datafile = np.loadtxt('Produktion/Vollständige_Temp_Kurve_.txt', delimiter='\t', unpack=True)
		a,da,b,db,c,dc,d,dd = 0,1,2,3,4,5,6,7
		A,dA,B,dB,C,dC,D,dD = datafile[a],datafile[da],datafile[b],datafile[db],datafile[c],datafile[dc],datafile[d],datafile[dd]


		x = np.array([])
		for i in range(0,len(A)):
			x = np.append(x,i)

		#creat axis and draw function
		ax = plt.figure(dpi=350).add_subplot(1,1,1)

		plt.errorbar(x,A,yerr=dA, color='royalblue',fmt='-',label='Temperatur oben')
		plt.errorbar(x,B,yerr=dB, color='firebrick',fmt='-',label='Temperatur mitte oben')
		plt.errorbar(x,C,yerr=dC, color='yellow',fmt='-',label='Temperatur mitte unten')
		plt.errorbar(x,D,yerr=dD, color='orangered',fmt='-',label='Temperatur unten')

		plt.xlabel('Datenpunkt / 5s')
		plt.ylabel('Temperatur / °C')
		plt.legend(loc='best')
		plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
		plt.tight_layout()
		plt.savefig('Produktion/%s/Vollständige_Temp_Kurve_%s.png'%(serial_number,serial_number))

		shutil.copy('Produktion/Vollständige_Temp_Kurve_.txt', 'Produktion/%s/Vollständige_Temp_Kurve_%s.txt'%(serial_number,serial_number))
		os.remove('Produktion/Vollständige_Temp_Kurve_.txt')

		measurment_run = 0
		measurment_run_extra += 1
		self.widgetl11L17.setText("Messung erfolgreich Beendet")



	def set_text(self,A):
		#dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
		#dut.init()
		#d = dut["PowerSupply"]
		#d.set_channel(2)
		#time.sleep(0.05)
		#vol = d.get_voltage()
		#time.sleep(0.05)
		#cur = d.get_current()

		####Fehler####
		#f1=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*(-5.775*10**(-7))*((100*(A[0][0]/(A[5][0]-A[0][0])))-100))))*np.sqrt((A[0][0]/(A[5][0]-A[0][0]))**2*0.00324**2+((100*(A[0][0]/(A[5][0]-A[0][0])**2))**2*(A[5][1])**2)+((100*(A[5][0]/(A[0][0]-A[5][0])**2)))**2*(A[0][1])**2)+0.05
		#f2=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*-5.775*10**(-7)*((100*(A[1][0]/(A[5][0]-A[1][0])))-100))))*np.sqrt((A[1][0]/(A[5][0]-A[1][0]))**2*0.00324**2+((100*(A[1][0]/(A[5][0]-A[1][0])**2))**2*(A[5][1])**2)+((100*(A[5][0]/(A[1][0]-A[5][0])**2)))**2*(A[1][1])**2)+0.05
		#f3=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*-5.775*10**(-7)*((100*(A[2][0]/(A[5][0]-A[2][0])))-100))))*np.sqrt((A[2][0]/(A[5][0]-A[2][0]))**2*0.00324**2+((100*(A[2][0]/(A[5][0]-A[2][0])**2))**2*(A[5][1])**2)+((100*(A[5][0]/(A[2][0]-A[5][0])**2)))**2*(A[2][1])**2)+0.05
		#f4=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*-5.775*10**(-7)*((100*(A[3][0]/(A[5][0]-A[3][0])))-100))))*np.sqrt((A[3][0]/(A[5][0]-A[3][0]))**2*0.00324**2+((100*(A[3][0]/(A[5][0]-A[3][0])**2))**2*(A[5][1])**2)+((100*(A[5][0]/(A[3][0]-A[5][0])**2)))**2*(A[3][1])**2)+0.05
	
		#T1=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(100*(A[0][0]/(A[5][0]-A[0][0]))))))/(2*(-5.775*10**(-7)*100)))
		#T2=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(100*(A[1][0]/(A[5][0]-A[1][0]))))))/(2*(-5.775*10**(-7)*100)))
		#T3=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(99.62*(A[2][0]/(A[5][0]-A[2][0]))))))/(2*(-5.775*10**(-7)*100)))
		#T4=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(99.95*(A[3][0]/(A[5][0]-A[3][0]))))))/(2*(-5.775*10**(-7)*100)))


		#self.widgetl10L1.setText(str(round(T1,2))+'\t'+str(round(f1,3)))
		#self.widgetl10L2.setText(str(round(T2,2))+'\t'+str(round(f2,3)))
		#self.widgetl10L3.setText(str(round(T3,2))+'\t'+str(round(f3,3)))
		#self.widgetl10L4.setText(str(round(T4,2))+'\t'+str(round(f4,3)))
		self.widgetl10L5.setText(str(round(((A[4][0]*1000-1.55639)/2.31754),2))+'\t'+str(round((np.sqrt((1/2.31754)**2*(A[4][1]*1000)**2+(A[4][0]*1000/2.31754**2)**2*0.01692**2+(1/2.31754)**2*0.4216**2)),2)))
		#self.widgetl10L6.setText(str(round(A[5][0],6))+'\t'+str(round(A[5][1],6)))
		#self.widgetl10L7.setText(str(round((float(cur)*float(vol))/(T1-T2)*0.05/(0.0001*np.pi),5))+'\t'+str(round(np.sqrt(((float(cur)*float(vol))/(T1-T2)**2*0.05/(0.0001*np.pi))**2*(f1**2+f2**2)+(float(cur)/(T1-T2)*0.05/(0.0001*np.pi))**2*0.005**2+(float(vol)/(T1-T2)*0.05/(0.0001*np.pi))**2*0.0005**2+(((float(cur)*float(vol))/(T3-T4)*1/(0.0001*np.pi))**2*0.004**2)),5)))
		#self.widgetl10L8.setText(str(round((float(cur)*float(vol))/(T2-T3)*thick/(0.0001*np.pi),5))+'\t'+str(round(np.sqrt(((float(cur)*float(vol))/(T2-T3)**2*thick/(0.0001*np.pi))**2*(f2**2+f3**2)+(float(cur)/(T2-T3)*thick/(0.0001*np.pi))**2*0.005**2+(float(vol)/(T2-T3)*thick/(0.0001*np.pi))**2*0.0005**2+(((float(cur)*float(vol))/(T2-T3)*1/(0.0001*np.pi))**2*0.0001**2)),5)))
		#self.widgetl10L9.setText(str(round((float(cur)*float(vol))/(T3-T4)*0.05/(0.0001*np.pi),5))+'\t'+str(round(np.sqrt(((float(cur)*float(vol))/(T3-T4)**2*0.05/(0.0001*np.pi))**2*(f3**2+f4**2)+(float(cur)/(T3-T4)*0.05/(0.0001*np.pi))**2*0.005**2+(float(vol)/(T3-T4)*0.05/(0.0001*np.pi))**2*0.0005**2+(((float(cur)*float(vol))/(T3-T4)*1/(0.0001*np.pi))**2*0.004**2)),5)))

	
		#self.widgetl10L13.setText(str(round((T1-T2)*np.pi/(float(cur)*float(vol)),5))+'\t'+str(round(np.sqrt(1/(float(cur)*float(vol))**2*(f1**2+f2**2)),5)))
		#self.widgetl10L14.setText(str(round((T2-T3)*np.pi/(float(cur)*float(vol)),5))+'\t'+str(round(np.sqrt(1/(float(cur)*float(vol))**2*(f1**2+f2**2)),5)))
		#self.widgetl10L15.setText(str(round((T3-T4)*np.pi/(float(cur)*float(vol)),5))+'\t'+str(round(np.sqrt(1/(float(cur)*float(vol))**2*(f1**2+f2**2)),5)))
		#self.widgetl10L16.setText(str(round((T2-T3)*np.pi/(float(cur)*float(vol))-2*0.0034/0.05*(T1-T2)*np.pi/(float(cur)*float(vol)),5)))


def main():
	app = QApplication(sys.argv)

	window = MainWindow()
	window.show()

	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
	
