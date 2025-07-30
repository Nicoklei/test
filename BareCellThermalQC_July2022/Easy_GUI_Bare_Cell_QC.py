import numpy as np
import time
from PyQt5.QtWidgets import(QApplication, QCheckBox, QComboBox, QDateEdit, QDateTimeEdit, QDial, QDoubleSpinBox, QFontComboBox, QLabel, QLCDNumber, QLineEdit, QMainWindow, QProgressBar, QPushButton, QRadioButton, QSlider, QSpinBox, QTimeEdit, QVBoxLayout,QHBoxLayout,QGridLayout,QStackedLayout, QWidget, QDialog, QDialogButtonBox)
import pyqtgraph as pg
from matplotlib import pyplot as plt
import sys
import adc_main, adc_utils
from basil.dut import Dut
from PyQt5.QtCore import pyqtSlot,QRunnable,QThreadPool, QObject, pyqtSignal
import os
import shutil


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
		general_layout = QGridLayout()

		#sector 00
		general_layout_sector_00 = QVBoxLayout()
		start_peltier_layout = QHBoxLayout()
		start_spirale_layout = QHBoxLayout()
		thickness_change_layout = QHBoxLayout()
		name_change_layout = QHBoxLayout()
		test_21_layout = QHBoxLayout()

		#sector 10
		general_layout_sector_10 = QVBoxLayout()
		weight_on_cell_layout = QHBoxLayout()

		#sector 01
		general_layout_sector_01 = QVBoxLayout()

		#sector 11
		general_layout_sector_11 = QVBoxLayout()

		#Variables
		self.bare_cell_thickness = 0.0074+0.0018
		self.serial_number = 0
		self.measurment_run = 0
		self.values_graph1 = np.array([])
		self.values_graph2 = np.array([])
		self.values_graph3 = np.array([])
		self.values_graph4 = np.array([])
		self.x_values_graph = np.array([])
		self.measurment_run_extra = 0
		self.TFM_test_21 = 0.00
		self.prev_serial_number = 0
		self.start_messurment_var = 0
		self.start_test_21_var = 0
		self.spirale_status = 0
		self.peltier_status = 0

		##without hardware comment out##
		# data = [2,2,1,0]
		# A = adc_main.main("-c", data)

		# dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
		# dut.init()
		# d = dut["PowerSupply"]
		# d.set_channel(1)
		# time.sleep(0.05)
		# vol = d.get_target_voltage()
		
		# d.set_channel(2)
		# time.sleep(0.05)
		# vol = d.get_target_voltage()
		##without hardware comment out until here##

		#--------------add Widgets--------------#
		####sector00####

		## Changing Labels
		self.widgetl00L1 = QLabel("Starte Peltier-Element")
		self.widgetl00L2 = QLabel("Starte Heizspirale")
		self.widgetl00L3 = QLabel("Aktuelle Spannung: 0.000")
		self.widgetl00L4 = QLabel("Aktuelle Spannung: 0.000")
		self.widgetl00L5 = QLabel("Pc und Pi \nsind verbunden")
		self.widgetl00L7 = QLabel()
		self.widgetl00L8 = QLabel("Aktueller Strom: 0.000")
		self.widgetl00L9 = QLabel("Aktueller Strom: 0.000")
		self.widgetl00L10 = QLabel()
		self.widgetl00L17 = QLabel()

		## Not changing Labels
		widgetl00L1 = QLabel("Bare Cell QC Setup Auslesesystem")
		widgetl00L6 = QLabel("Dicke des Materials \nzwischen Aluminium Stäben:")
		widgetl00L7 = QLabel("Name Testobjekt:")
		widgetl00L8 = QLabel("Peltier-Element Steuerung")
		widgetl00L9 = QLabel("Heizspirale Steuerung")
		widgetl00L10 = QLabel("Einstellungen zur Messung eines DUT")
		widgetl00L11 = QLabel("Messungen")	
		widgetl00L12 = QLabel("Vergleichstest 21 starten\noder Vergleichswert eingeben:")		
		widgetl00L5 = QLabel("Gewicht auf Device / kg:")

		## Buttons
		self.widgetPB2 = QPushButton("Messung Starten")
		self.widgetPB10 = QPushButton("Messreihe weiterführen und gleichen Ordner weiterverwenden")
		self.widgetPB11 = QPushButton("Graph Leeren")
		self.widgetPB12 = QPushButton("Programm starten")
		self.widgetPB13 = QPushButton("Vergleichstest 21 starten")

		## Other functions
		widget00DSB3 = QDoubleSpinBox()
		self.widget00DSB4 = QDoubleSpinBox()

		self.widget00ChB1 = QCheckBox()
		self.widget00ChB2 = QCheckBox()

		widget00LE1 = QLineEdit()
			

		####sector10####


		####sector01####

		## Functions to plot the graph
		self.widget01G = pg.PlotWidget()
		self.widget01G.setBackground('w')
		self.widget01G.addLegend()
		self.widget01G.showGrid(x=True, y=True)

		####sector11####

				
		#-------add functions to Widgets-------# 
		####sector00####
		font6 = widgetl00L8.font()
		font6.setPointSize(11)
		font10 = widgetl00L1.font()
		font10.setPointSize(15)
		widgetl00L1.setFont(font10)
		widgetl00L8.setFont(font6)
		widgetl00L9.setFont(font6)
		widgetl00L10.setFont(font6)
		widgetl00L11.setFont(font6)
		widgetl00L5.setFont(font6)
		self.widgetl00L10.setFont(font6)
  
		font11 = self.widgetl00L7.font()
		font11.setPointSize(12)
		self.widgetl00L7.setFont(font11)

		self.widgetPB2.clicked.connect(self.start_messurment)
		self.widgetPB10.clicked.connect(self.new_messurment_series)
		self.widgetPB11.clicked.connect(self.clear_graph)
		self.widgetPB12.clicked.connect(self.start_program)
		self.widgetPB13.clicked.connect(self.start_test_21)

		widget00DSB3.valueChanged.connect(self.thickness)
		widget00DSB3.setValue(1.80)
		widget00DSB3.setSuffix("mm")
		self.widget00DSB4.setMinimum(0.00)
		self.widget00DSB4.setMaximum(4.00)
		self.widget00DSB4.valueChanged.connect(self.TFM_comparison)
		self.widget00DSB4.setSuffix("cm²K/W")

		self.widget00ChB1.stateChanged.connect(self.on_off_peltier)
		self.widget00ChB2.stateChanged.connect(self.on_off_spirale)

		widget00LE1.textEdited.connect(self.text_edited)

		font7 = self.widgetl00L17.font()
		font7.setPointSize(18)
		self.widgetl00L17.setFont(font7)

		####sector10####

		####sector01####

		####sector11####


		#---------add Widgets into Layouts---------#
		#sector00
		general_layout_sector_00.addWidget(widgetl00L1)

		general_layout_sector_00.addWidget(self.widgetPB12)
  
		general_layout_sector_00.addWidget(widgetl00L8)
		widgetl00L8.setContentsMargins(0,8,0,0)
		start_peltier_layout.addWidget(self.widgetl00L1)
		start_peltier_layout.addWidget(self.widget00ChB1)
		general_layout_sector_00.addLayout(start_peltier_layout)

		general_layout_sector_00.addWidget(self.widgetl00L3)

		general_layout_sector_00.addWidget(self.widgetl00L8)

		general_layout_sector_00.addWidget(widgetl00L9)
		widgetl00L9.setContentsMargins(0,8,0,0)
		start_spirale_layout.addWidget(self.widgetl00L2)
		start_spirale_layout.addWidget(self.widget00ChB2)
		general_layout_sector_00.addLayout(start_spirale_layout)

		general_layout_sector_00.addWidget(self.widgetl00L4)

		general_layout_sector_00.addWidget(self.widgetl00L9)

		general_layout_sector_00.addWidget(widgetl00L10)
		widgetl00L10.setContentsMargins(0,8,0,0)
		thickness_change_layout.addWidget(widgetl00L6)
		thickness_change_layout.addWidget(widget00DSB3)
		general_layout_sector_00.addLayout(thickness_change_layout)

		name_change_layout.addWidget(widgetl00L7)
		name_change_layout.addWidget(widget00LE1)
		general_layout_sector_00.addLayout(name_change_layout)

		general_layout_sector_00.addWidget(self.widgetPB10)
		general_layout_sector_00.addWidget(self.widgetPB11)

		general_layout_sector_00.addWidget(widgetl00L11)
		widgetl00L11.setContentsMargins(0,8,0,0)

		test_21_layout.addWidget(widgetl00L12)
		test_21_layout.addWidget(self.widgetPB13)
		test_21_layout.addWidget(self.widget00DSB4)
		general_layout_sector_00.addLayout(test_21_layout)

		general_layout_sector_00.addWidget(self.widgetPB2)
		general_layout_sector_00.addWidget(self.widgetl00L7)

		weight_on_cell_layout.addWidget(widgetl00L5)
		weight_on_cell_layout.addWidget(self.widgetl00L10)
		weight_on_cell_layout.setContentsMargins(0,8,0,0)
		general_layout_sector_00.addLayout(weight_on_cell_layout)

		general_layout_sector_00.addWidget(self.widgetl00L17)
	
		#sector10


		#sector01
		general_layout_sector_01.addWidget(self.widget01G)


		#sector11
		

		#----------add Layouts into Grid----------#
	
		general_layout.addLayout(general_layout_sector_00, 0, 0)
		general_layout.addLayout(general_layout_sector_10, 1, 0)
		general_layout.addLayout(general_layout_sector_01, 0, 1)
		general_layout.addLayout(general_layout_sector_11, 1, 1)

		general_layout_sector_00.setContentsMargins(0,0,0,0)
		general_layout_sector_10.setContentsMargins(0,0,0,0)
		general_layout_sector_01.setContentsMargins(0,0,0,0)
		general_layout_sector_11.setContentsMargins(0,0,0,0)
		general_layout.setContentsMargins(5,5,5,5)
		general_layout.setSpacing(2)

		widget = QWidget()
		widget.setLayout(general_layout)
		self.setMinimumSize(1100,600)
		self.setCentralWidget(widget)
		
		### start thread ###
		self.threadpool = QThreadPool()
		


	def TFM_comparison(self,i):
		self.TFM_test_21 = i

	def start_program(self):
		worker = Worker(self.start_program)
		self.threadpool.start(worker)

		worker.signals.finished.connect(self.update_spirale_peltier)
		worker.signals.finished.connect(self.start_program)

	def clear_graph(self):
		self.widget01G.clear()
		self.values_graph1 = np.array([])
		self.values_graph2 = np.array([])
		self.values_graph3 = np.array([])
		self.values_graph4 = np.array([])
		self.x_values_graph = np.array([])

	def new_messurment_series(self):
		self.measurment_run = self.measurment_run_extra
		self.widgetl00L7.setText("Messung kann gestartet werden")

	def text_edited(self,s):
		self.serial_number = s

	def thickness(self,i):
		self.bare_cell_thickness=0.0074+i/1000

	def update_spirale_peltier(self):
		try:
			dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
			dut.init()
			d = dut["PowerSupply"]
			d.set_channel(1)
			time.sleep(0.05)
			vol_pel = d.get_voltage()
			time.sleep(0.05)
			cur_pel = d.get_current()
			self.widgetl00L3.setText("Aktuelle Spannung: " + str(vol_pel))
			self.widgetl00L8.setText("Aktueller Strom: " + str(cur_pel))
			time.sleep(0.05)
			d.set_channel(2)
			time.sleep(0.05)
			vol = d.get_voltage()
			time.sleep(0.05)
			cur = d.get_current()
			self.widgetl00L4.setText("Aktuelle Spannung: " + str(vol))
			self.widgetl00L9.setText("Aktueller Strom: " + str(cur))
			self.widgetl00L17.setText("")
		except:
			QApplication.processEvents()
			self.widgetl00L17.setText("Keine Verbindung zum HMP4040. Überprüfe\nZugriffsrechte oder ttyUSB auf Port 0 ist")
			QApplication.processEvents()
			return 0

		try:
			data = [1,1,1,1]
			A = adc_main.main("-c", data)
			self.widgetl00L17.setText("")
		except:
			self.widgetl00L17.setText("Keine Verbindung zum Pi oder Auslesesystem")
			return 0

		if self.spirale_status == 0 and float(vol) > 0.5:
			dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
			dut.init()
			d = dut["PowerSupply"]
			d.set_channel(2)
			time.sleep(0.1)
			d.off()
		elif self.spirale_status == 1 and float(vol) < 0.5:
			dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
			dut.init()
			d = dut["PowerSupply"]
			d.set_channel(2)
			time.sleep(0.1)
			d.on()

		if self.peltier_status == 0 and float(vol_pel) > 0.5:
			dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
			dut.init()
			d = dut["PowerSupply"]
			d.set_channel(1)
			time.sleep(0.1)
			d.off()
		elif self.peltier_status == 1 and float(vol_pel) < 0.5:
			dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
			dut.init()
			d = dut["PowerSupply"]
			d.set_channel(1)
			time.sleep(0.1)
			d.on()

		f1=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*(-5.775*10**(-7))*((100*(A[0][0]/(A[5][0]-A[0][0])))-100))))*np.sqrt((A[0][0]/(A[5][0]-A[0][0]))**2*0.00324**2+((100*(A[0][0]/(A[5][0]-A[0][0])**2))**2*(A[5][1])**2)+((100*(A[5][0]/(A[0][0]-A[5][0])**2)))**2*(A[0][1])**2)+0.05
		f2=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*-5.775*10**(-7)*((100*(A[1][0]/(A[5][0]-A[1][0])))-100))))*np.sqrt((A[1][0]/(A[5][0]-A[1][0]))**2*0.00324**2+((100*(A[1][0]/(A[5][0]-A[1][0])**2))**2*(A[5][1])**2)+((100*(A[5][0]/(A[1][0]-A[5][0])**2)))**2*(A[1][1])**2)+0.05
		f3=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*-5.775*10**(-7)*((100*(A[2][0]/(A[5][0]-A[2][0])))-100))))*np.sqrt((A[2][0]/(A[5][0]-A[2][0]))**2*0.00324**2+((100*(A[2][0]/(A[5][0]-A[2][0])**2))**2*(A[5][1])**2)+((100*(A[5][0]/(A[2][0]-A[5][0])**2)))**2*(A[2][1])**2)+0.05
		f4=1/(np.sqrt(100*((3.9083*10**(-3))**2*100+4*-5.775*10**(-7)*((100*(A[3][0]/(A[5][0]-A[3][0])))-100))))*np.sqrt((A[3][0]/(A[5][0]-A[3][0]))**2*0.00324**2+((100*(A[3][0]/(A[5][0]-A[3][0])**2))**2*(A[5][1])**2)+((100*(A[5][0]/(A[3][0]-A[5][0])**2)))**2*(A[3][1])**2)+0.05
	
		T1=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(100*(A[0][0]/(A[5][0]-A[0][0]))))))/(2*(-5.775*10**(-7)*100)))
		T2=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(100*(A[1][0]/(A[5][0]-A[1][0]))))))/(2*(-5.775*10**(-7)*100)))
		T3=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(99.62*(A[2][0]/(A[5][0]-A[2][0]))))))/(2*(-5.775*10**(-7)*100)))
		T4=((-3.9083*10**(-3)*100+np.sqrt((-3.9083*10**(-3)*100)**2-4*(-5.775*10**(-7)*100)*(100-(99.95*(A[3][0]/(A[5][0]-A[3][0]))))))/(2*(-5.775*10**(-7)*100)))

		self.widget01G.clear()
		self.values_graph1 = np.append(self.values_graph1,(T1))
		self.values_graph2 = np.append(self.values_graph2,(T2))
		self.values_graph3 = np.append(self.values_graph3,(T3))
		self.values_graph4 = np.append(self.values_graph4,(T4))
		self.x_values_graph = np.append(self.x_values_graph,len(self.values_graph1))

		if (-0.05 < (np.mean(self.values_graph1[-24:-15])-np.mean(self.values_graph1[-8:-1])) < 0.05) and (-0.05 < (np.mean(self.values_graph2[-24:-15])-np.mean(self.values_graph2[-8:-1])) < 0.05) and (-0.05 < (np.mean(self.values_graph3[-24:-15])-np.mean(self.values_graph3[-8:-1])) < 0.05) and (-0.05 < (np.mean(self.values_graph4[-24:-15])-np.mean(self.values_graph4[-8:-1])) < 0.05) and self.start_messurment_var == 1:
			self.start_messurment_var = 0
			print(self.x_values_graph[-1])
			self.messurment()
		elif (-0.05 < (np.mean(self.values_graph1[-24:-15])-np.mean(self.values_graph1[-8:-1])) < 0.05) and (-0.05 < (np.mean(self.values_graph2[-24:-15])-np.mean(self.values_graph2[-8:-1])) < 0.05) and (-0.05 < (np.mean(self.values_graph3[-24:-15])-np.mean(self.values_graph3[-8:-1])) < 0.05) and (-0.05 < (np.mean(self.values_graph4[-24:-15])-np.mean(self.values_graph4[-8:-1])) < 0.05) and self.start_test_21_var == 1:
			self.start_test_21_var = 0
			print(self.x_values_graph[-1])
			self.TFM_test_21_func()
		elif (-0.05 < (np.mean(self.values_graph1[-24:-15])-np.mean(self.values_graph1[-8:-1])) < 0.05) and (-0.05 < (np.mean(self.values_graph2[-24:-15])-np.mean(self.values_graph2[-8:-1])) < 0.05) and (-0.05 < (np.mean(self.values_graph3[-24:-15])-np.mean(self.values_graph3[-8:-1])) < 0.05) and (-0.05 < (np.mean(self.values_graph4[-24:-15])-np.mean(self.values_graph4[-8:-1])) < 0.05):
			self.widgetl00L7.setText("Temperatur Equilibrium vorhanden")
		elif self.start_test_21_var == 1 or self.start_messurment_var == 1:
			self.widgetl00L7.setText("Messung wird gestartet, sobald Equilibrium vorhanden ist")
		else:
			self.widgetl00L7.setText("Messung sollte nicht gestartet werden. Equilibrium nicht vorhanden")

		self.widget01G.setTitle("Temperatur Verlauf", color='b')
		self.widget01G.setLabel('left','Temperatur / °C', color='b')
		self.widget01G.setLabel('bottom', 'Datenpunkte / 5s', color='b')
		self.widget01G.plot(self.x_values_graph,self.values_graph1, pen=(0,0,0), name ='Sensor oben')
		self.widget01G.plot(self.x_values_graph,self.values_graph2, pen='b', name ='Sensor mitte oben')
		self.widget01G.plot(self.x_values_graph,self.values_graph3, pen='g', name ='Sensor mitte unten')
		self.widget01G.plot(self.x_values_graph,self.values_graph4, pen='r', name ='Sensor unten')
		
		if T1 >= 30:
			d.set_channel(1)
			time.sleep(0.05)
			d.off()
			time.sleep(0.05)
			d.set_channel(2)
			time.sleep(0.05)
			d.off()
			QApplication.processEvents()
			self.widgetl00L17.setText("Oberer Temperatursensor zu heiß")
			QApplication.processEvents()
		if T4 >= 25:
			d.set_channel(1)
			time.sleep(0.05)
			d.off()
			time.sleep(0.05)
			d.set_channel(2)
			time.sleep(0.05)
			d.off()
			QApplication.processEvents()
			self.widgetl00L17.setText("Unterer Temperatursensor zu heiß")
			QApplication.processEvents()

		self.widgetl00L10.setText(str(round(((A[4][0]*1000-1.55639)/2.31754),2))+'\t'+str(round((np.sqrt((1/2.31754)**2*(A[4][1]*1000)**2+(A[4][0]*1000/2.31754**2)**2*0.01692**2+(1/2.31754)**2*0.4216**2)),2)))

		name = '/home/cellqc/gittut/BareCellThermalQC_July2022/Produktion/Vollständige_Temp_Kurve_.txt'
		datei = open(name,'a')

		datei.write(str(round(T1,6))+'\t'+str(round(f1,6))
		+'\t'+str(round(T2,6))+'\t'+str(round(f2,6))
		+'\t'+str(round(T3,6))+'\t'+str(round(f3,6))
		+'\t'+str(round(T4,6))+'\t'+str(round(f4,6))
		+'\t'+str(round(((A[4][0]*1000-1.55639)/2.31754),4))+'\t'+str(round((np.sqrt((1/2.31754)**2*(A[4][1]*1000)**2+(A[4][0]*1000/2.31754**2)**2*0.01692**2+(1/2.31754)**2*0.4216**2)),4))
		+'\t'+str((float(cur)*float(vol))/(T1-T2)*0.05/(0.0001*np.pi))+'\t'+str((np.sqrt(((float(cur)*float(vol))/(T1-T2)**2*0.05/(0.0001*np.pi))**2*(f1**2+f2**2))))
		+'\t'+str((float(cur)*float(vol))/(T2-T3)*self.bare_cell_thickness/(0.0001*np.pi))+'\t'+str((np.sqrt(((float(cur)*float(vol))/(T2-T3)**2*self.bare_cell_thickness/(0.0001*np.pi))**2*(f2**2+f3**2))))
		+'\t'+str((float(cur)*float(vol))/(T3-T4)*0.05/(0.0001*np.pi))+'\t'+str((np.sqrt(((float(cur)*float(vol))/(T3-T4)**2*0.05/(0.0001*np.pi))**2*(f3**2+f4**2))))
		+'\t'+str(float(cur)*float(vol))
		+'\n')

		datei.close()

	def on_off_peltier(self, i):
		if i == 0:
			self.peltier_status = 0
			self.widgetl00L1.setText("Peltier-Element aus")
			dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
			dut.init()
			d = dut["PowerSupply"]
			d.set_channel(1)
			time.sleep(0.1)
			d.off()
		elif i == 2:
			self.peltier_status = 1
			self.widgetl00L1.setText("Peltier-Element an")
			dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
			dut.init()
			d = dut["PowerSupply"]
			d.set_channel(1)
			time.sleep(0.1)
			d.on()

	def on_off_spirale(self, i):
		if i == 0:
			self.spirale_status = 0
			self.widgetl00L2.setText("Heizspirale aus")
			dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
			dut.init()
			d = dut["PowerSupply"]
			d.set_channel(2)
			time.sleep(0.1)
			d.off()
		elif i == 2:
			self.spirale_status = 1
			self.widgetl00L2.setText("Heizspirale an")
			dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
			dut.init()
			d = dut["PowerSupply"]
			d.set_channel(2)
			time.sleep(0.1)
			d.on()

	def start_test_21(self):
		self.start_test_21_var = 1

	def TFM_test_21_func(self):
		QApplication.processEvents()
		self.widgetl00L17.setText("Test 21 Messung begonnen.\nBitte warte, dies dauert einige Minuten")
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
			lam2 = np.append(lam2,(float(cur)*float(vol))/(T2-T3)*self.bare_cell_thickness/(0.0001*np.pi))
			lam3 = np.append(lam3,(float(cur)*float(vol))/(T3-T4)*0.05/(0.0001*np.pi))
			var_lam1 = np.append(var_lam1,np.sqrt(((float(cur)*float(vol))/(T1-T2)**2*0.05/(0.0001*np.pi))**2*(f1**2+f2**2)))
			var_lam2 = np.append(var_lam2,np.sqrt(((float(cur)*float(vol))/(T2-T3)**2*self.bare_cell_thickness/(0.0001*np.pi))**2*(f2**2+f3**2)))
			var_lam3 = np.append(var_lam3,np.sqrt(((float(cur)*float(vol))/(T3-T4)**2*0.05/(0.0001*np.pi))**2*(f3**2+f4**2)))
			go += 1
		
		lambda1=np.sum(lam1/var_lam1**2)/np.sum(1/var_lam1**2)
		lambda2=np.sum(lam2/var_lam2**2)/np.sum(1/var_lam2**2)
		lambda3=np.sum(lam3/var_lam3**2)/np.sum(1/var_lam3**2)
		QApplication.processEvents()

		self.TFM_test_21 = (0.0092/lambda2-0.0076/lambda1)*(10**4)
		TFM_error = np.sqrt((0.0092/(lambda2)**2)**2*(np.sqrt(1/np.sum(1/var_lam2**2)))**2+(0.0076/(lambda1)**2)**2*(np.sqrt(1/np.sum(1/var_lam1**2)))**2+(1/(lambda2)-1/(lambda1))**2*(0.0005)**2)*10**4

		QApplication.processEvents()
		self.widget00DSB4.setValue(self.TFM_test_21.round(2))

		QApplication.processEvents()
		self.widgetl00L17.setText("Test 21 Messung abgeschlossen")

		dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
		dut.init()
		d = dut["PowerSupply"]
		d.set_channel(1)
		time.sleep(0.1)
		d.off()
		self.widget00ChB1.setChecked(False)
		time.sleep(0.1)
		d.set_channel(2)
		time.sleep(0.1)
		d.off()
		self.widget00ChB2.setChecked(False)

	def start_messurment(self):
		self.start_messurment_var = 1

	def messurment(self):
		if self.TFM_test_21 == 0.00:
			QApplication.processEvents()
			self.widgetl00L17.setText("Keine Vergleichs TFM gemessen. Messung ohne Vergleichs\nTFM durchführen bitte 0.01cm²K/W eintragen")
			return 0

		if self.serial_number == self.prev_serial_number:
			QApplication.processEvents()
			self.widgetl00L17.setText("Serien Nummer nicht geändert.\nMessung kann nicht gestartet werden")
			return 0

		QApplication.processEvents()
		self.widgetl00L17.setText("Neue Messung begonnen.\nBitte warten, dies dauert einige Minuten")
		QApplication.processEvents()

		try:
			os.mkdir("/home/cellqc/gittut/BareCellThermalQC_July2022/Produktion/%s"%(self.serial_number))
		except:
			pass
		go = 0
		datei = open('/home/cellqc/gittut/BareCellThermalQC_July2022/Produktion/%s/Messung%s_%s.txt'%(self.serial_number,self.measurment_run,self.serial_number),'w')
		datei1 = open('/home/cellqc/gittut/BareCellThermalQC_July2022/Produktion/Vollständige_Temp_Kurve_.txt','a')
		while go < 100:
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
			+'\t'+str(((float(cur)*float(vol))/(T2-T3)*self.bare_cell_thickness/(0.0001*np.pi)))+'\t'+str((np.sqrt(((float(cur)*float(vol))/(T2-T3)**2*self.bare_cell_thickness/(0.0001*np.pi))**2*(f2**2+f3**2))))
			+'\t'+str(((float(cur)*float(vol))/(T3-T4)*0.05/(0.0001*np.pi)))+'\t'+str((np.sqrt(((float(cur)*float(vol))/(T3-T4)**2*0.05/(0.0001*np.pi))**2*(f3**2+f4**2))))
			+'\t'+str(float(cur)*float(vol))
			+'\n')
			datei1.write(str(round(T1,6))+'\t'+str(round(f1,6))
			+'\t'+str(round(T2,6))+'\t'+str(round(f2,6))
			+'\t'+str(round(T3,6))+'\t'+str(round(f3,6))
			+'\t'+str(round(T4,6))+'\t'+str(round(f4,6))
			+'\t'+str(round(((A[4][0]*1000-1.55639)/2.31754),4))+'\t'+str(round((np.sqrt((1/2.31754)**2*(A[4][1]*1000)**2+(A[4][0]*1000/2.31754**2)**2*0.01692**2+(1/2.31754)**2*0.4216**2)),4))
			+'\t'+str((float(cur)*float(vol))/(T1-T2)*0.05/(0.0001*np.pi))+'\t'+str((np.sqrt(((float(cur)*float(vol))/(T1-T2)**2*0.05/(0.0001*np.pi))**2*(f1**2+f2**2))))
			+'\t'+str((float(cur)*float(vol))/(T2-T3)*self.bare_cell_thickness/(0.0001*np.pi))+'\t'+str((np.sqrt(((float(cur)*float(vol))/(T2-T3)**2*self.bare_cell_thickness/(0.0001*np.pi))**2*(f2**2+f3**2))))
			+'\t'+str((float(cur)*float(vol))/(T3-T4)*0.05/(0.0001*np.pi))+'\t'+str((np.sqrt(((float(cur)*float(vol))/(T3-T4)**2*0.05/(0.0001*np.pi))**2*(f3**2+f4**2))))
			+'\t'+str(float(cur)*float(vol))
			+'\n')

			self.widgetl00L10.setText(str(round(((A[4][0]*1000-1.55639)/2.31754),2))+'\t'+str(round((np.sqrt((1/2.31754)**2*(A[4][1]*1000)**2+(A[4][0]*1000/2.31754**2)**2*0.01692**2+(1/2.31754)**2*0.4216**2)),2)))
			time.sleep(0.05)
			go += 1

		datei1.close()
		datei.close()

		#---------------Plot_Messung---------------#

		# Load data
		A,dA,B,dB,C,dC,D,dD = [], [], [], [], [], [], [], []
		datafile = []
		datafile = np.loadtxt('/home/cellqc/gittut/BareCellThermalQC_July2022/Produktion/%s/Messung%s_%s.txt'%(self.serial_number,self.measurment_run,self.serial_number), delimiter='\t', unpack=True)
		a,da,b,db,c,dc,d,dd = 0,1,2,3,4,5,6,7
		A,dA,B,dB,C,dC,D,dD = datafile[a],datafile[da],datafile[b],datafile[db],datafile[c],datafile[dc],datafile[d],datafile[dd]

		# Creat timescale
		x = np.array([])
		for i in range(0,len(A)):
			x = np.append(x,i)

		# Creat axis and draw function
		plt.errorbar(x,A,yerr=dA, color='royalblue',fmt='.',label='Temperatur oben')
		plt.errorbar(x,B,yerr=dB, color='firebrick',fmt='.',label='Temperatur mitte oben')
		plt.errorbar(x,C,yerr=dC, color='yellow',fmt='.',label='Temperatur mitte unten')
		plt.errorbar(x,D,yerr=dD, color='orangered',fmt='.',label='Temperatur unten')

		# Some adjustments to the plot
		plt.xlabel('Datenpunkte / 5s')
		plt.ylabel('Temperatur / °C')
		plt.legend(loc='best')
		plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
		plt.tight_layout()
		plt.savefig('/home/cellqc/gittut/BareCellThermalQC_July2022/Produktion/%s/Messung%s_%s.png'%(self.serial_number,self.measurment_run,self.serial_number))
		plt.close()

		# Creat the document where Lambda, errors and other values are stored
		datei = open('/home/cellqc/gittut/BareCellThermalQC_July2022/Produktion/%s/Gemittelte_Werte_%s.txt'%(self.serial_number,self.serial_number),'a')

		lam1, lam2, lam3=datafile[10],datafile[12],datafile[14]
		var_lam1, var_lam2, var_lam3=datafile[11],datafile[13],datafile[15]
		weigth, dweigth=datafile[8],datafile[9]
		lambda1=np.sum(lam1/var_lam1**2)/np.sum(1/var_lam1**2)
		lambda2=np.sum(lam2/var_lam2**2)/np.sum(1/var_lam2**2)
		lambda3=np.sum(lam3/var_lam3**2)/np.sum(1/var_lam3**2)
		
		TFM=(0.0092/lambda2-0.0076/lambda1)*(10**4)
		TFM_error=np.sqrt((0.0092/(lambda2)**2)**2*(np.sqrt(1/np.sum(1/var_lam2**2)))**2+(0.0076/(lambda1)**2)**2*(np.sqrt(1/np.sum(1/var_lam1**2)))**2+(1/(lambda2)-1/(lambda1))**2*(0.0005)**2)*10**4

		datei.write('Gewicht' +'\t'+ 'err' +'\t'+ 'lambda_1' +'\t'+ 'err' +'\t'+ 'lambda_2' +'\t'+ 'err' +'\t'+ 'lambda_3' +'\t'+ 'err' +'\t'+ 'TFM_DUT' +'\t'+ 'err' +'\t'+ 'TFM_test_21'
		+'\n'+str(weigth[1])+'\t'+str(dweigth[1])
		+'\t'+str((lambda1.round(3)))+'\t'+str((np.sqrt(1/np.sum(1/var_lam1**2))).round(3))
		+'\t'+str((lambda2).round(3))+'\t'+str((np.sqrt(1/np.sum(1/var_lam2**2))).round(3))
		+'\t'+str((lambda3).round(3))+'\t'+str((np.sqrt(1/np.sum(1/var_lam3**2))).round(3))
		+'\t'+str(TFM.round(2))+'\t'+str(TFM_error.round(2))
		+'\t'+str(self.TFM_test_21)
		+'\n')

		datei.close()

		#---------------Plot_complete_temp_curve---------------#

		A,dA,B,dB,C,dC,D,dD = [], [], [], [], [], [], [], []
		datafile = []
		datafile = np.loadtxt('/home/cellqc/gittut/BareCellThermalQC_July2022/Produktion/Vollständige_Temp_Kurve_.txt', delimiter='\t', unpack=True)
		a,da,b,db,c,dc,d,dd = 0,1,2,3,4,5,6,7
		A,dA,B,dB,C,dC,D,dD = datafile[a],datafile[da],datafile[b],datafile[db],datafile[c],datafile[dc],datafile[d],datafile[dd]


		x = np.array([])
		for i in range(0,len(A)):
			x = np.append(x,i)

		#creat axis and draw function
		plt.errorbar(x,A,yerr=dA, color='royalblue',fmt='-',label='Temperatur oben')
		plt.errorbar(x,B,yerr=dB, color='firebrick',fmt='-',label='Temperatur mitte oben')
		plt.errorbar(x,C,yerr=dC, color='yellow',fmt='-',label='Temperatur mitte unten')
		plt.errorbar(x,D,yerr=dD, color='orangered',fmt='-',label='Temperatur unten')

		plt.xlabel('Datenpunkte / 5s')
		plt.ylabel('Temperatur / °C')
		plt.legend(loc='best')
		plt.grid(True, which='major',linestyle='-', color='dimgray', lw=0.8)
		plt.tight_layout()
		plt.savefig('/home/cellqc/gittut/BareCellThermalQC_July2022/Produktion/%s/Vollständige_Temp_Kurve_%s.png'%(self.serial_number,self.serial_number))
		plt.close()

		shutil.copy('/home/cellqc/gittut/BareCellThermalQC_July2022/Produktion/Vollständige_Temp_Kurve_.txt', 'Produktion/%s/Vollständige_Temp_Kurve_%s.txt'%(self.serial_number,self.serial_number))
		os.remove('/home/cellqc/gittut/BareCellThermalQC_July2022/Produktion/Vollständige_Temp_Kurve_.txt')

		self.measurment_run = 0
		self.measurment_run_extra += 1
		self.prev_serial_number = self.serial_number
		self.widgetl00L17.setText("Messung erfolgreich Beendet mit TFM=%s"%str(TFM.round(2)))

		dut = Dut("/home/cellqc/basil/examples/lab_devices/rs_hmp4040.yaml")
		dut.init()
		d = dut["PowerSupply"]
		d.set_channel(1)
		time.sleep(0.1)
		d.off()
		self.widget00ChB1.setChecked(False)
		time.sleep(0.1)
		d.set_channel(2)
		time.sleep(0.1)
		d.off()
		self.widget00ChB2.setChecked(False)

	def set_text(self,A):
		self.widgetl00L10.setText(str(round(((A[4][0]*1000-1.55639)/2.31754),2))+'\t'+str(round((np.sqrt((1/2.31754)**2*(A[4][1]*1000)**2+(A[4][0]*1000/2.31754**2)**2*0.01692**2+(1/2.31754)**2*0.4216**2)),2)))


def main():
	app = QApplication(sys.argv)

	window = MainWindow()
	window.show()

	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
	
