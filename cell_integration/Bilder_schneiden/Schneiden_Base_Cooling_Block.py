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
		widget0LE2 = QLineEdit()
		widget0LE2.textEdited.connect(self.picture_path)

		widget0PB1 = QPushButton("Bilder zuschneiden")
		widget0PB1.clicked.connect(self.start_edit)

		widgetl0L3 = QLabel("Orientierung des Bildes\n(Beginn oben links []\n Beginn unten rechts [/])")
		widget0ChB1 = QCheckBox()
		widget0ChB1.stateChanged.connect(self.orientation)

		# Add Widgets to Layouts and Layouts to main window
		layout01.addWidget(widgetl0L2)
		layout01.addWidget(widget0LE2)

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

		im = Image.open("%s.jpg"%path)

		serial_number = float(serial_number)

		# Create folder and check for existance of the folder, if so the process will not create new pictures
		if os.path.exists("Base_Block_%.4f-%.4f"%(serial_number,serial_number+89/10000)) ==True:
			self.widgetl0L1.setText("Für diese Palette wurden schon Bilder erstellt\nZum fortfahren Ordner %.4f-%.4f löschen"%(serial_number,serial_number+19/10000))
		
		os.mkdir("Base_Block_%.4f-%.4f"%(serial_number,serial_number+89/10000))

		# Cut out Bare Cells
		if up_down == 2:
			counter = 0
			for horizontal in range(9):
				#print(horizontal)
				for vertical in range(10):
					#print(f"{horizontal} \t {vertical} \t {counter}")
					Cell1 = im.crop((4800-540*vertical,3450-420*horizontal,5250-520*vertical,3900-420*horizontal))
					#print(f"{3450-420*horizontal} \t {4800-540*vertical} \t {3900-420*horizontal} \t {5250-520*vertical}")
					Cell1.save("Base_Block_%.4f-%.4f/%.4f.png"%(serial_number,serial_number+89/10000,serial_number+vertical/10000+horizontal/10000*9+counter/10000))
					Cell1.save("Base_Block_pictures/%.4f.png"%(serial_number+vertical/10000+horizontal/10000*9+counter/10000))
				counter += 1
		elif up_down == 0:
			counter = 0
			for horizontal in range(9):
				#print(horizontal)
				for vertical in range(10):
					#print(f"{horizontal} \t {vertical} \t {counter}")
					Cell1 = im.crop((0+540*vertical,90+420*horizontal,570+540*vertical,540+420*horizontal))
					Cell1.save("Base_Block_%.4f-%.4f/%.4f.png"%(serial_number,serial_number+89/10000,serial_number+vertical/10000+horizontal/10000*9+counter/10000))
					Cell1.save("Base_Block_pictures/%.4f.png"%(serial_number+vertical/10000+horizontal/10000*9+counter/10000))
					#print(round(serial_number+vertical/10000+horizontal/10000*4+counter/10000,4))
				counter += 1


# Start the GUI
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

