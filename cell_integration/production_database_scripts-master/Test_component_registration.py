from registerComponent_via_json import RegistrationInferface
import json
from itk_pdb.dbAccess import ITkPDSession
import itk_pdb.dbAccess as dbAccess
import time
import logging

import numpy as np
import time
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtWidgets import(QApplication, QCheckBox, QComboBox, QDateEdit, QDateTimeEdit, QDial, QDoubleSpinBox, QFontComboBox, QLabel, QLCDNumber, QLineEdit, QMainWindow, QProgressBar, QPushButton, QRadioButton, QSlider, QSpinBox, QTimeEdit, QVBoxLayout,QHBoxLayout,QGridLayout,QStackedLayout, QWidget, QDialog, QDialogButtonBox)
from PyQt5.QtGui import QPalette, QColor, QFont
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from matplotlib import pyplot as plt
import sys
from PIL import Image
import os
import upload_test_results_1
from datetime import datetime
import read_db

global serial_number 
serial_number = "0"
global mass
mass = None
global comp_type
comp_type = None
global access_code1
access_code1 = 'i*zgiVKdXn2wPZ€'
global access_code2
access_code2 = 'Hge4€jK95Kle'



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        global serial_number


        token = dbAccess.authenticate(accessCode1=access_code1, accessCode2=access_code2)
        os.environ["ITK_DB_AUTH"] = "%s"%token
        dbAccess.token = os.getenv("ITK_DB_AUTH")

		# Create Layouts
        layout = QVBoxLayout()
        layout01 = QHBoxLayout()
        layout02 = QHBoxLayout()

        self.widgetl0L1 = QLabel("Nummer der ersten zu speichernden Komponente eingeben:")
        self.widget0LE1 = QLineEdit()
        self.widget0LE1.textEdited.connect(self.text_edited)
        self.widget0LE1.setInputMask('0-0000;_')
        self.widgetl0L2 = QLabel("Hier werden fehlende Werte oder Probleme angezeigt")
        self.widgetl0L2.setStyleSheet("font-weight: bold")
        self.widgetl0L3 = QLabel("Komponente - wurde erfolgreich gespeichert")
        
        widget0CB1 = QComboBox()
        widget0CB1.addItems(["Keine Komponente ausgewählt","OB_BARE_MODULE_CELL", "OB_COOLING_BLOCK", "OB_BASE_BLOCK"])
        widget0CB1.currentTextChanged.connect(self.get_comp_type)

        widgetl0L2 = QLabel("Masse eingeben:")
        self.widget0LE2 = QLineEdit()
        self.widget0LE2.textEdited.connect(self.mass_of_part)

        widget0PB1 = QPushButton("Daten hochladen(Per Klick hier oder Enter drücken)")
        widget0PB1.clicked.connect(self.upload_data)

        layout01.addWidget(widgetl0L2)
        layout01.addWidget(self.widget0LE2)

        layout02.addWidget(self.widgetl0L1)
        layout02.addWidget(self.widget0LE1)

        layout.addWidget(widget0CB1)
        layout.addLayout(layout02)
        #layout.addWidget(self.widgetl0L3)
        layout.addLayout(layout01)
        layout.addWidget(self.widgetl0L2)
        #layout.addLayout(layout03)
        layout.addWidget(widget0PB1)

        layout.setSpacing(2)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def upload_data(self):
        global serial_number
        global comp_type
        global mass
        if comp_type != None:
            if len(serial_number) == 6:
                if self.search_for_component(comp_type,serial_number) != None:
                    self.widgetl0L2.setText("Komponente schon in der Data Base vorhanden. Manuelle Registration nötig")             
                else:
                    if mass != None:
                        #Getting the access token for the database and saving it as enviromental variable
                        token = dbAccess.authenticate(accessCode1=access_code1, accessCode2=access_code2)
                        os.environ["ITK_DB_AUTH"] = "%s"%token
                        dbAccess.token = os.getenv("ITK_DB_AUTH")

                        #Registering the component
                        if comp_type == "OB_BARE_MODULE_CELL":
                            register_data = {'componentType': 'OB_BARE_MODULE_CELL',
                                         'institution': 'BONN',
                                         'project': 'P',
                                         'properties': {'ASSEMBLY_TOOL_POSITION': 0, 'Assembly_Date': 'Dummy', 'Assembly_Tool_Identified': 'Dummy', 'Operator_Name': 'Dummy', 'PACKAGE_DATE': 'Dummy', 'PART_NUMBER': serial_number},
                                         'subproject': 'PB',
                                         'type': 'DUMMY'}
                        elif comp_type == "OB_COOLING_BLOCK":
                            register_data = {'componentType': 'OB_COOLING_BLOCK',
                                         'institution': 'BONN',
                                         'project': 'P',
                                         'properties': {'PART_NUMBER': serial_number,'Machining_Date': 'Dummy'},
                                         'subproject': 'PB',
                                         'type': 'DUMMY'}
                            stage_name = "QC"
                        elif comp_type == "OB_BASE_BLOCK":
                            register_data = {'componentType': 'OB_BASE_BLOCK',
                                         'institution': 'BONN',
                                         'project': 'P',
                                         'properties': {'PART_NUMBER': serial_number,'Machining_Date': 'Dummy'},
                                         'subproject': 'PB',
                                         'type': 'DUMMY'}
                            stage_name = "QC_BEFORE_NI_COATING"
                        dbAccess.doSomething("registerComponent",register_data)

                        #Searching if the component got registered over the alternative identifier
                        index_arr,special_code = self.search_for_component(comp_type,serial_number)

                        #Getting the right time format and giving the test data
                        format = "%Y-%m-%dT%H:%M:%SZ"
                        today = datetime.today()
                        today_str = today.strftime(format)

                        if comp_type == "OB_BARE_MODULE_CELL":
                            stage_name = "QC"
                            post_data_1 = {
                                "component": special_code,
                                "testType": "Mass_Control",
                                "institution": "BONN",
                                "runNumber": "0-0",
                                "date": today_str,
                                "passed": "true",
                                "problems": "false",
                                "results": {
                                "Cell_Mass": mass,
                                "Estimated_Glue_Mass": 0
                                    }
                                }
                        elif comp_type == "OB_COOLING_BLOCK":
                            stage_name = "QC"
                            post_data_1 = {
                                "component": special_code,
                                "testType": "Mass_control",
                                "institution": "BONN",
                                "runNumber": "0-0",
                                "date": today_str,
                                "passed": "true",
                                "problems": "false",
                                "results": {
                                "MASS": mass
                                    }
                                }
                        elif comp_type == "OB_BASE_BLOCK":
                            stage_name = "QC_BEFORE_NI_COATING"
                            post_data_1 = {
                                "component": special_code,
                                "testType": "Mass_control",
                                "institution": "BONN",
                                "runNumber": "0-0",
                                "date": today_str,
                                "passed": "true",
                                "problems": "false",
                                "results": {
                                "Base_Block_Mass": mass,
                                "Estimated_Ni_Mass": 0
                                    }
                                }

                        #Setting the component stage to QC
                        post_data = {'component': special_code,
                                    'stage': stage_name}
                        dbAccess.doSomething("setComponentStage", 
                                            data = post_data)

                        #Uploading the test result
                        dbAccess.doSomething("uploadTestRunResults", post_data_1)

                        #Counting the serial number one higher and clearing the mass
                        self.widgetl0L2.setText("Bare Cell %s wurde erfolgreich gespeichert"%serial_number)
                        serial_number = int(serial_number[2:6])
                        serial_number = serial_number+1
                        if serial_number<10:
                            serial_number = "0-000%s"%serial_number
                        elif 9<serial_number<100:
                            serial_number = "0-00%s"%serial_number
                        elif 99<serial_number<1000:
                            serial_number = "0-0%s"%serial_number
                        elif 999<serial_number<10000:
                            serial_number = "0-%s"%serial_number
                        self.widget0LE1.setText(serial_number)
                        self.widgetl0L1.setText("Komponente %s wird als nächstes eingespeichert"%serial_number)
                        self.widget0LE2.clear()
                        mass = None
                    else:
                        self.widgetl0L2.setText("Keine Masse eingegeben")
            else:
                self.widgetl0L2.setText("Seriennummer nicht vollständig")
        else:
            self.widgetl0L2.setText("Keinen Komponenten Typen ausgewählt")

    def search_for_component(self,comp_type,SN):
        '''
        Searches for a ceartain component
        Needs component_type as str; SN as serial_number
        '''
        comp_data = {"project":"P","componentType":comp_type}
        c_list = dbAccess.extractList("listComponents", method = "GET",
                data = comp_data,
                output = ["code","alternativeIdentifier"])
        c_list_1 = np.array(c_list)

        search_element = SN
        try:
            comp_index = np.where(c_list_1[:,1] == search_element)
            c_list_1[comp_index][0][0]
            return comp_index[0],c_list_1[comp_index][0][0]
        except ValueError:
            return None
        except IndexError:
            return None

    def text_edited(self,s):
        '''
		Gets the serial number of the part
		'''
        global serial_number
        serial_number = s

    def mass_of_part(self,s):
        '''
		Gets the mass of the part
		'''
        global mass
        mass = s

    def get_comp_type(self,s):
        '''
		Gets the type of the component you want to enter
		'''
        global comp_type
        comp_type = s
        if comp_type == "Keine Komponente ausgewählt":
            comp_type = None

    def keyPressEvent(self, event):
        '''
		When Enter is pressed, upload of data will start
		'''
        if event.key() == Qt.Key_Return:
            self.upload_data()




app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

