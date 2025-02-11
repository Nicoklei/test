import pandas as pd
import numpy as np
import itk_pdb.dbAccess as dbAccess
import os
from datetime import datetime
from pathlib import Path
from CSV_file_changer_Base_Block import search_for_component

import itkdb

access_code1 = 'i*zgiVKdXn2wPZ€'
access_code2 = 'Hge4€jK95Kle'
token = dbAccess.authenticate(accessCode1=access_code1, accessCode2=access_code2)
os.environ["ITK_DB_AUTH"] = "%s"%token
dbAccess.token = os.getenv("ITK_DB_AUTH")

def delete_component(comp_type, SN, reason):
    code, sn, temp = search_for_component(comp_type, SN)
    for i in code:
        dbAccess.doSomething('deleteComponent', method = "POST", data={'component' : i, 'reason' : reason})
        print('deleted' + SN[i])


def eos_upload_picture(filename, sn, code, title):
        #"ITKDB_ACCESS_CODE1" access_code1 als enviromental setzen
        #"ITKDB_ACCESS_CODE2" access_code2 als enviromental setzen

        client = itkdb.Client(use_eos=True)

        data = {"component": code,
                "title": "%s at stage %s"%(sn, title),
                "description": "Picture at stage %s"%title,
                "url": Path(filename),
                "type": "file"}
        attachment = {"data": open(filename, 'rb')}

        with Path(filename).open("rb") as fpointer:
                files = {"data": itkdb.utils.get_file_components({"data": fpointer})}  
                response = client.post("createComponentAttachment", data=data, files=files)  


def eos_upload_metrology(filename, sn, code, title):
        #"ITKDB_ACCESS_CODE1" access_code1 als enviromental setzen
        #"ITKDB_ACCESS_CODE2" access_code2 als enviromental setzen
        client = itkdb.Client(use_eos=True)

        data = {"component": code,
                "title": "%s at stage %s"%(sn, title),
                "description": "Metrology at stage %s"%title,
                "url": Path(filename),
                "type": "file"}
        attachment = {"data": open(filename, 'rb')}

        with Path(filename).open("rb") as fpointer:
                files = {"data": itkdb.utils.get_file_components({"data": fpointer})}  
                response = client.post("createComponentAttachment", data=data, files=files)  


def mass_control_test(start, stop, comp_type, comp_stage, test_type, filename, sheet_name, file_save, altid_name, skiprows=4, *args, **kwargs):
    '''
    -kwargs take the type of key (either resultX_key or propertyX_key) and as value the code of the key
    
    -args take columns of the excel table. First value needs to be the component alternative identifier
    second one needs to be the date and rest need to be the values given in the kwargs
    '''
    
    df = pd.read_excel(filename, sheet_name=sheet_name, skiprows=skiprows, usecols=args)
    array = df.to_numpy()

    code=[]
    date=[]
    format = "%d/%m/%Y"
    prop_key = []
    prop = []
    counter_prop = 1
    counter_res = 1

    for key, value in kwargs.items():
        prop = np.append(prop, value)
        if key[0:2] == 'pr':
            prop_key = np.append(prop_key, [key,'property%s_value'%counter_prop])
            counter_prop += 1
        else:
            prop_key = np.append(prop_key, [key,'result%s_value'%counter_res])
            counter_res += 1
    columns = ['component','componentType','stage','testType','date','runNumber','passed','problems']#'property1_key','property1_value','property2_key','property2_value']
    columns = np.append(columns,prop_key)


    for i in range(start-1,stop):
        code.append('%s%s'%(altid_name,array[i][0]))
        date.append(array[i][1].strftime(format))
    code, sn, temp = search_for_component(comp_type,code)

    test_results = []
    pre_reg = []
    register = []
    array = array[start-1:stop]
    array = np.append(array, np.zeros_like(array), axis=1)


    for i in range(0,len(sn)):
        for j in range(len(prop)):
            pre_reg = np.append(pre_reg,[prop[j],array[i][j+2]])
        test_results = (sn[i],comp_type,comp_stage,test_type,date[i],'1.0',True,False)
        test_results = np.append(test_results,pre_reg)
        register.append(test_results)
        
        test_results = []
        pre_reg = []

    df_1 =  pd.DataFrame(data=register,columns=columns)
    df_1.to_csv('csv_files/%s/Mass_control_%s.csv'%(file_save,file_save))
    print(df_1)


def dim_control_test(start, stop, comp_type, comp_stage, filename, sheet_name, file_save, altid_name, skiprows=4, *args, **kwargs):
    '''
    -kwargs take the type of key (either resultX_key or propertyX_key) and as value the code of the key
    
    -args take columns of the excel table. First value needs to be the component alternative identifier
    second one needs to be the date, third one needs to be the pass/nopass if key is given
    and rest need to be the fitting values given in the kwargs
    '''
    df = pd.read_excel(filename, sheet_name=sheet_name,skiprows=skiprows, usecols=args)
    array = df.to_numpy()
    
    code=[]
    date=[]
    pass_nopass=[]
    format = "%d/%m/%Y"
    register = []
    prop = []
    prop_key = []
    pre_reg = []
    pre_reg_1 = []
    counter_prop = 1
    counter_res = 1
    
    for key, value in kwargs.items():
        prop = np.append(prop, value)
        if key[0:2] == 'pr':
            prop_key = np.append(prop_key, [key,'property%s_value'%counter_prop])
            counter_prop += 1
        else:
            prop_key = np.append(prop_key, [key,'result%s_value'%counter_res])
            counter_res += 1
    columns = ['component','componentType','stage','testType','date','runNumber','passed','problems']#'property1_key','property1_value','property2_key','property2_value']
    columns = np.append(columns,prop_key)

    for i in range(start-1,stop):
        code.append('%s%s'%(altid_name,array[i][0]))
        date.append(array[i][1].strftime(format))
        if array[i][2] == 'Pass':
            pass_nopass.append(True)
        elif array[i][2] == 'No Pass':
            pass_nopass.append(False)
        elif comp_type == 'OB_PG_TILE':
            pass_nopass.append(True)

    code, sn, temp = search_for_component(comp_type, code)
    array = array[start-1:stop]

    print(sn,date,pass_nopass)
    for i in range(0,len(sn)):
        for j in range(len(prop)):
            if prop[j] == 'Pass/No_Pass':
                pre_reg = np.append(pre_reg,[prop[j],pass_nopass[i]])
            else:
                pre_reg = np.append(pre_reg,[prop[j],array[i][j+2]])
        pre_reg_1 = (sn[i],comp_type,comp_stage,'Dimensional_Control',date[i],'1.0',pass_nopass[i],False)
        pre_reg_1 = np.append(pre_reg_1,pre_reg)
        register.append(pre_reg_1)
        pre_reg = []
        pre_reg_1 = []

    df_1 =  pd.DataFrame(data=register,columns=columns)
    df_1.to_csv('csv_files/%s/Dim_control_%s.csv'%(file_save,file_save))
    print(df_1)


def visual_control_test(start, stop, comp_type, comp_stage, filename, sheet_name, file_save, altid_name, skiprows=4, *args):
    '''
    -args take columns of the excel table. First value needs to be the component alternative identifier
    second one needs to be the date, third one needs to be the pass/nopass key
    '''

    df = pd.read_excel(filename, sheet_name=sheet_name,skiprows=skiprows, usecols=args)
    array = df.to_numpy()
    
    code=[]
    date=[]
    pass_nopass=[]
    test_results = []
    format = "%d/%m/%Y"

    for i in range(start-1,stop):
        code.append('%s%s'%(altid_name,array[i][0]))
        date.append(array[i][1].strftime(format))
        if array[i][2] == 'Pass':
            pass_nopass.append(True)
        elif array[i][2] == 'No Pass':
            pass_nopass.append(False)

    code, sn, temp = search_for_component(comp_type, code)

    for i in range(0,len(sn)):
        test_results.append((sn[i],comp_type,comp_stage,'Visual_Inspection',date[i],'1.0',pass_nopass[i],'false','Pass/No_Pass',pass_nopass[i]))

    df_1 =  pd.DataFrame(data=test_results,columns=['component','componentType','stage','testType','date','runNumber','passed','problems','result1_key','result1_value'])
    df_1.to_csv('csv_files/%s/visual_control_%s.csv'%(file_save,file_save))
    print(df_1)
    
    
def thread_check_test(start, stop, comp_type, comp_stage, filename, sheet_name, file_save, altid_name, skiprows=4, *args):
    '''
    -args take columns of the excel table. First value needs to be the component alternative identifier
    second one needs to be the date, third one needs to be the failure model, and forth needs to be the failure load
    '''
    df = pd.read_excel(filename, sheet_name=sheet_name,skiprows=skiprows, usecols=args)
    array = df.to_numpy()
    code=[]
    date=[]
    format = "%d/%m/%Y"

    for i in range(start-1,stop):
        code.append('%s%s'%(altid_name,array[i][0]))
        date.append(array[i][1].strftime(format))

    code, sn, temp = search_for_component(comp_type, code)

    test_results = []

    for i in range(0,len(sn)):
        test_results.append((sn[i],comp_type,comp_stage,'Thread_Check',date[i],'1.0',True,'false','Failure_Load', array[i][3], 'Failure_Model_(Thread/Pin)', array[i][2]))


    df_1 =  pd.DataFrame(data=test_results,columns=['component','componentType','stage','testType','date','runNumber','passed','problems','result1_key','result1_value','result2_key','result2_value'])
    df_1.to_csv('csv_files/%s/thread_check_%s.csv'%(file_save,file_save))


def thermal_cycling_test(start, stop, comp_type, comp_stage, filename, sheet_name, file_save, altid_name, skiprows=4, *args):
    '''
    -args take columns of the excel table. First value needs to be the component alternative identifier
    second one needs to be the date, everything else should and is always a hard coded value in here
    '''
    df = pd.read_excel(filename, sheet_name=sheet_name,skiprows=skiprows, usecols=args)
    array = df.to_numpy()
    code=[]
    date=[]
    format = "%d/%m/%Y"

    for i in range(start-1,stop):
        code.append('%s%s'%(altid_name,array[i][0]))
        date.append(array[i][1].strftime(format))

    code, sn, temp = search_for_component(comp_type, code)

    test_results = []

    for i in range(0,len(sn)):
        test_results.append((sn[i],comp_type,comp_stage,'Thermal_cycling',date[i],'1.0',True,'false','Maximum_Temperature', 40, 'Minimum_Temperature', -45, 'Number_of_Cycles', 1, 'Done/Not_Done', True))


    df_1 =  pd.DataFrame(data=test_results,columns=['component','componentType','stage','testType','date','runNumber','passed','problems','property1_key','property1_value','property2_key','property2_value','property3_key','property3_value','result1_key','result1_value'])
    df_1.to_csv('csv_files/%s/thermal_cycling_%s.csv'%(file_save,file_save))


def thermal_impedance_test(start, stop, comp_type, comp_stage, filename, sheet_name, file_save, altid_name, skiprows=4, *args):
    '''
    -args take columns of the excel table. First value needs to be the component alternative identifier
    second one needs to be the date, third one needs to be the test temperature, the forth one needs to be test power
    and the fifth needs to be the apparent thermal impedance
    '''
    df = pd.read_excel(filename, sheet_name=sheet_name,skiprows=skiprows, usecols=args)
    array = df.to_numpy()
    code=[]
    date=[]
    format = "%d/%m/%Y"

    for i in range(start-1,stop):
        code.append('%s%s'%(altid_name,array[i][0]))
        date.append(array[i][1].strftime(format))

    code, sn, temp = search_for_component(comp_type, code)

    test_results = []

    for i in range(0,len(sn)):
        test_results.append((sn[i],comp_type,comp_stage,'Thermal_performance_check',date[i],'1.0',True,'false','Test_Date', date[i], 'Test_Temperature', array[i][2], 'Test_Power', array[i][3], 'Apparent_Thermal_Impedance', array[i][4]))


    df_1 =  pd.DataFrame(data=test_results,columns=['component','componentType','stage','testType','date','runNumber','passed','problems','property1_key','property1_value','property2_key','property2_value','property3_key','property3_value','result1_key','result1_value'])
    df_1.to_csv('csv_files/%s/thermal_impedence_%s.csv'%(file_save,file_save))
