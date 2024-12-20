import numpy as np
import time
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtWidgets import(QApplication, QCheckBox, QComboBox, QDateEdit, QDateTimeEdit, QDial, QDoubleSpinBox, QFontComboBox, QLabel, QLCDNumber, QLineEdit, QMainWindow, QProgressBar, QPushButton, QRadioButton, QSlider, QSpinBox, QTimeEdit, QVBoxLayout,QHBoxLayout,QGridLayout,QStackedLayout, QWidget, QDialog, QDialogButtonBox)
from PyQt5.QtGui import QPalette, QColor
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from matplotlib import pyplot as plt
import sys
from PIL import Image
import os



class MainWindow(QMainWindow):

	def __init__(self):
		super().__init__()

		global serial_number
		global path
		global path_folder
		path_folder = '/home/loaded_cell_qc/sciebo - Klein, Nico (s6nnklei@uni-bonn.de)@uni-bonn.sciebo.de/CERN_Doku/P0/P0_BareCellFoto/'
		global up_down
		up_down = 0

		# Create Layouts
		layout = QVBoxLayout()
		layout01 = QHBoxLayout()
		layout02 = QHBoxLayout()
		layout03 = QHBoxLayout()

		# Create Widgets and give purpose
		self.widgetl0L1 = QLabel("Nummer der ersten Zelle eingeben:")
		widget0LE1 = QLineEdit()
		widget0LE1.textEdited.connect(self.text_edited)
		widget0LE1.setInputMask('1.0000;_')

		widgetl0L2 = QLabel("Pfad des Bildes eingeben:")
		self.widget0LE2 = QLineEdit()
		self.widget0LE2.textEdited.connect(self.picture_path)

		widget0PB1 = QPushButton("Bilder zuschneiden")
		widget0PB1.clicked.connect(self.start_edit)

		widgetl0L3 = QLabel("Orientierung des Bildes\n(Beginn oben links []\n Beginn unten rechts [/])")
		widget0ChB1 = QCheckBox()
		widget0ChB1.stateChanged.connect(self.orientation)

		# Add Widgets to Layouts and Layouts to main window
		layout01.addWidget(widgetl0L2)
		layout01.addWidget(self.widget0LE2)

		layout02.addWidget(self.widgetl0L1)
		layout02.addWidget(widget0LE1)

		layout03.addWidget(widgetl0L3)
		layout03.addWidget(widget0ChB1)

		layout.addLayout(layout01)
		layout.addLayout(layout02)
		layout.addLayout(layout03)
		layout.addWidget(widget0PB1)

		layout.setSpacing(2)

		widget = QWidget()
		widget.setLayout(layout)
		self.setCentralWidget(widget)

	def picture_path(self,s):
		'''
		Gets the picture path from a widget
		'''
		global path
		path = s
		global serial_number
		serial_number = '0.%s'%path[10:14]
		

	def text_edited(self,s):
		'''
		Gets the serial number of the component
		'''
		global serial_number
		serial_number = s
		#print(serial_number,type(serial_number))

	def orientation(self, i):
		global up_down
		up_down = i

	def start_edit(self):
		'''
		Is started by pressing a button and will then creat
		a folder in which all the cut out components are saved
		'''
		global path
		global serial_number
		#BaseBlock_1-0451-0540

		im = Image.open("%s%s.jpg"%(path_folder, path))

		#serial_number = float(serial_number)
		#print(serial_number)
		serial_number = int(path[10:14])
		print(serial_number)
		#print(("Base_Block_1.%i-1.%i"%(serial_number,serial_number+89)))
		#return 0

		# Create folder and check for existance of the folder, if so the process will not create new pictures
		#if os.path.exists("%.4f-%.4f"%(serial_number,serial_number+19)) ==True:
		#	self.widgetl0L1.setText("Für diese Palette wurden schon Bilder erstellt\nZum fortfahren Ordner %.4f-%.4f löschen"%(serial_number,serial_number+19/10000))
		
		#os.mkdir("%.4f-%.4f"%(serial_number,serial_number+19))

		# Cut out Bare Cells
		if up_down == 2:
			counter = 0
			for horizontal in range(4):
				#print(horizontal)
				for vertical in range(5):
					#print(f"{horizontal} \t {vertical} \t {counter}")
					Cell1 = im.crop((4300-1050*vertical,3100-1050*horizontal,5250-1050*vertical,4000-1050*horizontal))
					#Cell1.save("%.4f-%.4f/%.4f.png"%(serial_number,serial_number+19,serial_number+vertical+horizontal*4+counter))
					Cell1.save("Bare_Cell_pictures_pre_production/1.%i.png"%(serial_number+vertical+horizontal*4+counter))
     				#print(round(serial_number+vertical/10000+horizontal/10000*4+counter/10000,4))
				counter += 1
		elif up_down == 0:
			counter = 0
			for horizontal in range(4):
				#print(horizontal)
				for vertical in range(5):
					#print(f"{horizontal} \t {vertical} \t {counter}")
					Cell1 = im.crop((70+1050*vertical,0+1050*horizontal,1070+1050*vertical,900+1050*horizontal))
					#Cell1.save("%.4f-%.4f/%.4f.png"%(serial_number,serial_number+19/10000,serial_number+vertical/10000+horizontal/10000*4+counter/10000))
					Cell1.save("Bare_Cell_pictures_pre_production/1.%i.png"%(serial_number+vertical+horizontal*4+counter))
     				#print(round(serial_number+vertical/10000+horizontal/10000*4+counter/10000,4))
				counter += 1


# Start the GUI
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

