import numpy as np
import time
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtWidgets import(QApplication, QCheckBox, QComboBox, QDateEdit, QDateTimeEdit, QDial, QDoubleSpinBox, QFontComboBox, QLabel, QLCDNumber, QLineEdit, QMainWindow, QProgressBar, QPushButton, QRadioButton, QSlider, QSpinBox, QTimeEdit, QVBoxLayout,QHBoxLayout,QGridLayout,QStackedLayout, QWidget, QDialog, QDialogButtonBox)
from PyQt5.QtGui import QPalette, QColor, QFont
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from matplotlib import pyplot as plt
import sys
import os
from datetime import datetime

import itk_pdb.dbAccess as dbAccess
import itkdb
import CSV_file_changer_Base_Block as reg_BB
import Base_Block_test_results as BB_test


serial_number_stop = None
serial_number_start = None
list_of_alt_id = None
comp_type = "Keine Komponente ausgewählt"
test_type = "Keinen Test ausgewählt"
access_code1 = 'i*zgiVKdXn2wPZ€'
access_code2 = 'Hge4€jK95Kle'
picture_path = None
metro_path = None
skip_rows = 4


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        #token = dbAccess.authenticate(accessCode1=access_code1, accessCode2=access_code2)
        #os.environ["ITK_DB_AUTH"] = "%s"%token
        #dbAccess.token = os.getenv("ITK_DB_AUTH")

		# Create Layouts
        layout = QVBoxLayout()
        layout01 = QHBoxLayout()
        layout02 = QHBoxLayout()
        layout03 = QHBoxLayout()
        layout04 = QHBoxLayout()
        layout05 = QHBoxLayout()
        layout06 = QHBoxLayout()

        self.widgetl0L6 = QLabel("Generelle Voreinstellungen treffen")
        font = self.widgetl0L6.font()
        font.setPointSize(14)
        self.widgetl0L6.setFont(font)

        self.widgetl0L1 = QLabel("Nummer der ersten zu speichernden Komponente eingeben:")
        self.widget0LE1 = QLineEdit()
        self.widget0LE1.textEdited.connect(self.text_edited_start)
        self.widget0LE1.setInputMask('0000;_')

        self.widgetl0L2 = QLabel("Nummer der letzten zu speichernden Komponente eingeben:")
        self.widget0LE2 = QLineEdit()
        self.widget0LE2.textEdited.connect(self.text_edited_stop)
        self.widget0LE2.setInputMask('0000;_')

        self.widgetl0L3 = QLabel("Name der File eingeben, sonst wird 'ZW_PDBBareCells_P1_V4.xlsx' genutzt:")
        self.widget0LE3 = QLineEdit()
        self.widget0LE3.textEdited.connect(self.text_edited_filename)

        widget0CB1 = QComboBox()
        widget0CB1.addItems(["Keine Komponente ausgewählt","OB_BARE_MODULE_CELL", "OB_COOLING_BLOCK", "OB_BASE_BLOCK", "OB_PG_TILE"])
        widget0CB1.currentTextChanged.connect(self.get_comp_type)
        
        widget0CB3 = QComboBox()
        widget0CB3.addItems(["Produktion","Pre-Produktion"])
        widget0CB3.currentTextChanged.connect(self.get_pre_pro)


        self.widgetl0L7 = QLabel("CSV Dateien für Registration und Stage erstellen")
        self.widgetl0L7.setFont(font)

        widget0PB1 = QPushButton("CSV Datei zur Registration erstellen")
        widget0PB1.clicked.connect(self.create_csv_file_registration)

        widget0PB2 = QPushButton("CSV Datei zur Stage erstellen")
        widget0PB2.clicked.connect(self.create_csv_file_set_stage)

        widget0PB7 = QPushButton("CSV Datei zum Shippment erstellen")
        widget0PB7.clicked.connect(self.create_shippment_csv)
        
        widget0PB8 = QPushButton("CSV Datei zum Assemblen einer Komponente erstellen")
        widget0PB8.clicked.connect(self.create_assemble_csv)

        self.widgetl0L5 = QLabel("CSV Dateien für Tests erstellen")
        self.widgetl0L5.setFont(font)

        widget0CB2 = QComboBox()
        widget0CB2.addItems(["Keinen Test ausgewählt", "Massen Kontrolle", "Dimensions Kontrolle", "Visuelle Kontrolle", "Thread Check", "Thermal Cycling", "Thermal Impedance"])
        widget0CB2.currentTextChanged.connect(self.get_test_type)

        widget0PB3 = QPushButton("CSV Datei zum ausgewählten Test erstellen")
        widget0PB3.clicked.connect(self.create_csv_file_upload_test)


        self.widgetl0L9 = QLabel("Dateien zu EoS hochladen")
        self.widgetl0L9.setFont(font)
        
        self.widgetl0L14 = QLabel("CSV Datei zum Assemblen und Shippment erstellen")
        self.widgetl0L14.setFont(font)

        self.widgetl0L10 = QLabel("Datei Pfad zu Bildern (Name Bild: '1.****') eingeben, sonst wird \n'/Bilder_schneiden/Base_Block_pictures/' verwendet:")
        self.widget0LE4 = QLineEdit()
        self.widget0LE4.textEdited.connect(self.text_edited_picture)

        self.widgetl0L11 = QLabel("Datei Pfad zu Metrology Berichten \n(Name Bericht: 'Base_Block_1_****.xlsx') eingeben, sonst wird \n'metrology_reports_Base_Block/' verwendet:")
        self.widget0LE5 = QLineEdit()
        self.widget0LE5.textEdited.connect(self.text_edited_metrology)


        widget0PB4 = QPushButton("Bilder zu EoS hochladen")
        widget0PB4.clicked.connect(self.eos_upload_picture)

        widget0PB5 = QPushButton("Metrology Bericht zu EoS hochladen")
        widget0PB5.clicked.connect(self.eos_upload_metrology)
        
        self.widgetl0L12 = QLabel("Komponenten löschen")
        self.widgetl0L12.setFont(font)
        self.widgetl0L13 = QLabel("Grund für die Löschung hier eingeben:")
        self.widget0LE6 = QLineEdit()
        self.widget0LE6.textEdited.connect(self.reason_for_delete)
        widget0PB6 = QPushButton("Komponenten unwiederruflich löschen")
        widget0PB6.clicked.connect(self.delete_components)


        self.widgetl0L8 = QLabel("Status des Programms")
        self.widgetl0L8.setFont(font)
        self.widgetl0L4 = QLabel("Wählen Sie die Parameter aus")
        font1 = self.widgetl0L4.font()
        font1.setPointSize(12)
        self.widgetl0L4.setFont(font1)

#print(register_comp_csv(4,8,'OB_BASE_BLOCK','ZW_PDBBareCells_P1_V4.xlsx', 4, 5, 7, property1_key='PART_NUMBER',property2_key='Machining_Date'))

        layout01.addWidget(self.widgetl0L1)
        layout01.addWidget(self.widget0LE1)
        layout02.addWidget(self.widgetl0L2)
        layout02.addWidget(self.widget0LE2)
        layout03.addWidget(self.widgetl0L3)
        layout03.addWidget(self.widget0LE3)
        layout04.addWidget(self.widgetl0L10)
        layout04.addWidget(self.widget0LE4)
        layout05.addWidget(self.widgetl0L11)
        layout05.addWidget(self.widget0LE5)


        layout.addWidget(self.widgetl0L6)
        layout.addWidget(widget0CB3)
        layout.addLayout(layout01)
        layout.addLayout(layout02)
        layout.addLayout(layout03)
        layout.addWidget(widget0CB1)

        layout.addWidget(self.widgetl0L7)
        layout.addWidget(widget0PB1)
        layout.addWidget(widget0PB2)

        layout.addWidget(self.widgetl0L5)
        layout.addWidget(widget0CB2)
        layout.addWidget(widget0PB3)

        layout.addWidget(self.widgetl0L9)
        #layout.addLayout(layout04)
        #layout.addLayout(layout05)
        layout.addWidget(widget0PB4)
        layout.addWidget(widget0PB5)
        
        layout.addWidget(self.widgetl0L14)
        layout.addWidget(widget0PB7)
        layout.addWidget(widget0PB8)
        
        layout.addWidget(self.widgetl0L12)
        layout06.addWidget(self.widgetl0L13)
        layout06.addWidget(self.widget0LE6)
        layout.addLayout(layout06)
        layout.addWidget(widget0PB6)
        
        layout.addWidget(self.widgetl0L8)
        layout.addWidget(self.widgetl0L4)

        layout.setSpacing(2)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def reason_for_delete(self,s):
        '''
        Entersreason for deltion of components
        '''
        global del_reason
        del_reason = s

    def text_edited_picture(self,s):
        '''
		Gets the path to the picture folder
		'''
        global picture_path
        picture_path = s
    def text_edited_metrology(self,s):
        '''
		Gets the path to the picture folder
		'''
        global metro_path
        metro_path = s
    def text_edited_start(self,s):
        '''
		Gets the serial number of the first part
		'''
        global serial_number_start
        serial_number_start = s
    def text_edited_stop(self,s):
        '''
		Gets the serial number of the last part
		'''
        global serial_number_stop
        serial_number_stop = s
    def text_edited_filename(self,s):
        '''
		Gets filename
		'''
        global filename
        filename = s
        
    def get_serial_numbers(self, altid_name):
        global serial_number_start
        global serial_number_stop
        global pre_production_id
        
        list_of_alt_id = []
        list_of_cells = range(int(serial_number_start),int(serial_number_stop)+1)
        for serial_number in list_of_cells:
            if serial_number<10:
                serial_number = "%s%s-000%s"%(altid_name, pre_production_id, serial_number)
            elif 9<serial_number<100:
                serial_number = "%s%s-00%s"%(altid_name, pre_production_id, serial_number)
            elif 99<serial_number<1000:
                serial_number = "%s%s-0%s"%(altid_name, pre_production_id, serial_number)
            elif 999<serial_number<10000:
                serial_number = "%s%s-%s"%(altid_name, pre_production_id, serial_number)
            list_of_alt_id.append(serial_number)
        return list_of_alt_id
        
    def delete_components(self):
        global del_reason
        global comp_type
        global altid_name

        list_of_alt_id = self.get_serial_numbers(altid_name)        

        BB_test.delete_component(comp_type, list_of_alt_id, del_reason)
        QApplication.processEvents()
        self.widgetl0L4.setText("Alle Komponenten erfolgreich gelöscht")
        QApplication.processEvents()
        
    def get_pre_pro(self,s):
        global pre_production_id
        global filename
        if s == "Produktion":
            pre_production_id = '1'
            filename = '/home/loaded_cell_qc/sciebo - Klein, Nico (s6nnklei@uni-bonn.de)@uni-bonn.sciebo.de/CERN_Doku/P1/P1_Doku/ZW_PDBBareCells_P1_V5_2024-05-27.xlsx'
        elif s == "Pre-Produktion":
            pre_production_id = '0'
            filename = '/home/loaded_cell_qc/sciebo - Klein, Nico (s6nnklei@uni-bonn.de)@uni-bonn.sciebo.de/CERN_Doku/P0/P0_Doku/ZW_PDBBareCells_Quali-0_2023-09-28.xlsx'

            
            
    def get_comp_type(self,s):
        '''
		Gets the type of the component you want
        and sets different global varibles for the type
		'''
        global comp_type
        global sheet_name
        global cols
        global kwargs_comp_type
        global comp_stage
        global file_save
        global altid_name
        global assemble_altid
        global assemble_children
        
        comp_type = s
        if comp_type == "Keine Komponente ausgewählt":
            return 0
        
        elif comp_type == "OB_BASE_BLOCK":
            comp_stage = "QC_BEFORE_NI_COATING"
            sheet_name = 'ZW Base Blocks Erfassung'
            col_1 = 3
            col_2 = 5
            col_3 = 7
            cols = (col_1, col_2, col_3)
            kwargs_comp_type = {"property1_key":'MATERIAL_ROD_AL-G_SUPPLIER_REFERENCE' , "property2_key":'PART_NUMBER' , "property3_key":'Machining_Date'}
            file_save = "Base_Block"
            altid_name = ""

        elif comp_type == "OB_COOLING_BLOCK":
            comp_stage = "QC"
            sheet_name = 'ZW Cooling Blocks-Erfassung'
            col_1 = 3
            col_2 = 5
            col_3 = 7
            cols = (col_1, col_2, col_3)
            kwargs_comp_type = {"property1_key":'MATERIAL_ROD_AL-G_SUPPLIER_REFERENCE' , "property2_key":'PART_NUMBER' , "property3_key":'Machining_Date'}
            file_save = "Cooling_Block"
            altid_name = "CB"
        
        elif comp_type == "OB_BARE_MODULE_CELL":
            if pre_production_id == '0':
                comp_stage = "QC"
                sheet_name = 'ZW BC Zuordnung PGT Zuordnung'
                col_1 = 0
                col_2 = 1
                col_3 = 5
                col_5 = 7
                col_6 = 8
                cols = (col_1, col_2, col_3, col_5, col_6)
                kwargs_comp_type = {"property1_key":'PART_NUMBER', "property2_key":'PACKAGE_DATE', "property3_key":'Assembly_Date', "property5_key":'Assembly_Tool_Identified', "property6_key":'ASSEMBLY_TOOL_POSITION'}
                file_save = "Bare_Cell"
                altid_name = "BC"
                assemble_altid = ('BC', 'CB', 'PGT')
                assemble_children = {"child1":'OB_COOLING_BLOCK', "child2":'OB_PG_TILE'}
            else:
                comp_stage = "QC"
                sheet_name = 'ZW BC Zuordnung PGT Zuordnung'
                col_1 = 0
                col_2 = 2 
                col_3 = 6 
                col_5 = 8
                col_6 = 9
                cols = (col_1, col_2, col_3, col_5, col_6)
                kwargs_comp_type = {"property1_key":'PART_NUMBER', "property2_key":'PACKAGE_DATE', "property3_key":'Assembly_Date', "property5_key":'Assembly_Tool_Identified', "property6_key":'ASSEMBLY_TOOL_POSITION'}
                file_save = "Bare_Cell"
                altid_name = "BC"
                assemble_altid = ('BC', 'CB', 'PGT')
                assemble_children = {"child1":'OB_COOLING_BLOCK', "child2":'OB_PG_TILE'}

        elif comp_type == "OB_PG_TILE":
            if pre_production_id == '0':
                comp_stage = "QC1"
                sheet_name = 'ZW BC Zuordnung PGT Zuordnung'
                col_1 = 0
                col_2 = 1
                col_3 = 3
                cols = (col_1, col_2, col_3)
                kwargs_comp_type = {"property1_key":'PART_NUMBER', "property2_key":'Delivery_Date', "property3_key":'Supplier_Batch_Reference'}
                file_save = "PG_Tile"
                altid_name = "PGT"
            else:
                comp_stage = "QC1"
                sheet_name = 'ZW BC Zuordnung PGT Zuordnung'
                col_1 = 0
                col_2 = 2
                col_3 = 4
                cols = (col_1, col_2, col_3)
                kwargs_comp_type = {"property1_key":'PART_NUMBER', "property2_key":'Delivery_Date', "property3_key":'Supplier_Batch_Reference'}
                file_save = "PG_Tile"
                altid_name = "PGT"



    def create_csv_file_registration(self):
        global sheet_name
        global cols
        global kwargs_comp_type
        global comp_type
        global serial_number_stop
        global filename
        global serial_number_start
        global list_of_alt_id
        global file_save
        global altid_name

        if comp_type == "Keine Komponente ausgewählt":
            self.widgetl0L4.setText("Ein Komponenten Typ muss ausgewählt werden")
        else:
            if serial_number_start != None:
                if serial_number_stop != None:
                    self.widgetl0L4.setText("Die CSV Datei wird erstellt. Bitte warten")
                    QApplication.processEvents()
                    reg_BB.register_comp_csv(int(serial_number_start)-1,int(serial_number_stop), comp_type, filename, sheet_name, file_save, altid_name, skip_rows, cols, **kwargs_comp_type)
                    #register_comp_csv(4,8, "OB_BASE_BLOCK", 'ZW_PDBBareCells_P1_V4.xlsx', sheet_name, file_save, 4, col_1, col_2, **kwargs_Base_Block)
                    self.widgetl0L4.setText("Die CSV Datei ist erstellt")
                else: self.widgetl0L4.setText("Ein Stop Serien Nummer muss ausgewählt werden")
            else: self.widgetl0L4.setText("Ein Start Serien Nummer muss ausgewählt werden")

    def create_csv_file_set_stage(self):
        global list_of_alt_id
        global comp_type
        global comp_stage
        global serial_number_start
        global serial_number_stop
        global file_save
        global altid_name

        if comp_type == "Keine Komponente ausgewählt":
            self.widgetl0L4.setText("Ein Komponenten Typ muss ausgewählt werden")
        else:
            if serial_number_start != None:
                if serial_number_stop != None:
                        self.widgetl0L4.setText("Die CSV Datei für die Stage wird erstellt. Bitte warten")
                        QApplication.processEvents()
                        
                        list_of_alt_id = self.get_serial_numbers(altid_name)
                        
                        reg_BB.set_stage_csv(list_of_alt_id, comp_type, comp_stage, file_save)
                        self.widgetl0L4.setText("Die CSV Datei für die Stage wurde erstellt")
                else: self.widgetl0L4.setText("Ein Stop Serien Nummer muss ausgewählt werden")
            else: self.widgetl0L4.setText("Ein Start Serien Nummer muss ausgewählt werden")


    def create_shippment_csv(self):
        global list_of_alt_id
        global comp_type
        global serial_number_start
        global serial_number_stop
        global file_save
        global altid_name

        if comp_type == "Keine Komponente ausgewählt":
            self.widgetl0L4.setText("Ein Komponenten Typ muss ausgewählt werden")
        else:
            if serial_number_start != None:
                if serial_number_stop != None:
                        self.widgetl0L4.setText("Die CSV Datei für das Shippment wird erstellt. Bitte warten")
                        QApplication.processEvents()

                        list_of_alt_id = self.get_serial_numbers(altid_name)
                        
                        reg_BB.shipping(list_of_alt_id, comp_type, file_save)
                        self.widgetl0L4.setText("Die CSV Datei für das Shippment wurde erstellt")
                else: self.widgetl0L4.setText("Ein Stop Serien Nummer muss ausgewählt werden")
            else: self.widgetl0L4.setText("Ein Start Serien Nummer muss ausgewählt werden")

    def create_assemble_csv(self):
        global list_of_alt_id
        global comp_type
        global serial_number_start
        global serial_number_stop
        global file_save
        global assemble_altid
        global assemble_children
        

        if comp_type == "Keine Komponente ausgewählt":
            self.widgetl0L4.setText("Ein Komponenten Typ muss ausgewählt werden")
        else:
            if serial_number_start != None:
                if serial_number_stop != None:
                        self.widgetl0L4.setText("Die CSV Datei zum Assemblen wird erstellt. Bitte warten")
                        QApplication.processEvents()

                        list_of_alt_id = self.get_serial_numbers(altid_name="")
                        
                        reg_BB.assembly(list_of_alt_id, comp_type, file_save, *assemble_altid, **assemble_children)
                        self.widgetl0L4.setText("Die CSV Datei zum Assemblen wurde erstellt")
                else: self.widgetl0L4.setText("Ein Stop Serien Nummer muss ausgewählt werden")
            else: self.widgetl0L4.setText("Ein Start Serien Nummer muss ausgewählt werden")


    def get_test_type(self,s):
        '''
		Gets the type of test you want to upload
        and sets different global varibles for the type
		'''
        global test_type
        global sheet_name_test
        global comp_stage
        global comp_type
        global kwargs_test_type
        test_type = s    
        global cols_test
        if test_type == "Keinen Test ausgewählt":
            return 0  

        elif test_type == "Massen Kontrolle":
            if comp_type == "OB_BASE_BLOCK":
                comp_stage = "QC_BEFORE_NI_COATING"
                sheet_name_test = 'ZW Base Blocks-Wägung'
                col_1 = 0
                col_2 = 1
                col_3 = 3
                cols_test = (col_1, col_2, col_3)
                kwargs_test_type = {"result1_key":'Base_Block_Mass', "result2_key":'Estimated_Ni_Mass'}
            elif comp_type == "OB_COOLING_BLOCK":
                comp_stage = "QC"
                sheet_name_test = 'ZW Cooling Blocks-Wägung'
                col_1 = 0
                col_2 = 1
                col_3 = 3    
                cols_test = (col_1, col_2, col_3)
                kwargs_test_type = {"result1_key":'MASS'}
            elif comp_type == "OB_PG_TILE":
                if pre_production_id == '0':
                    comp_stage = "QC1"
                    sheet_name_test = 'ZW BC Zuordnung PGT Zuordnung'
                    col_1 = 0
                    col_2 = 1
                    col_3 = 4
                    cols_test = (col_1, col_2, col_3)
                    kwargs_test_type = {"result1_key":'MASS'}
                else:
                    comp_stage = "QC1"
                    sheet_name_test = 'ZW BC Zuordnung PGT Zuordnung'
                    col_1 = 0
                    col_2 = 2
                    col_3 = 5
                    cols_test = (col_1, col_2, col_3)
                    kwargs_test_type = {"result1_key":'MASS'}
            elif comp_type == "OB_BARE_MODULE_CELL":
                comp_stage = "QC"
                sheet_name_test = 'DATA Bare Cell'
                col_1 = 4
                col_2 = 23 
                col_3 = 31 
                col_4 = 32
                cols_test = (col_1, col_2, col_3, col_4)
                kwargs_test_type = {"result1_key":'Cell_Mass', "result2_key":"Estimated_Glue_Mass"}

        elif test_type == "Dimensions Kontrolle":
            if comp_type == "OB_BASE_BLOCK":
                comp_stage = "QC_BEFORE_NI_COATING"
                sheet_name_test = 'ZW Base Blocks-Geometrie'
                col_1 = 0
                col_2 = 1
                col_3 = 3
                col_4 = 4
                cols_test = (col_1, col_2, col_3, col_4)
                kwargs_test_type = {"result1_key":'Pass/No_Pass', "result2_key": 'THICKNESS'}
            elif comp_type == "OB_COOLING_BLOCK":
                comp_stage = "QC"
                sheet_name_test = 'ZW Cooling Blocks-Geometrie'
                col_1 = 0
                col_2 = 1
                col_3 = 3
                col_4 = 4
                cols_test = (col_1, col_2, col_3, col_4)
                kwargs_test_type = {"result1_key":'Pass/No_Pass', "result2_key":'THICKNESS'}
            elif comp_type == "OB_PG_TILE":
                comp_stage = "QC1"
                sheet_name_test = 'ZW BC-PGT Maße übertragen'
                col_1 = 0
                col_2 = 1
                col_3 = 3
                col_4 = 4
                col_5 = 5
                cols_test = (col_1, col_2, col_3, col_4, col_5)
                kwargs_test_type = {"result1_key":"THICKNESS", "result2_key":"WIDTH", "result3_key":"LENGTH"}
            elif comp_type == "OB_BARE_MODULE_CELL":
                comp_stage = "QC"
                sheet_name_test = 'DATA Bare Cell'
                col_1 = 0
                col_2 = 16
                col_3 = 18
                col_4 = 22
                cols_test = (col_1, col_2, col_3, col_4)
                kwargs_test_type = {"result1_key":'Pass/No_Pass', "result2_key":"Glue+Cooling_Block_Thickness"}

        elif test_type == "Visuelle Kontrolle":
            if comp_type == "OB_BASE_BLOCK":
                if pre_production_id == '0':
                    comp_stage = "QC_BEFORE_NI_COATING"
                    sheet_name_test = 'ZW Base Blocks-Geometrie'
                    col_1 = 0
                    col_2 = 1
                    col_3 = 3 
                    cols_test = (col_1, col_2, col_3)
                else:
                    comp_stage = "QC_BEFORE_NI_COATING"
                    sheet_name_test = 'ZW Base Blocks-Sichtprüfung'
                    col_1 = 0
                    col_2 = 1
                    col_3 = 4 
                    cols_test = (col_1, col_2, col_3)
            elif comp_type == "OB_COOLING_BLOCK":
                self.widgetl0L4.setText("Kein solcher Test für Cooling Blocks")
            elif comp_type == "OB_PG_TILE":
                self.widgetl0L4.setText("Kein solcher Test für PG Tiles")
            elif comp_type == "OB_BARE_MODULE_CELL":
                if pre_production_id == '0':
                    comp_stage = "QC"
                    sheet_name_test = 'CERN Bare Module Cell'
                    col_1 = 2
                    col_2 = 6
                    col_3 = 11
                    cols_test = (col_1, col_2, col_3)
                else:
                    comp_stage = "QC"
                    sheet_name_test = 'CERN Bare Module Cell'
                    col_1 = 2
                    col_2 = 6
                    col_3 = 12
                    cols_test = (col_1, col_2, col_3)

        elif test_type == "Thread Check": # not one test uploaded in pre or normal sheet
            if comp_type == "OB_BASE_BLOCK":
                self.widgetl0L4.setText("Kein solcher Test für Base Blocks")
            elif comp_type == "OB_COOLING_BLOCK":
                comp_stage = "QC"
                sheet_name_test = 'ZW Cooling Blocks-Zugprobe'
                col_1 = 0
                col_2 = 2
                col_3 = 4
                col_4 = 5 
                cols_test = (col_1, col_2, col_3, col_4)
            elif comp_type == "OB_PG_TILE":
                self.widgetl0L4.setText("Kein solcher Test für PG Tiles")
            elif comp_type == "OB_BARE_MODULE_CELL":
                self.widgetl0L4.setText("Kein solcher Test für Bare Cells")

        elif test_type == "Thermal Cycling":
            if comp_type == "OB_BASE_BLOCK":
                self.widgetl0L4.setText("Kein solcher Test für Base Blocks")
            elif comp_type == "OB_COOLING_BLOCK":
                self.widgetl0L4.setText("Kein solcher Test für Cooling Blocks")
            elif comp_type == "OB_PG_TILE":
                self.widgetl0L4.setText("Kein solcher Test für PG Tiles")
            elif comp_type == "OB_BARE_MODULE_CELL":
                comp_stage = "QC"
                sheet_name_test = 'CERN Bare Module Cell'
                col_1 = 2
                col_2 = 6
                cols_test = (col_1, col_2)
                
        elif test_type == "Thermal Impedance":
            if comp_type == "OB_BASE_BLOCK":
                self.widgetl0L4.setText("Kein solcher Test für Base Blocks")
            elif comp_type == "OB_COOLING_BLOCK":
                self.widgetl0L4.setText("Kein solcher Test für Cooling Blocks")
            elif comp_type == "OB_PG_TILE":
                self.widgetl0L4.setText("Kein solcher Test für PG Tiles")
            elif comp_type == "OB_BARE_MODULE_CELL":
                if pre_production_id == '0':
                    comp_stage = "QC"
                    sheet_name_test = 'CERN Bare Module Cell'
                    col_1 = 2
                    col_2 = 22
                    col_3 = 24
                    col_4 = 25
                    col_5 = 26
                    cols_test = (col_1, col_2, col_3, col_4, col_5)
                else:
                    comp_stage = "QC"
                    sheet_name_test = 'CERN Bare Module Cell'
                    col_1 = 2
                    col_2 = 24 
                    col_3 = 26 
                    col_4 = 27 
                    col_5 = 28 
                    cols_test = (col_1, col_2, col_3, col_4, col_5)
                
                
    def create_csv_file_upload_test(self):
        global test_type
        global sheet_name_test
        global comp_stage
        global comp_type
        global serial_number_start
        global serial_number_stop
        global filename
        global file_save
        global cols_test
        global altid_name
        if comp_type == "Keine Komponente ausgewählt":
            self.widgetl0L4.setText("Ein Komponenten Typ muss ausgewählt werden")
        else:
            if serial_number_start != None:
                if serial_number_stop != None:
                    if test_type == "Keinen Test ausgewählt":
                        self.widgetl0L4.setText("Ein Test Typ muss ausgewählt werden")
                    elif comp_type == "Keine Komponente ausgewählt":
                        self.widgetl0L4.setText("Ein Komponenten Typ muss ausgewählt werden")
                    elif test_type == "Massen Kontrolle":
                        self.widgetl0L4.setText("Die CSV Datei für den Masse Test wird erstellt. Bitte warten")
                        QApplication.processEvents()
                        BB_test.mass_control_test(int(serial_number_start),int(serial_number_stop), comp_type, comp_stage, filename, sheet_name_test, file_save, altid_name, skip_rows, *cols_test, **kwargs_test_type)
                        self.widgetl0L4.setText("Die CSV Datei für den Masse Test wurde erstellt")
                    elif test_type == "Dimensions Kontrolle":
                        self.widgetl0L4.setText("Die CSV Datei für den Dimensions Test wird erstellt. Bitte warten")
                        QApplication.processEvents()
                        BB_test.dim_control_test(int(serial_number_start),int(serial_number_stop), comp_type, comp_stage, filename, sheet_name_test, file_save, altid_name, skip_rows, *cols_test, **kwargs_test_type)
                        self.widgetl0L4.setText("Die CSV Datei für den Dimensions Test wurde erstellt")
                    elif test_type == "Visuelle Kontrolle":
                        self.widgetl0L4.setText("Die CSV Datei für den Visuellen Test wird erstellt. Bitte warten")
                        QApplication.processEvents()
                        BB_test.visual_control_test(int(serial_number_start),int(serial_number_stop), comp_type, comp_stage, filename, sheet_name_test, file_save, altid_name, skip_rows, *cols_test)
                        self.widgetl0L4.setText("Die CSV Datei für den Visuellen Test wurde erstellt")
                    elif test_type == "Thread Check":
                        self.widgetl0L4.setText("Die CSV Datei für den Thread Check test wird erstellt. Bitte warten")
                        QApplication.processEvents()
                        BB_test.thread_check_test(int(serial_number_start),int(serial_number_stop), comp_type, comp_stage, filename, sheet_name_test, file_save, altid_name, skip_rows, *cols_test)
                    elif test_type == "Thermal Cycling":
                        self.widgetl0L4.setText("Die CSV Datei für den Thermal Cycling test wird erstellt. Bitte warten")
                        QApplication.processEvents()
                        BB_test.thermal_cycling_test(int(serial_number_start),int(serial_number_stop), comp_type, comp_stage, filename, sheet_name_test, file_save, altid_name, skip_rows, *cols_test)
                    elif test_type == "Thermal Impedance":
                        self.widgetl0L4.setText("Die CSV Datei für den Thermal Impedance test wird erstellt. Bitte warten")
                        QApplication.processEvents()
                        BB_test.thermal_impedance_test(int(serial_number_start),int(serial_number_stop), comp_type, comp_stage, filename, sheet_name_test, file_save, altid_name, skip_rows, *cols_test)
                else: self.widgetl0L4.setText("Ein Stop Serien Nummer muss ausgewählt werden")
            else: self.widgetl0L4.setText("Ein Start Serien Nummer muss ausgewählt werden")

    def eos_upload_picture(self):
        global list_of_alt_id
        global comp_type
        global serial_number_start
        global serial_number_stop
        global picture_path
        global comp_stage
        global altid_name

        if picture_path == None:
            if comp_type == "OB_BASE_BLOCK":
                picture_path = 'Bilder_schneiden/Base_Block_pictures/'
            elif comp_type == "OB_COOLING_BLOCK":
                picture_path = 'Bilder_schneiden/Cooling_Block_pictures/'
        else:
            picture_path = picture_path

        if comp_type == "Keine Komponente ausgewählt":
            self.widgetl0L4.setText("Ein Komponenten Typ muss ausgewählt werden")
        else:
            if serial_number_start != None:
                if serial_number_stop != None:
                        self.widgetl0L4.setText("Die Bilder für den Visuellen Test werden hochgeladen. Bitte warten")
                        QApplication.processEvents()

                        list_of_alt_id = self.get_serial_numbers(altid_name)
                        print(list_of_alt_id)
                        
                        code, serial_numbers, temp = BB_test.search_for_component(comp_type, list_of_alt_id)
                        list_of_alt_id_clean = self.get_serial_numbers('')
                        for i in range(0,len(serial_numbers)):
                            print(list_of_alt_id_clean[i][2:6])
                            #BB_test.eos_upload_picture("%s1.%s.png"%(picture_path,list_of_alt_id_clean[i][2:6]), serial_numbers[i], code[i], comp_stage)
                        self.widgetl0L4.setText("Die Bilder für den Visuellen Test wurden hochgeladen")
                else: self.widgetl0L4.setText("Ein Stop Serien Nummer muss ausgewählt werden")
            else: self.widgetl0L4.setText("Ein Start Serien Nummer muss ausgewählt werden")

    def eos_upload_metrology(self):
        global list_of_alt_id
        global comp_type
        global comp_stage
        global serial_number_start
        global serial_number_stop
        global metro_path
        global altid_name

        if metro_path == None:
            if comp_type == "OB_BASE_BLOCK":
                metro_path = '/home/loaded_cell_qc/sciebo - Klein, Nico (s6nnklei@uni-bonn.de)@uni-bonn.sciebo.de/CERN_Doku/P1/P1_BaseBlockMessprotokoll/Base_Block_1_'
            elif comp_type == "OB_COOLING_BLOCK":
                metro_path = 'metrology_reports_Cooling_Block/'
        else:
            metro_path = metro_path


        if comp_type == "Keine Komponente ausgewählt":
            self.widgetl0L4.setText("Ein Komponenten Typ muss ausgewählt werden")
        else:
            if serial_number_start != None:
                if serial_number_stop != None:
                        self.widgetl0L4.setText("Die Metrology reports werden hochgeladen. Bitte warten")
                        QApplication.processEvents()

                        list_of_alt_id = self.get_serial_numbers(altid_name)
                        
                        code, serial_numbers, temp = BB_test.search_for_component(comp_type, list_of_alt_id)
                        list_of_alt_id_clean = self.get_serial_numbers('')
                        for i in range(0,len(serial_numbers)):
                            BB_test.eos_upload_metrology("%s%s.xlsx"%(metro_path,int(list_of_alt_id_clean[i][2:6])), serial_numbers[i], code[i], comp_stage)
                        self.widgetl0L4.setText("Die Metrology reports wurden erfolgreich hochgeladen")
                else: self.widgetl0L4.setText("Ein Stop Serien Nummer muss ausgewählt werden")
            else: self.widgetl0L4.setText("Ein Start Serien Nummer muss ausgewählt werden")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
