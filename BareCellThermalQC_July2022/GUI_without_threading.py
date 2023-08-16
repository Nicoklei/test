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
		layout011 = QHBoxLayout()

		layout11 = QVBoxLayout()

		#Variables
		global gain_a
		gain_a=2
		global gain_b
		gain_b=2
		global gain_c
		gain_c=1
		global gain_a_e
		gain_a_e=2
		global gain_b_e
		gain_b_e=2
		global gain_c_e
		gain_c_e=1
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
		global messurment_run
		messurment_run = 0
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
		##without hardware comment out##
		#data = [2,2,1,0]
		#A = adc_main.main("-c", data)

	
		#global how_many_times
		#how_many_times=20
		global v_values
		v_values=np.array([])

		#--------------add Widgets--------------#
		####sector00####

		self.widgetl00L1 = QLabel("Starte Peltier-Element")
		self.widgetl00L2 = QLabel("Starte Heizspirale")
		self.widgetl00L3 = QLabel("Jetzige Spannung:\n0.000")
		self.widgetl00L4 = QLabel("Jetzige Spannung:\n0.000")
		self.widgetl00L5 = QLabel("Keine Verbindung zum Pi")
		self.widgetl00L6 = QLabel("Knopf drücken um Range zu ändern.\nAnsonsten wird die vorherige oder \ndie Standart Range verwendet")
		self.widgetl00L7 = QLabel()
		self.widgetl00L8 = QLabel("Jetziger Strom:\n0.000")
		self.widgetl00L9 = QLabel("Jetziger Strom:\n0.000")


		widget00SB1 = QSpinBox()
		widget00SB2 = QSpinBox()
		self.widgetPB2 = QPushButton("Messung Starten")
		self.widgetPB3 = QPushButton("Verbindung Testen")
		self.widgetPB4 = QPushButton("Range setzen")
		self.widgetPB6 = QPushButton("Spannung setzen")
		self.widgetPB7 = QPushButton("Spannung setzen")
		self.widgetPB8 = QPushButton("Strom setzen")
		self.widgetPB9 = QPushButton("Strom setzen")
		self.widgetPB10 = QPushButton("Neue Messreihe Starten")
		self.widgetPB11 = QPushButton("Graph Leeren")

		widgetS1 = QSlider()	

		widgetl00L1 = QLabel("Test zur Verbindung zum Pi")
		widgetl00L2 = QLabel("Range ADC1 (Temperaturmessung oben):")
		widgetl00L3 = QLabel("Range ADC2 (Temperaturmessung unten):")
		widgetl00L4 = QLabel("Range ADC3:")
		widgetl00L5 = QLabel("Anzahl der \nMessungen")
		widgetl00L6 = QLabel("Dicke des Materials \nzwischen Aluminium Stäben:")
		widgetl00L7 = QLabel("Name Testobjekt:")
		widgetl00L8 = QLabel("Peltier-Element Steuerung")
		widgetl00L9 = QLabel("Heizspirale Steuerung")
		widgetl00L10 = QLabel("Einstellungen zur Messung eines DUT")
		widgetl00L11 = QLabel("Einstellungen des Messbereiches der ADC's")

		widget00CB1 = QComboBox()
		widget00CB2 = QComboBox()
		widget00CB3 = QComboBox()

		widget00SB3 = QSpinBox()

		widget00DSB1 = QDoubleSpinBox()
		widget00DSB2 = QDoubleSpinBox()
		widget00DSB3 = QDoubleSpinBox()

		widget00ChB1 = QCheckBox()
		widget00ChB2 = QCheckBox()

		widget00LE1 = QLineEdit()
			

		####sector10####
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
		widgetl10L13 = QLabel("Ausgabe der Volt \nWerte des ADC")

		widgetl10L1 = QLabel("Temperatursensor oben / °C:")
		widgetl10L2 = QLabel("Temperatursensor mitte oben / °C:")
		widgetl10L3 = QLabel("Temperatursensor mitte unten / °C:")
		widgetl10L4 = QLabel("Temperatursensor unten / °C:")
		widgetl10L5 = QLabel("Gewicht auf Device / kg:")
		widgetl10L6 = QLabel("Spannung Temperatursensoren:")
		widgetl10L7 = QLabel("Lambda1 (oben:)")
		widgetl10L8 = QLabel("Lambda2 (mitte):")
		widgetl10L9 = QLabel("Lambda3 (unten):")
		widgetl10L15 = QLabel("Wärmewiderstand oben:")
		widgetl10L16 = QLabel("Wärmewiderstand mitte:")
		widgetl10L17 = QLabel("Wärmewiderstand unten:")
		widgetl10L18 = QLabel("Wärmewiderstand DUT:")
		widgetl10L10 = QLabel("Ergebnis Lambda oben:")
		widgetl10L11 = QLabel("Ergebnis Lambda mitte:")
		widgetl10L12 = QLabel("Ergebnis Lambda unten:")

		####sector01####
		widgetl01L3 = QLabel("Eingabe des Volt Bereiches \nund Gains zur \nKalibration der ADCs")
		widgetl01L4 = QLabel("Volt Eingabe:")
		widgetl01L5 = QLabel("Gain Eingabe:")
		widgetl01L6 = QLabel("ADC1 (Temperaturmessung):")
		widgetl01L7 = QLabel("ADC2:")
		widgetl01L8 = QLabel("ADC3:")
		widgetl01L9 = QLabel("Messabstände:")
		
		self.widgetl01L10 = QLabel()
		self.widgetl01L11 = QLabel("Knopf drücken um Gain zu ändern.\nAnsonsten wird das vorherige oder \ndas Standart Gain verwendet")

		self.widgetPB5 = QPushButton("Gain setzen")

		widgetSB1 = QSpinBox()
		widgetSB2 = QSpinBox()
		widgetCB1 = QComboBox()
		widgetCB2 = QComboBox()
		widgetCB3 = QComboBox()
		widgetPB1 = QPushButton("Starte ADC Kalibration")

		####sector11####
		self.widget11G = pg.PlotWidget()
		self.widget11G.setBackground('w')
		self.widget11G.addLegend()
		self.widget11G.showGrid(x=True, y=True)

				
		#-------add functions to Widgets-------# 
		####sector00####
		widgetS1.valueChanged.connect(self.value_change)

		font6 = widgetl00L1.font()
		font6.setPointSize(11)
		widgetl00L1.setFont(font6)
		widgetl00L8.setFont(font6)
		widgetl00L9.setFont(font6)
		widgetl00L10.setFont(font6)
		widgetl00L11.setFont(font6)

		##without hardware comment out##
		#dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
		#dut.init()
		#d = dut["PowerSupply"]
		#d.set_channel(1)
		#time.sleep(0.05)
		#vol = d.get_target_voltage()

		widget00SB1.setSuffix("mV")
		widget00SB1.setMinimum(0)
		widget00SB1.setMaximum(32000)
		#widget00SB1.setValue(int(float(vol)*1000))
		widget00SB1.valueChanged.connect(self.start_peltier)
		
		##without hardware comment out##
		#d.set_channel(2)
		#time.sleep(0.05)
		#vol = d.get_target_voltage()

		widget00SB2.setSuffix("mV")
		widget00SB2.setMinimum(0)
		widget00SB2.setMaximum(32000)
		#widget00SB2.setValue(int(float(vol)*1000))
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
		widget00SB3.valueChanged.connect(self.messurment_frequancy)
		widget00SB3.setValue(10)

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

		widget00ChB1.stateChanged.connect(self.on_off_peltier)
		widget00ChB2.stateChanged.connect(self.on_off_spirale)

		widget00LE1.textEdited.connect(self.text_edited)

		####sector10####
		font2 = widgetl10L13.font()
		font2.setPointSize(11)
		widgetl10L13.setFont(font2)


		####sector01####
		#Spinboxes
		widgetSB1.setSuffix("mV")
		widgetSB1.setMinimum(0)
		widgetSB1.setMaximum(3300)
		widgetSB1.valueChanged.connect(self.voltage_value)
		widgetSB2.setMinimum(0)
		widgetSB2.setMaximum(50)
		widgetSB2.valueChanged.connect(self.messurment_frequancy_cal)
		widgetSB2.setValue(20)

		self.widgetPB5.clicked.connect(self.set_data2)

		font1 = widgetl01L3.font()
		font1.setPointSize(11)
		widgetl01L3.setFont(font1)

		font3 = widgetl01L6.font()
		font3.setPointSize(8)
		widgetl01L6.setFont(font3)

		font4 = widgetl01L7.font()
		font4.setPointSize(8)
		widgetl01L7.setFont(font4)

		font5 = widgetl01L8.font()
		font5.setPointSize(8)
		widgetl01L8.setFont(font5)


				
		#ComboBoxes
		widgetCB1.NoInsert
		widgetCB1.addItems(["2,048V", "4,096V", "1,024V", "0,512V", "0,256V"])
		widgetCB1.currentIndexChanged.connect(self.index_changed_a_e)
		widgetCB2.NoInsert
		widgetCB2.addItems(["2,048V", "4,096V", "1,024V", "0,512V", "0,256V"])
		widgetCB2.currentIndexChanged.connect(self.index_changed_b_e)
		widgetCB3.NoInsert
		widgetCB3.addItems(["4,096V", "2,048V", "1,024V", "0,512V", "0,256V"])
		widgetCB3.currentIndexChanged.connect(self.index_changed_c_e)
		
		widgetPB1.clicked.connect(self.start_kalibration)

		#----------Timer----------#
		##without hardware comment out##
		#self.timer = QTimer()
		#self.timer.start(2000)
		#self.timer.timeout.connect(self.update_spirale_peltier)

		#self.test_connection()

		#---------add Widgets into Layouts---------#
		#sector00
		layout00.addWidget(widgetl00L1)
		layout003.addWidget(self.widgetl00L5)
		layout003.addWidget(self.widgetPB3)
		layout00.addLayout(layout003)
		layout00.addWidget(widgetl00L8)
		widgetl00L8.setContentsMargins(0,12,0,0)
		layout006.addWidget(self.widgetl00L1)
		layout006.addWidget(widget00ChB1)
		layout00.addLayout(layout006)
		layout001.addWidget(widget00SB1)
		layout001.addWidget(self.widgetPB6)
		layout001.addWidget(self.widgetl00L3)
		#layout001.setContentsMargins(15,0,0,0)
		layout002.addWidget(widget00SB2)
		layout002.addWidget(self.widgetPB7)
		layout002.addWidget(self.widgetl00L4)
		#layout002.setContentsMargins(15,0,0,0)
		layout00.addLayout(layout001)
		layout008.addWidget(widget00DSB1)
		layout008.addWidget(self.widgetPB8)
		layout008.addWidget(self.widgetl00L8)
		#layout008.setContentsMargins(15,0,0,0)
		layout00.addLayout(layout008)
		layout00.addWidget(widgetl00L9)
		widgetl00L9.setContentsMargins(0,12,0,0)
		layout007.addWidget(self.widgetl00L2)
		layout007.addWidget(widget00ChB2)
		#layout007.setContentsMargins(0,12,0,0)
		layout00.addLayout(layout007)
		layout00.addLayout(layout002)
		layout009.addWidget(widget00DSB2)
		layout009.addWidget(self.widgetPB9)
		layout009.addWidget(self.widgetl00L9)
		#layout009.setContentsMargins(15,0,0,0)
		layout00.addLayout(layout009)
		layout00.addWidget(widgetl00L10)
		widgetl00L10.setContentsMargins(0,12,0,0)
		layout005.addWidget(widgetl00L5)
		layout005.addWidget(widget00SB3)
		layout0010.addWidget(widgetl00L6)
		layout0010.addWidget(widget00DSB3)
		layout00.addLayout(layout0010)
		layout0011.addWidget(widgetl00L7)
		layout0011.addWidget(widget00LE1)
		layout00.addLayout(layout0011)
		layout00.addLayout(layout005)
		layout00.addWidget(self.widgetPB10)
		layout00.addWidget(self.widgetPB11)
		layout00.addWidget(widgetl00L11)
		widgetl00L11.setContentsMargins(0,12,0,0)
		layout00.addWidget(widgetl00L2)
		layout00.addWidget(widget00CB1)
		layout00.addWidget(widgetl00L3)
		layout00.addWidget(widget00CB2)
		layout00.addWidget(widgetl00L4)
		layout00.addWidget(widget00CB3)
		layout004.addWidget(self.widgetl00L6)
		layout004.addWidget(self.widgetPB4)
		layout00.addLayout(layout004)
		layout00.addWidget(self.widgetPB2)
		layout00.addWidget(self.widgetl00L7)

	
		#sector10
		layout10.addWidget(widgetl10L13)
		layout101.addWidget(widgetl10L1)
		layout101.addWidget(self.widgetl10L1)
		layout102.addWidget(widgetl10L2)
		layout102.addWidget(self.widgetl10L2)
		layout103.addWidget(widgetl10L3)
		layout103.addWidget(self.widgetl10L3)
		layout104.addWidget(widgetl10L4)
		layout104.addWidget(self.widgetl10L4)
		layout105.addWidget(widgetl10L5)
		layout105.addWidget(self.widgetl10L5)
		layout106.addWidget(widgetl10L6)
		layout106.addWidget(self.widgetl10L6)
		layout107.addWidget(widgetl10L7)
		layout107.addWidget(self.widgetl10L7)
		layout108.addWidget(widgetl10L8)
		layout108.addWidget(self.widgetl10L8)
		layout109.addWidget(widgetl10L9)
		layout109.addWidget(self.widgetl10L9)
		layout1010.addWidget(widgetl10L10)
		layout1010.addWidget(self.widgetl10L10)
		layout1011.addWidget(widgetl10L11)
		layout1011.addWidget(self.widgetl10L11)
		layout1012.addWidget(widgetl10L12)
		layout1012.addWidget(self.widgetl10L12)
		layout1013.addWidget(widgetl10L15)
		layout1013.addWidget(self.widgetl10L13)
		layout1014.addWidget(widgetl10L16)
		layout1014.addWidget(self.widgetl10L14)
		layout1015.addWidget(widgetl10L17)
		layout1015.addWidget(self.widgetl10L15)
		layout1016.addWidget(widgetl10L18)
		layout1016.addWidget(self.widgetl10L16)
		
		#sector01
		layout01.addWidget(widgetl01L3)
		layout01.addWidget(widgetl01L9)
		layout01.addWidget(widgetSB2)
		layout01.addWidget(widgetl01L4)
		layout01.addWidget(widgetSB1)
		layout01.addWidget(widgetl01L5)
		layout01.addWidget(widgetl01L6)
		layout01.addWidget(widgetCB1)
		layout01.addWidget(widgetl01L7)
		layout01.addWidget(widgetCB2)
		layout01.addWidget(widgetl01L8)
		layout01.addWidget(widgetCB3)
		layout011.addWidget(self.widgetl01L11)
		layout011.addWidget(self.widgetPB5)
		layout01.addLayout(layout011)
		layout01.addWidget(widgetPB1)
		layout01.addWidget(self.widgetl01L10)

		#sector11
		layout11.addWidget(self.widget11G)

		#----------add Layouts into Grid----------#
	
		##more Layouts sector10##
		layout10.addLayout(layout101)
		layout10.addLayout(layout102)
		layout10.addLayout(layout103)
		layout10.addLayout(layout104)
		layout10.addLayout(layout105)
		layout10.addLayout(layout106)
		layout10.addLayout(layout107)
		layout10.addLayout(layout108)
		layout10.addLayout(layout109)
		layout10.addLayout(layout1010)
		layout10.addLayout(layout1011)
		layout10.addLayout(layout1012)
		layout10.addLayout(layout1013)
		layout10.addLayout(layout1014)
		layout10.addLayout(layout1015)
		layout10.addLayout(layout1016)

		layout.addLayout(layout00, 0, 0)
		layout.addLayout(layout10, 1, 0)
		#layout.addLayout(layout01, 0, 1)
		layout.addLayout(layout11, 0, 1)


		layout00.setContentsMargins(0,0,0,0)
		layout10.setContentsMargins(0,0,0,0)
		layout01.setContentsMargins(0,0,0,0)
		layout11.setContentsMargins(0,0,0,0)
		layout.setContentsMargins(5,5,5,5)
		layout.setSpacing(2)

		widget = QWidget()
		widget.setLayout(layout)
		self.setMinimumSize(1200,1050)
		self.setCentralWidget(widget)

	def clear_graph(self):
		self.widget11G.clear()
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
		global messurment_run
		messurment_run = 0

	def text_edited(self,s):
		global serial_number
		serial_number = s
		print(serial_number,type(serial_number))

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
		dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
		dut.init()
		d = dut["PowerSupply"]
		d.set_channel(1)
		time.sleep(0.05)
		vol = d.get_voltage()
		time.sleep(0.05)
		cur = d.get_current()
		self.widgetl00L3.setText("Jetzige Spannung\n" + str(vol))
		self.widgetl00L8.setText("Jetzige Strom\n" + str(cur))
		time.sleep(0.05)
		d.set_channel(2)
		time.sleep(0.05)
		vol = d.get_voltage()
		time.sleep(0.05)
		cur = d.get_current()
		self.widgetl00L4.setText("Jetzige Spannung\n" + str(vol))
		self.widgetl00L9.setText("Jetziger Strom\n" + str(cur))
		data = [1,1,1,1]
		A = adc_main.main("-c", data)

		self.widget11G.clear()
		global values_graph1
		values_graph1 = np.append(values_graph1,((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(99.633963*(A[0][0]/(A[5][0]-A[0][0]))))))/(2*(-5.775*10**(-7)*100))))
		global values_graph2
		values_graph2 = np.append(values_graph2,((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(99.84885*(A[1][0]/(A[5][0]-A[1][0]))))))/(2*(-5.775*10**(-7)*100))))
		global values_graph3
		values_graph3 = np.append(values_graph3,((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(99.6936*(A[2][0]/(A[5][0]-A[2][0]))))))/(2*(-5.775*10**(-7)*100))))
		global values_graph4
		values_graph4 = np.append(values_graph4,((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(99.46649*(A[3][0]/(A[5][0]-A[3][0]))))))/(2*(-5.775*10**(-7)*100))))

		global x_values_graph
		x_values_graph = np.append(x_values_graph,len(values_graph1))

		#print(x_values_graph,values_graph)
		self.widget11G.setTitle("Temperatur Verlauf", color='b')
		self.widget11G.setLabel('left','Temperatur (°C)', color='b')
		self.widget11G.setLabel('bottom', 'Datenpunkte / 2s', color='b')
		self.widget11G.plot(x_values_graph,values_graph1, pen=(0,0,0), name ='Sensor oben')
		self.widget11G.plot(x_values_graph,values_graph2, pen='b', name ='Sensor mitte oben')
		self.widget11G.plot(x_values_graph,values_graph3, pen='g', name ='Sensor mitte unten')
		self.widget11G.plot(x_values_graph,values_graph4, pen='r', name ='Sensor unten')
		
		self.set_text(A)

		#print(round(((99.633963*(A[0][0]/(A[5][0]-A[0][0])))),2),round(((99.84885*(A[1][0]/(A[5][0]-A[1][0])))),2))
		#print(round(((99.6936*(A[2][0]/(A[5][0]-A[2][0])))),2),round(((99.46649*(A[3][0]/(A[5][0]-A[3][0])))),2))

		name = 'Vorordner/Vollständige_Temp_Kurve_.txt'
		datei = open(name,'a')

		#datei.write(str(round(((100*(A[0][0]/(A[5][0]-A[0][0])))-99.954)/0.39087,2))+'\t'+str(round(np.sqrt((((100*(A[0][0]/(A[5][0]-A[0][0])))-99.954)/0.39087**2)**2*0.00049**2+(1/0.39087)**2*0.1364**2+(1/0.39087*(330/(A[0][0]-A[5][0])**2))**2*A[0][1]**2+(1/0.39087*(100*(A[0][0]/(A[5][0]-A[0][0])**2)))**2*A[5][1]**2),2))+'\t'+str(round(((100*(A[1][0]/(A[5][0]-A[1][0])))-99.954)/0.39087,2))+'\t'+str(round(np.sqrt((((100*(A[1][0]/(A[5][0]-A[1][0])))-99.954)/0.39087**2)**2*0.00049**2+(1/0.39087)**2*0.1364**2+(1/0.39087*(330/(A[1][0]-A[5][0])**2))**2*A[1][1]**2+(1/0.39087*(100*(A[1][0]/(A[5][0]-A[1][0])**2)))**2*A[5][1]**2),2))+'\t'+str(round(((100*(A[2][0]/(A[5][0]-A[2][0])))-99.954)/0.39087,2))+'\t'+str(round(np.sqrt((((100*(A[2][0]/(A[5][0]-A[2][0])))-99.954)/0.39087**2)**2*0.00049**2+(1/0.39087)**2*0.1364**2+(1/0.39087*(330/(A[2][0]-A[5][0])**2))**2*A[2][1]**2+(1/0.39087*(100*(A[2][0]/(A[5][0]-A[2][0])**2)))**2*A[5][1]**2),2))+'\t'+str(round(((100*(A[3][0]/(A[5][0]-A[3][0])))-99.954)/0.39087,2))+'\t'+str(round(np.sqrt((((100*(A[3][0]/(A[5][0]-A[3][0])))-99.954)/0.39087**2)**2*0.00049**2+(1/0.39087)**2*0.1364**2+(1/0.39087*(330/(A[3][0]-A[5][0])**2))**2*A[3][1]**2+(1/0.39087*(100*(A[3][0]/(A[5][0]-A[3][0])**2)))**2*A[5][1]**2),2))+'\t'+str(round(((A[4][0]*1000-1.556)/2.318),3))+'\t'+str(round((np.sqrt((1/2.318)**2*(A[4][1]*1000)**2+(A[4][0]*1000/2.318**2)**2*0.0169**2+(1/2.318)**2*0.03032**2)),3))+'\t'+str(round(((100.059*(A[0][0]/(A[5][0]-A[0][0])))-(100.14*(A[1][0]/(A[5][0]-A[1][0]))))/(float(cur)*float(vol)),5))+'\t'+str(round(((100.14*(A[1][0]/(A[5][0]-A[1][0])))-(100.117*(A[2][0]/(A[5][0]-A[2][0]))))/(float(cur)*float(vol)),5))+'\t'+str(round(((100.117*(A[2][0]/(A[5][0]-A[2][0])))-(99.889*(A[3][0]/(A[5][0]-A[3][0]))))/(float(cur)*float(vol)),5))+'\n')
		f1=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*(-5.775*10**(-7))*((99.633963*(A[0][0]/(A[5][0]-A[0][0])))-100))))*np.sqrt((A[0][0]/(A[5][0]-A[0][0]))**2*0.00324**2+((99.633963*(A[0][0]/(A[5][0]-A[0][0])**2))**2*(A[5][1])**2)+((99.633963*(A[5][0]/(A[0][0]-A[5][0])**2)))**2*(A[0][1])**2)+0.18
		f2=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*-5.775*10**(-7)*((99.84885*(A[1][0]/(A[5][0]-A[1][0])))-100))))*np.sqrt((A[1][0]/(A[5][0]-A[1][0]))**2*0.00324**2+((99.84885*(A[1][0]/(A[5][0]-A[1][0])**2))**2*(A[5][1])**2)+((99.84885*(A[5][0]/(A[1][0]-A[5][0])**2)))**2*(A[1][1])**2)+0.18
		f3=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*-5.775*10**(-7)*((99.6936*(A[2][0]/(A[5][0]-A[2][0])))-100))))*np.sqrt((A[2][0]/(A[5][0]-A[2][0]))**2*0.00324**2+((99.6936*(A[2][0]/(A[5][0]-A[2][0])**2))**2*(A[5][1])**2)+((99.6936*(A[5][0]/(A[2][0]-A[5][0])**2)))**2*(A[2][1])**2)+0.18
		f4=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*-5.775*10**(-7)*((99.46649*(A[3][0]/(A[5][0]-A[3][0])))-100))))*np.sqrt((A[3][0]/(A[5][0]-A[3][0]))**2*0.00324**2+((99.46649*(A[3][0]/(A[5][0]-A[3][0])**2))**2*(A[5][1])**2)+((99.46649*(A[5][0]/(A[3][0]-A[5][0])**2)))**2*(A[3][1])**2)+0.18
	
		T1=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(99.633963*(A[0][0]/(A[5][0]-A[0][0]))))))/(2*(-5.775*10**(-7)*100)))
		T2=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(99.84885*(A[1][0]/(A[5][0]-A[1][0]))))))/(2*(-5.775*10**(-7)*100)))
		T3=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(99.6936*(A[2][0]/(A[5][0]-A[2][0]))))))/(2*(-5.775*10**(-7)*100)))
		T4=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(99.46649*(A[3][0]/(A[5][0]-A[3][0]))))))/(2*(-5.775*10**(-7)*100)))

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

		if T1 >= 120:
			d.off()
			time.sleep(0.05)
			d.set_channel(1)
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


	def messurment_frequancy_cal(self, i):
		global how_many_times 
		how_many_times = i

	def messurment_frequancy(self, i):
		global how_often
		how_often = i


	def voltage_value(self, i):
		n = 0	
		global v_values
		v_values = np.array([])	
		while n<=how_many_times:
			a = int(i)/how_many_times
			v_values = np.append(v_values, int(a*n))	
			n+=1
		return v_values

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
	
	def index_changed_a_e(self, i):
		global gain_a_e
		gain = i
		if gain == 0:
			gain_a_e = 2
		elif gain == 1:
			gain_a_e = 1
		elif gain == 2:
			gain_a_e = 4
		elif gain == 3:
			gain_a_e = 8
		elif gain == 4:
			gain_a_e = 16

	def index_changed_b_e(self, i):
		global gain_b_e
		gain = i
		if gain == 0:
			gain_b_e = 2
		elif gain == 1:
			gain_b_e = 1
		elif gain == 2:
			gain_b_e = 4
		elif gain == 3:
			gain_b_e = 8
		elif gain == 4:
			gain_b_e = 16


	def index_changed_c_e(self, i):
		global gain_c_e
		gain = i
		if gain == 0:
			gain_c_e = 1
		elif gain == 1:
			gain_c_e = 2
		elif gain == 2:
			gain_c_e = 4
		elif gain == 3:
			gain_c_e = 8
		elif gain == 4:
			gain_c_e = 16



	def test_connection(self):
		try:
			data = [2,2,1,0]
			A = adc_main.main("-c", data)
			#self.set_text(A)
			self.widgetl00L5.setText("Pc und Pi \nsind verbunden")
		except:
			self.widgetl00L5.setText("Konnte keine Verbindung herstellen. \nStarte \"ads_main.py -s\" auf dem Pi \noder \"ads_main.py -c\" auf dem Pc")

	def set_data(self):
		try:
			data = [gain_a,gain_b,gain_c,0]
			A = adc_main.main("-c", data)
			self.widgetl00L6.setText("Neue Range wurde \nerfolgreich gesetzt")
			self.widgetl01L11.setText("Knopf drücken um Range zu ändern.\nAnsonsten wird die vorherige oder \ndie Standart Range verwendet")
			#self.widgetl00L5.setText("Verbindung hergestellt")
			#self.set_text(A)
		except:
			self.widgetl00L6.setText("Das setzen der Range hat nicht \nfunktioniert. Verbindung testen")

	def set_data2(self):
		try:
			data = [gain_a_e,gain_b_e,gain_c_e,0]
			A = adc_main.main("-c", data)
			self.widgetl01L11.setText("Neue Range wurde \nerfolgreich gesetzt")
			self.widgetl00L6.setText("Knopf drücken um Range zu ändern.\nAnsonsten wird die vorherige oder \ndie Standart Range verwendet")
			self.widgetl00L5.setText("Verbindung hergestellt")
			#self.set_text(A)
		except:
			self.widgetl01L11.setText("Das setzen der Range hat nicht \nfunktioniert. Verbindung testen")


	def start_kalibration(self):
		if np.size(v_values)<=0:
			self.widgetl01L10.setText("Messbereich einstellen!")
		else:
			dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
			dut.init()
			d = dut["PowerSupply"]
			d.set_channel(3)	
			d.on()

			#---------------Curve-Fit---------------#
			#define Function
			def func(x,m,n):
				return x*m+n

			if gain_a_e==1:
				namea=4.096
			elif gain_a_e==2:
				namea=2.048
			elif gain_a_e==4:
				namea=1.024
			elif gain_a_e==8:
				namea=0.512
			elif gain_a_e==16:
				namea=0.256

			if gain_b_e==1:
				nameb=4.096
			elif gain_b_e==2:
				nameb=2.048
			elif gain_b_e==4:
				nameb=1.024
			elif gain_b_e==8:
				nameb=0.512
			elif gain_b_e==16:
				nameb=0.256

			if gain_c_e==1:
				namec=4.096
			elif gain_c_e==2:
				namec=2.048
			elif gain_c_e==4:
				namec=1.024
			elif gain_c_e==8:
				namec=0.512
			elif gain_c_e==16:
				namec=0.256

			
			n = how_many_times

			datei = open("Kal/Kalibration_ADC1_%.3fV_ADC2_%.3fV_ADC3_%.3fV.txt"%(namea,nameb,namec),'w')

			for i in v_values:
					time.sleep(0.05)
					d.set_voltage(i/1000)
					time.sleep(0.5)
					data = [0,0,0,1]
					A = adc_main.main("-c", data)
					datei.write(str(A[0][0]) + '\t'+ str(A[0][1]) + '\t'+ str(A[0][2]) + '\t'+ str(A[0][3]) + '\t' + str(A[1][0]) + '\t'+ str(A[1][1]) + '\t'+ str(A[1][2]) + '\t'+ str(A[1][3]) +  '\t' + str(A[2][0]) + '\t'+ str(A[2][1]) + '\t'+ str(A[2][2]) + '\t'+ str(A[2][3]) + '\t' + str(A[3][0]) + '\t'+ str(A[3][1]) + '\t'+ str(A[3][2]) + '\t'+ str(A[3][3]) + '\t' + str(A[4][0]) + '\t' + str(A[4][1]) + '\t'+ str(A[4][2]) + '\t'+ str(A[4][3]) + '\t' + str(A[5][0]) + '\t'+ str(A[5][1]) + '\t'+ str(A[5][2]) + '\t'+ str(A[5][3]) + '\n')#+ str(A[6][0]) + '\t'+ str(A[6][1]) + '\t'+ str(A[6][2]) + '\t'+ str(A[6][3]) + '\t' + str(A[7][0]) + '\t'+ str(A[7][1]) + '\t'+ str(A[7][2]) + '\t'+ str(A[7][3]) + '\t' + str(A[8][0]) + '\t'+ str(A[8][1]) + '\t'+ str(A[8][2]) + '\t'+ str(A[8][3]) + '\t' + str(A[9][0]) + '\t'+ str(A[9][1]) + '\t'+ str(A[9][2]) + '\t'+ str(A[9][3]) + '\n')
					time.sleep(0.05)
			datei.close()

			datafile = np.loadtxt("Kal/Kalibration_ADC1_%.3fV_ADC2_%.3fV_ADC3_%.3fV.txt"%(namea,nameb,namec), delimiter='\t', unpack=True)

			run_new = 0

			for name in [namea,nameb,namec]:
				
				run = 0
				while run<2:

					A = datafile[(run+run_new*4)*4]
					B = datafile[2+(run+run_new*4)*4]
					dA = datafile[1+(run+run_new*4)*4]
					dB = datafile[3+(run+run_new*4)*4]	
	
					x = np.array([])
					for i in range(0,how_many_times+1):
						x = np.append(x,i)


					#curve-fit-program
					popt,pcov = curve_fit(func,B,A)
					errors = np.sqrt(np.diag(pcov))
					#print('Steigung: ' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5))+ '\t' + 'y-Achse: ' + str(popt[1].round(5)) + '+/-' + str(errors[1].round(5)))
					#print('Nochmal komplett: y=' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5)) + '*x+' + str(popt[1].round(5))+ '+/-' + str(errors[1].round(5)) + '\n')
					#datei.write(str(popt[0].round(5)) + '\t' + str(errors[0].round(5))+ '\t' + str(popt[1].round(5)) + '\t' + str(errors[1].round(5)) + '\n')

					#creat fit
					xlin = np.linspace(min(B), max(B),1000)
					ylin = func(xlin,popt[0],popt[1])

					#creat axis and draw function
					ax = plt.figure(dpi=350).add_subplot(1,1,1)

					plt.errorbar(B,A,xerr=dB,yerr=dA, color='royalblue',fmt='+',label='m = %s +/- %s \nn = %s +/- %s'%(str(popt[0].round(5)),str(errors[0].round(5)),str(popt[1].round(5)),str(errors[1].round(5))))
					plt.plot(xlin,ylin,color='firebrick', label='Fit-Gerade',lw=1.2)
	
					plt.xlabel('ADC Values')
					plt.ylabel('Volt/V')
					plt.grid(True, which='minor',linestyle='--', color='darkgray', lw=0.5)
					plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
					plt.legend(loc='best')	
					plt.tight_layout()
					#plt.savefig('./Bilder%.3f/ADC%dchannal%d'%(name,run_new+1,run+1))
					print(run,run_new,name)
					if run==0:
						plt.savefig('./Bilder%.3f/ADC%dchannal%d_gegen_channal%d'%(name,run_new+1,run+1,run+2))
					else:
						plt.savefig('./Bilder%.3f/ADC%dchannal%d_gegen_channal%d'%(name,run_new+1,run+2,run+3))
					run += 1
				run_new += 1
			d.off()
			self.widgetl01L10.setText("Energie Kalibration abgeschlossen!")

	
	def start_messurment(self):
		global messurment_run
		go = 0
		datei = open('Vorordner/Messung%s_%s.txt'%(messurment_run,serial_number),'w')
		datei1 = open('Vorordner/Vollständige_Temp_Kurve_.txt','a')
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

			#datei.write(str(A[0][0]) + '\t' + str(A[0][1]) + '\t' + str(round(omega0,2)) + '\t' + str(round(gaus0,2)) + '\t' + str(A[1][0]) + '\t' + str(A[1][1]) + '\t' + str(round(omega1,2)) + '\t' + str(round(gaus1,2)) + '\t' + str(A[2][0]) + '\t' + str(A[2][1]) + '\t' + str(round(omega2,2)) + '\t' + str(round(gaus2,2))+ '\t' + str(A[3][0]) + '\t' + str(A[3][1]) + '\t' + str(round(omega3,2)) + '\t' + str(round(gaus3,2))+ '\t' + str(A[4][0]) + '\t' + str(A[4][1]) + '\t' + str(A[5][0]) + '\t' + str(A[5][1]) + '\n')
			#datei.write(str(round(((100*(A[0][0]/(A[5][0]-A[0][0])))-99.954)/0.39087,2))+'\t'+str(round(np.sqrt((((100*(A[0][0]/(A[5][0]-A[0][0])))-99.954)/0.39087**2)**2*0.00049**2+(1/0.39087)**2*0.1364**2+(1/0.39087*(330/(A[0][0]-A[5][0])**2))**2*A[0][1]**2+(1/0.39087*(100*(A[0][0]/(A[5][0]-A[0][0])**2)))**2*A[5][1]**2),2))+'\t'+str(round(((100*(A[1][0]/(A[5][0]-A[1][0])))-99.954)/0.39087,2))+'\t'+str(round(np.sqrt((((100*(A[1][0]/(A[5][0]-A[1][0])))-99.954)/0.39087**2)**2*0.00049**2+(1/0.39087)**2*0.1364**2+(1/0.39087*(330/(A[1][0]-A[5][0])**2))**2*A[1][1]**2+(1/0.39087*(100*(A[1][0]/(A[5][0]-A[1][0])**2)))**2*A[5][1]**2),2))+'\t'+str(round(((100*(A[2][0]/(A[5][0]-A[2][0])))-99.954)/0.39087,2))+'\t'+str(round(np.sqrt((((100*(A[2][0]/(A[5][0]-A[2][0])))-99.954)/0.39087**2)**2*0.00049**2+(1/0.39087)**2*0.1364**2+(1/0.39087*(330/(A[2][0]-A[5][0])**2))**2*A[2][1]**2+(1/0.39087*(100*(A[2][0]/(A[5][0]-A[2][0])**2)))**2*A[5][1]**2),2))+'\t'+str(round(((100*(A[3][0]/(A[5][0]-A[3][0])))-99.954)/0.39087,2))+'\t'+str(round(np.sqrt((((100*(A[3][0]/(A[5][0]-A[3][0])))-99.954)/0.39087**2)**2*0.00049**2+(1/0.39087)**2*0.1364**2+(1/0.39087*(330/(A[3][0]-A[5][0])**2))**2*A[3][1]**2+(1/0.39087*(100*(A[3][0]/(A[5][0]-A[3][0])**2)))**2*A[5][1]**2),2))+'\t'+str(round(((A[4][0]*1000-1.556)/2.318),3))+'\t'+str(round((np.sqrt((1/2.318)**2*(A[4][1]*1000)**2+(A[4][0]*1000/2.318**2)**2*0.0169**2+(1/2.318)**2*0.03032**2)),3))+'\t'+str(round(((100.059*(A[0][0]/(A[5][0]-A[0][0])))-(100.14*(A[1][0]/(A[5][0]-A[1][0]))))/(float(cur)*float(vol)),5))+'\t'+str(round(((100.14*(A[1][0]/(A[5][0]-A[1][0])))-(100.117*(A[2][0]/(A[5][0]-A[2][0]))))/(float(cur)*float(vol)),5))+'\t'+str(round(((100.117*(A[2][0]/(A[5][0]-A[2][0])))-(99.889*(A[3][0]/(A[5][0]-A[3][0]))))/(float(cur)*float(vol)),5))+'\n')

			f1=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*(-5.775*10**(-7))*((99.633963*(A[0][0]/(A[5][0]-A[0][0])))-100))))*np.sqrt((A[0][0]/(A[5][0]-A[0][0]))**2*0.00324**2+((99.633963*(A[0][0]/(A[5][0]-A[0][0])**2))**2*(A[5][1])**2)+((99.633963*(A[5][0]/(A[0][0]-A[5][0])**2)))**2*(A[0][1])**2)+0.18
			f2=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*-5.775*10**(-7)*((99.84885*(A[1][0]/(A[5][0]-A[1][0])))-100))))*np.sqrt((A[1][0]/(A[5][0]-A[1][0]))**2*0.00324**2+((99.84885*(A[1][0]/(A[5][0]-A[1][0])**2))**2*(A[5][1])**2)+((99.84885*(A[5][0]/(A[1][0]-A[5][0])**2)))**2*(A[1][1])**2)+0.18
			f3=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*-5.775*10**(-7)*((99.6936*(A[2][0]/(A[5][0]-A[2][0])))-100))))*np.sqrt((A[2][0]/(A[5][0]-A[2][0]))**2*0.00324**2+((99.6936*(A[2][0]/(A[5][0]-A[2][0])**2))**2*(A[5][1])**2)+((99.6936*(A[5][0]/(A[2][0]-A[5][0])**2)))**2*(A[2][1])**2)+0.18
			f4=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*-5.775*10**(-7)*((99.46649*(A[3][0]/(A[5][0]-A[3][0])))-100))))*np.sqrt((A[3][0]/(A[5][0]-A[3][0]))**2*0.00324**2+((99.46649*(A[3][0]/(A[5][0]-A[3][0])**2))**2*(A[5][1])**2)+((99.46649*(A[5][0]/(A[3][0]-A[5][0])**2)))**2*(A[3][1])**2)+0.18
	
			T1=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(99.633963*(A[0][0]/(A[5][0]-A[0][0]))))))/(2*(-5.775*10**(-7)*100)))
			T2=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(99.84885*(A[1][0]/(A[5][0]-A[1][0]))))))/(2*(-5.775*10**(-7)*100)))
			T3=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(99.6936*(A[2][0]/(A[5][0]-A[2][0]))))))/(2*(-5.775*10**(-7)*100)))
			T4=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(99.46649*(A[3][0]/(A[5][0]-A[3][0]))))))/(2*(-5.775*10**(-7)*100)))

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

			self.set_text(A)
			time.sleep(1)
			go += 1

		datei1.close()
		datei.close()

		#---------------Curve-Fit---------------#
		#define Function
		def func(x,m,n):
			return x*m+n

		#get data(every 15 pairs off data the channal changes to the next. So there are 15 pairs of achan0 data and than 15 of achan1 and so on)
		datafile = np.loadtxt('Vorordner/Messung%s_%s.txt'%(messurment_run,serial_number), delimiter='\t', unpack=True)
		a,da,b,db,c,dc,d,dd = 0,1,2,3,4,5,6,7
		A,dA,B,dB,C,dC,D,dD = datafile[a],datafile[da],datafile[b],datafile[db],datafile[c],datafile[dc],datafile[d],datafile[dd]


		x = np.array([])
		for i in range(0,len(A)):
			x = np.append(x,i)

		#curve-fit-program
		#popt,pcov = curve_fit(func,x,A*1000)
		#errors = np.sqrt(np.diag(pcov))
		#print('Steigung: ' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5))+ '\n' + 'y-Achse: ' + str(popt[1].round(5)) + '+/-' + str(errors[1].round(5)))
		#print('Nochmal komplett: y=' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5)) + '*x+' + str(popt[1].round(5))+ '+/-' + str(errors[1].round(5)))

		#creat fit
		#xlin = np.linspace(min(x),max(x),1000)
		#ylin = func(xlin,popt[0],popt[1])

		#creat axis and draw function
		ax = plt.figure(dpi=350).add_subplot(1,1,1)
		#ax.set_facecolor('gainsboro')
		plt.errorbar(x,A,yerr=dA, color='royalblue',fmt='.',label='Temperatur oben')
		plt.errorbar(x,B,yerr=dB, color='firebrick',fmt='.',label='Temperatur mitte oben')
		plt.errorbar(x,C,yerr=dC, color='yellow',fmt='.',label='Temperatur mitte unten')
		plt.errorbar(x,D,yerr=dD, color='orangered',fmt='.',label='Temperatur unten')
		#plt.errorbar(x,(E+1.7), color='navy',fmt='+',label='Channel 1b')
		#plt.plot(xlin,ylin,color='firebrick', label='Fit-Gerade',lw=1.2)

		plt.xlabel('Datenpunkt/0.5s')
		plt.ylabel('Temperatur / °C')
		plt.legend(loc='best')
		plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
		plt.tight_layout()
		plt.savefig('Vorordner/Messung%s_%s.png'%(messurment_run,serial_number))
		#plt.show()

		datei = open('Vorordner/Gemittelte_Werte_%s.txt'%(serial_number),'a')

		lam1,lam2,lam3=datafile[10],datafile[12],datafile[14]
		var_lam1,var_lam2,var_lam3=datafile[11],datafile[13],datafile[15]
		weigth,dweigth=datafile[8],datafile[9]
		lambda1=np.sum(lam1/var_lam1**2)/np.sum(1/var_lam1**2)
		lambda2=np.sum(lam2/var_lam2**2)/np.sum(1/var_lam2**2)
		lambda3=np.sum(lam3/var_lam3**2)/np.sum(1/var_lam3**2)
		self.widgetl10L10.setText(str(round(lambda1,2))+'\t'+str(round(np.sqrt(1/np.sum(1/var_lam1**2)),2)))
		self.widgetl10L11.setText(str(round(lambda2,2))+'\t'+str(round(np.sqrt(1/np.sum(1/var_lam2**2)),2)))
		self.widgetl10L12.setText(str(round(lambda3,2))+'\t'+str(round(np.sqrt(1/np.sum(1/var_lam3**2)),2)))
		
		datei.write(str(weigth[1])+'\t'+str(dweigth[1])
		+'\t'+str((lambda1))+'\t'+str((np.sqrt(1/np.sum(1/var_lam1**2))))
		+'\t'+str((lambda2))+'\t'+str((np.sqrt(1/np.sum(1/var_lam2**2))))
		+'\t'+str((lambda3))+'\t'+str((np.sqrt(1/np.sum(1/var_lam3**2))))
		+'\n')

		datei.close()

		datafile = np.loadtxt('Vorordner/Vollständige_Temp_Kurve_.txt', delimiter='\t', unpack=True)
		a,da,b,db,c,dc,d,dd = 0,1,2,3,4,5,6,7
		A,dA,B,dB,C,dC,D,dD = datafile[a],datafile[da],datafile[b],datafile[db],datafile[c],datafile[dc],datafile[d],datafile[dd]


		x = np.array([])
		for i in range(0,len(A)):
			x = np.append(x,i)

		#curve-fit-program
		#popt,pcov = curve_fit(func,x,A*1000)
		#errors = np.sqrt(np.diag(pcov))
		#print('Steigung: ' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5))+ '\n' + 'y-Achse: ' + str(popt[1].round(5)) + '+/-' + str(errors[1].round(5)))
		#print('Nochmal komplett: y=' + str(popt[0].round(5)) + '+/-' + str(errors[0].round(5)) + '*x+' + str(popt[1].round(5))+ '+/-' + str(errors[1].round(5)))

		#creat fit
		#xlin = np.linspace(min(x),max(x),1000)
		#ylin = func(xlin,popt[0],popt[1])

		#creat axis and draw function
		ax = plt.figure(dpi=350).add_subplot(1,1,1)
		#ax.set_facecolor('gainsboro')
		plt.errorbar(x,A,yerr=dA, color='royalblue',fmt='-',label='Temperatur oben')
		plt.errorbar(x,B,yerr=dB, color='firebrick',fmt='-',label='Temperatur mitte oben')
		plt.errorbar(x,C,yerr=dC, color='yellow',fmt='-',label='Temperatur mitte unten')
		plt.errorbar(x,D,yerr=dD, color='orangered',fmt='-',label='Temperatur unten')
		#plt.errorbar(x,(E+1.7), color='navy',fmt='+',label='Channel 1b')
		#plt.plot(xlin,ylin,color='firebrick', label='Fit-Gerade',lw=1.2)

		plt.xlabel('Datenpunkt / 2s')
		plt.ylabel('Temperatur / °C')
		plt.legend(loc='best')
		plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
		plt.tight_layout()
		plt.savefig('Vorordner/Vollständige_Temp_Kurve_%s.png'%(serial_number))

		messurment_run += 1
		self.widgetl00L7.setText("Messung erfolgreich Beendet")

	def set_text(self,A):
		dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
		dut.init()
		d = dut["PowerSupply"]
		d.set_channel(2)
		time.sleep(0.05)
		vol = d.get_voltage()
		time.sleep(0.05)
		cur = d.get_current()

		####Fehler####
		f1=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*(-5.775*10**(-7))*((99.633963*(A[0][0]/(A[5][0]-A[0][0])))-100))))*np.sqrt((A[0][0]/(A[5][0]-A[0][0]))**2*0.00324**2+((99.633963*(A[0][0]/(A[5][0]-A[0][0])**2))**2*(A[5][1])**2)+((99.633963*(A[5][0]/(A[0][0]-A[5][0])**2)))**2*(A[0][1])**2)+0.18
		f2=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*-5.775*10**(-7)*((99.84885*(A[1][0]/(A[5][0]-A[1][0])))-100))))*np.sqrt((A[1][0]/(A[5][0]-A[1][0]))**2*0.00324**2+((99.84885*(A[1][0]/(A[5][0]-A[1][0])**2))**2*(A[5][1])**2)+((99.84885*(A[5][0]/(A[1][0]-A[5][0])**2)))**2*(A[1][1])**2)+0.18
		f3=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*-5.775*10**(-7)*((99.6936*(A[2][0]/(A[5][0]-A[2][0])))-100))))*np.sqrt((A[2][0]/(A[5][0]-A[2][0]))**2*0.00324**2+((99.6936*(A[2][0]/(A[5][0]-A[2][0])**2))**2*(A[5][1])**2)+((99.6936*(A[5][0]/(A[2][0]-A[5][0])**2)))**2*(A[2][1])**2)+0.18
		f4=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*-5.775*10**(-7)*((99.46649*(A[3][0]/(A[5][0]-A[3][0])))-100))))*np.sqrt((A[3][0]/(A[5][0]-A[3][0]))**2*0.00324**2+((99.46649*(A[3][0]/(A[5][0]-A[3][0])**2))**2*(A[5][1])**2)+((99.46649*(A[5][0]/(A[3][0]-A[5][0])**2)))**2*(A[3][1])**2)+0.18
	
		T1=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(99.633963*(A[0][0]/(A[5][0]-A[0][0]))))))/(2*(-5.775*10**(-7)*100)))
		T2=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(99.84885*(A[1][0]/(A[5][0]-A[1][0]))))))/(2*(-5.775*10**(-7)*100)))
		T3=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(99.6936*(A[2][0]/(A[5][0]-A[2][0]))))))/(2*(-5.775*10**(-7)*100)))
		T4=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(99.46649*(A[3][0]/(A[5][0]-A[3][0]))))))/(2*(-5.775*10**(-7)*100)))

		#datei.write(str(round(T1,4))+'\t'+str(round(f1,4))
		#+'\t'+str(round(T2,4))+'\t'+str(round(f2,4))
		#+'\t'+str(round(T3,4))+'\t'+str(round(f3,4))
		#+'\t'+str(round(T4,4))+'\t'+str(round(f4,4))
		#+'\t'+str(round(((A[4][0]*1000-1.55639)/2.31754),2))+'\t'+str(round((np.sqrt((1/2.31754)**2*(A[4][1]*1000)**2+(A[4][0]*1000/2.31754**2)**2*0.01692**2+(1/2.31754)**2*0.4216**2)),2))
		#+'\t'+str(round((float(cur)*float(vol))/(T1-T2)*0.05/(0.0001*np.pi),5))+'\t'+str(round(np.sqrt(((float(cur)*float(vol))/(T1-T2)**2*0.05/(0.0001*np.pi))**2*(f1**2+f2**2)),5))
		#+'\t'+str(round((float(cur)*float(vol))/(T2-T3)*0.0076/(0.0001*np.pi),5))+'\t'+str(round(np.sqrt(((float(cur)*float(vol))/(T2-T3)**2*0.0076/(0.0001*np.pi))**2*(f2**2+f3**2)),5))
		#+'\t'+str(round((float(cur)*float(vol))/(T3-T4)*0.05/(0.0001*np.pi),5))+'\t'+str(round(np.sqrt(((float(cur)*float(vol))/(T3-T4)**2*0.05/(0.0001*np.pi))**2*(f3**2+f4**2)),5))
		#+'\n')


		self.widgetl10L1.setText(str(round(T1,4))+'\t'+str(round(f1,4)))
		self.widgetl10L2.setText(str(round(T2,4))+'\t'+str(round(f2,4)))
		self.widgetl10L3.setText(str(round(T3,4))+'\t'+str(round(f3,4)))
		self.widgetl10L4.setText(str(round(T4,4))+'\t'+str(round(f4,4)))
		self.widgetl10L5.setText(str(round(((A[4][0]*1000-1.55639)/2.31754),2))+'\t'+str(round((np.sqrt((1/2.31754)**2*(A[4][1]*1000)**2+(A[4][0]*1000/2.31754**2)**2*0.01692**2+(1/2.31754)**2*0.4216**2)),2)))
		self.widgetl10L6.setText(str(round(A[5][0],6))+'\t'+str(round(A[5][1],6)))
		#self.widgetl10L6.setText(str(round(((A[4][0]*1000-2.21505)/2.33586),2)))
		self.widgetl10L7.setText(str(round((float(cur)*float(vol))/(T1-T2)*0.05/(0.0001*np.pi),5))+'\t'+str(round(np.sqrt(((float(cur)*float(vol))/(T1-T2)**2*0.05/(0.0001*np.pi))**2*(f1**2+f2**2)+(float(cur)/(T1-T2)*0.05/(0.0001*np.pi))**2*0.005**2+(float(vol)/(T1-T2)*0.05/(0.0001*np.pi))**2*0.0005**2+(((float(cur)*float(vol))/(T3-T4)*1/(0.0001*np.pi))**2*0.004**2)),5)))
		self.widgetl10L8.setText(str(round((float(cur)*float(vol))/(T2-T3)*thick/(0.0001*np.pi),5))+'\t'+str(round(np.sqrt(((float(cur)*float(vol))/(T2-T3)**2*thick/(0.0001*np.pi))**2*(f2**2+f3**2)+(float(cur)/(T2-T3)*thick/(0.0001*np.pi))**2*0.005**2+(float(vol)/(T2-T3)*thick/(0.0001*np.pi))**2*0.0005**2+(((float(cur)*float(vol))/(T2-T3)*1/(0.0001*np.pi))**2*0.0001**2)),5)))
		self.widgetl10L9.setText(str(round((float(cur)*float(vol))/(T3-T4)*0.05/(0.0001*np.pi),5))+'\t'+str(round(np.sqrt(((float(cur)*float(vol))/(T3-T4)**2*0.05/(0.0001*np.pi))**2*(f3**2+f4**2)+(float(cur)/(T3-T4)*0.05/(0.0001*np.pi))**2*0.005**2+(float(vol)/(T3-T4)*0.05/(0.0001*np.pi))**2*0.0005**2+(((float(cur)*float(vol))/(T3-T4)*1/(0.0001*np.pi))**2*0.004**2)),5)))
		#self.widgetl10L10.setText(str(A[9]))
		###Fehler von lambda###
		#print(str(round(np.sqrt(((float(cur)*float(vol))/((((99.633963*(A[0][0]/(A[5][0]-A[0][0])))-99.954)/0.39087)-(((99.84885*(A[1][0]/(A[5][0]-A[1][0])))-99.954)/0.39087))**2*0.05/(0.0001*np.pi))**2*(((np.sqrt((((99.633963*(A[0][0]/(A[5][0]-A[0][0])))-99.954)/0.39087**2)**2*0.00049**2+(1/0.39087)**2*0.1364**2+(1/0.39087*(330/(A[0][0]-A[5][0])**2))**2*A[0][1]**2+(1/0.39087*(99.633963*(A[0][0]/(A[5][0]-A[0][0])**2)))**2*A[5][1]**2)+((A[0][0]/(A[5][0]-A[0][0]))/0.39087)**2*0.00324)**2)+(np.sqrt((((99.84885*(A[1][0]/(A[5][0]-A[1][0])))-99.954)/0.39087**2)**2*0.00049**2+(1/0.39087)**2*0.1364**2+(1/0.39087*(330/(A[1][0]-A[5][0])**2))**2*A[1][1]**2+(1/0.39087*(99.84885*(A[1][0]/(A[5][0]-A[1][0])**2)))**2*A[5][1]**2)+((A[0][0]/(A[5][0]-A[0][0]))/0.39087)**2*0.00324)**2)),2)))
		#print(str(round(np.sqrt(((float(cur)*float(vol))/((((99.84885*(A[1][0]/(A[5][0]-A[1][0])))-99.954)/0.39087)-(((99.6936*(A[2][0]/(A[5][0]-A[2][0])))-99.954)/0.39087))**2*0.0076/(0.0001*np.pi))**2*((np.sqrt((((99.84885*(A[1][0]/(A[5][0]-A[1][0])))-99.954)/0.39087**2)**2*0.00049**2+(1/0.39087)**2*0.1364**2+(1/0.39087*(330/(A[1][0]-A[5][0])**2))**2*A[1][1]**2+(1/0.39087*(99.84885*(A[1][0]/(A[5][0]-A[1][0])**2)))**2*A[5][1]**2)+((A[0][0]/(A[5][0]-A[0][0]))/0.39087)**2*0.00324)**2+(np.sqrt((((99.6936*(A[2][0]/(A[5][0]-A[2][0])))-99.954)/0.39087**2)**2*0.00049**2+(1/0.39087)**2*0.1364**2+(1/0.39087*(330/(A[2][0]-A[5][0])**2))**2*A[2][1]**2+(1/0.39087*(99.6936*(A[2][0]/(A[5][0]-A[2][0])**2)))**2*A[5][1]**2)+((A[0][0]/(A[5][0]-A[0][0]))/0.39087)**2*0.00324)**2)),2)))
		#print(str(round(np.sqrt(((float(cur)*float(vol))/((((99.6936*(A[2][0]/(A[5][0]-A[2][0])))-99.954)/0.39087)-(((99.46649*(A[3][0]/(A[5][0]-A[3][0])))-99.954)/0.39087))**2*0.05/(0.0001*np.pi))**2*((np.sqrt((((99.6936*(A[2][0]/(A[5][0]-A[2][0])))-99.954)/0.39087**2)**2*0.00049**2+(1/0.39087)**2*0.1364**2+(1/0.39087*(330/(A[2][0]-A[5][0])**2))**2*A[2][1]**2+(1/0.39087*(99.6936*(A[2][0]/(A[5][0]-A[2][0])**2)))**2*A[5][1]**2)+((A[0][0]/(A[5][0]-A[0][0]))/0.39087)**2*0.00324)**2+(np.sqrt((((99.46649*(A[3][0]/(A[5][0]-A[3][0])))-99.954)/0.39087**2)**2*0.00049**2+(1/0.39087)**2*0.1364**2+(1/0.39087*(330/(A[3][0]-A[5][0])**2))**2*A[3][1]**2+(1/0.39087*(99.46649*(A[3][0]/(A[5][0]-A[3][0])**2)))**2*A[5][1]**2)+((A[0][0]/(A[5][0]-A[0][0]))/0.39087)**2*0.00324)**2)),2)))
		#print(str(round(1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*(-5.775*10**(-7))*((99.633963*(A[0][0]/(A[5][0]-A[0][0])))-100))))*np.sqrt((A[0][0]/(A[5][0]-A[0][0]))**2*0.00324**2+((99.633963*(A[0][0]/(A[5][0]-A[0][0])**2))**2*(A[5][1])**2)+((99.633963*(A[5][0]/(A[0][0]-A[5][0])**2)))**2*(A[0][1])**2),4)))
		#print(str(round(1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*-5.775*10**(-7)*((99.84885*(A[1][0]/(A[5][0]-A[1][0])))-100))))*np.sqrt((A[1][0]/(A[5][0]-A[1][0]))**2*0.00324**2+((99.84885*(A[1][0]/(A[5][0]-A[1][0])**2))**2*(A[5][1])**2)+((99.84885*(A[5][0]/(A[1][0]-A[5][0])**2)))**2*(A[1][1])**2),4)))
		#print(str(round(1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*-5.775*10**(-7)*((99.6936*(A[2][0]/(A[5][0]-A[2][0])))-100))))*np.sqrt((A[2][0]/(A[5][0]-A[2][0]))**2*0.00324**2+((99.6936*(A[2][0]/(A[5][0]-A[2][0])**2))**2*(A[5][1])**2)+((99.6936*(A[5][0]/(A[2][0]-A[5][0])**2)))**2*(A[2][1])**2),4)))
		#print(str(round(1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*-5.775*10**(-7)*((99.46649*(A[3][0]/(A[5][0]-A[3][0])))-100))))*np.sqrt((A[3][0]/(A[5][0]-A[3][0]))**2*0.00324**2+((99.46649*(A[3][0]/(A[5][0]-A[3][0])**2))**2*(A[5][1])**2)+((99.46649*(A[5][0]/(A[3][0]-A[5][0])**2)))**2*(A[3][1])**2),4)))
		
		self.widgetl10L13.setText(str(round((T1-T2)*np.pi/(float(cur)*float(vol)),5))+'\t'+str(round(np.sqrt(1/(float(cur)*float(vol))**2*(f1**2+f2**2)),5)))
		self.widgetl10L14.setText(str(round((T2-T3)*np.pi/(float(cur)*float(vol)),5))+'\t'+str(round(np.sqrt(1/(float(cur)*float(vol))**2*(f1**2+f2**2)),5)))
		self.widgetl10L15.setText(str(round((T3-T4)*np.pi/(float(cur)*float(vol)),5))+'\t'+str(round(np.sqrt(1/(float(cur)*float(vol))**2*(f1**2+f2**2)),5)))
		self.widgetl10L16.setText(str(round((T2-T3)*np.pi/(float(cur)*float(vol))-0.0074/0.05*(T1-T2)*np.pi/(float(cur)*float(vol)),5)))

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
