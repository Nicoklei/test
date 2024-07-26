import pandas as pd
import numpy as np
import itk_pdb.dbAccess as dbAccess
import os
from datetime import datetime
from pathlib import Path

import itkdb

access_code1 = 'i*zgiVKdXn2wPZ€'
access_code2 = 'Hge4€jK95Kle'
token = dbAccess.authenticate(accessCode1=access_code1, accessCode2=access_code2)
os.environ["ITK_DB_AUTH"] = "%s"%token
dbAccess.token = os.getenv("ITK_DB_AUTH")

def search_for_component(comp_type,SN):
    '''
    Searches for a ceartain component
    Needs component_type as str; SN as serial_number
    Returns None, if more than one or zero components are found
    Returns Code of component as first value and the SerialNumber as second value
    '''
    access_code1 = 'i*zgiVKdXn2wPZ€'
    access_code2 = 'Hge4€jK95Kle'
    token = dbAccess.authenticate(accessCode1=access_code1, accessCode2=access_code2)
    os.environ["ITK_DB_AUTH"] = "%s"%token
    dbAccess.token = os.getenv("ITK_DB_AUTH")

    code = []
    Atlas_SN = []
    recived_comp_type = []

    for i in SN:
        comp_data = {"project":"P","component" : i, 'alternativeIdentifier': True,"type":comp_type,"componentType":comp_type}
        c_list = dbAccess.extractList("getComponent", method = "GET",
                data = comp_data)
        #print(c_list)
        if comp_type == c_list.get("componentType").get("code"):
            code.append(c_list.get("code"))
            Atlas_SN.append(c_list.get("serialNumber"))
            recived_comp_type.append(c_list.get("componentType").get("code"))
            print(c_list.get("code"), c_list.get("serialNumber"), c_list.get("alternativeIdentifier"), c_list.get("componentType").get("code"))
        else:
            print("Not the right component type")
            #code.append(None)
            #Atlas_SN.append(None)
            #recived_comp_type.append(c_list.get("componentType").get("code"))
            
    return code, Atlas_SN, comp_type
    #for element in search_element:
    #    try:
            #print(element)
    #        comp_index = np.where(c_list_1[:,1] == element)
            #print(comp_index, c_list_1[comp_index][0][0])
    #        code.append(c_list_1[comp_index][0][0]), Atlas_SN.append(c_list_1[comp_index][0][2])
            #print(code, Atlas_SN)
    #        continue
    #    except ValueError:
    #        code.append(None),  Atlas_SN.append(None)
            #print(code, Atlas_SN)
    #    except IndexError:
    #        code.append(None),  Atlas_SN.append(None)
            #print(code, Atlas_SN)
    #return code, Atlas_SN

#dbAccess.doSomething('deleteComponent',method = "POST", data={'component' : '1-2430', 'alternativeIdentifier': True, 'reason' : 'Test of deletion'})

def delete_component(comp_type, SN, reason):
    code, sn, temp = search_for_component(comp_type, SN)
    for i in code:
        dbAccess.doSomething('deleteComponent',method = "POST", data={'component' : i, 'reason' : reason})
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

#eos_test("BaseBloc_1-0001-0090(2).jpg", "20UPBBB0000002", "c7f81310557d253e167458d4591ab80c")


def mass_control_test(start, stop, comp_type, comp_stage, filename, sheet_name, file_save, skiprows=4, *args, **kwargs):
    df = pd.read_excel(filename, sheet_name=sheet_name, skiprows=skiprows, usecols=args[0])
    array = df.to_numpy()
    code=[]
    date=[]
    format = "%d/%m/%Y"

    prop_key = []
    prop = []
    counter_prop = 1
    counter_res = 1
    #print(kwargs)
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
        code.append(array[i][0])
        date.append(array[i][1].strftime(format))
    code, sn, temp = search_for_component(comp_type,code)

    test_results = []
    pre_reg = []
    register = []
    array = array[start-1:stop]
    array = np.append(array, np.zeros_like(array), axis=1)


    for i in range(0,len(sn)):
        #print(prop)
        for j in range(len(prop)):
            print(type(array[i][j+2]))
            pre_reg = np.append(pre_reg,[prop[j],array[i][j+2]])
        #print(pre_reg)
        
        test_results = (sn[i],comp_type,comp_stage,'Mass_Control',date[i],'1.0',True,False)
        test_results = np.append(test_results,pre_reg)
        #print(test_results)
        register.append(test_results)
        test_results = []
        pre_reg = []

    df_1 =  pd.DataFrame(data=register,columns=columns)
    df_1.to_csv('csv_files/%s/Mass_control_%s.csv'%(file_save,file_save))
    print(df_1)

#mass_control_test(5, 20, "OB_BASE_BLOCK", "QC_BEFORE_NI_COATING", 'ZW_PDBBareCells_P1_V4.xlsx', 5, 'Base_Block', 4, (0,1,3),**{"result1_key":'Base_Block_Mass', "result2_key":'Estimated_Ni_Mass'})

def dim_control_test(start, stop, comp_type, comp_stage, filename, sheet_name, file_save, skiprows=4, *args, **kwargs):
    df = pd.read_excel(filename, sheet_name=sheet_name,skiprows=skiprows, usecols=args[0])
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
    #print(columns)

    for i in range(start-1,stop):
        code.append(array[i][0])
        date.append(array[i][1].strftime(format))
        if array[i][2] == 'Pass':
            pass_nopass.append(True)
        elif array[i][2] == 'No Pass':
            pass_nopass.append(False)

    code, sn, temp = search_for_component(comp_type,code)
    array = array[start-1:stop]

    for i in range(0,len(sn)):
        for j in range(len(prop)):
            if prop[j] == 'Metrology_Report':
                pre_reg = np.append(pre_reg,[prop[j],'Dummy'])
            elif prop[j] == 'Pass/No_Pass':
                if array[i][j+2] == 'Pass':
                    pass_nopass_val = True
                elif array[i][j+2] == 'No Pass':
                    pass_nopass_val = False
                elif comp_type == 'OB_PG_TILE':
                    pass_nopass_val = True
                    pass_nopass = np.ones_like(code, dtype = bool)
                pre_reg = np.append(pre_reg,[prop[j],pass_nopass_val])
            else:
                if comp_type == 'OB_PG_TILE':
                    pre_reg = np.append(pre_reg,[prop[j],array[i][j+1]])
                else:
                    pre_reg = np.append(pre_reg,[prop[j],array[i][j+2]])
        pre_reg_1 = (sn[i],comp_type,comp_stage,'Dimensional_Control',date[i],'1.0',pass_nopass[i],False)
        pre_reg_1 = np.append(pre_reg_1,pre_reg)
        register.append(pre_reg_1)
        pre_reg = []
        pre_reg_1 = []

    df_1 =  pd.DataFrame(data=register,columns=columns)#['component','componentType','stage','testType','date','runNumber','passed','problems','property1_key','property1_value','result1_key','result1_value','result2_key','result2_value'])
    df_1.to_csv('csv_files/%s/Dim_control_%s.csv'%(file_save,file_save))
    #print(df_1)



#sheet_name_test = 11
#col_1 = 0
#col_2 = 1
#col_3 = 3
#col_4 = 4
#col_5 = 5
#cols_test = (col_1, col_2, col_3, col_4, col_5)
#kwargs_test_type = {"result1_key":'Pass/No_Pass', "result2_key":'THICKNESS', "property1_key":'Machine_Name', "result3_key":'Metrology_Report'}
#dim_control_test(3,9,'OB_COOLING_BLOCK', "QC", 'ZW_PDBBareCells_P1_V4.xlsx',sheet_name_test, "Cooling_Block", 4, cols_test,**kwargs_test_type)

#sheet_name_test = 6
#col_1 = 0
#col_2 = 1
#col_3 = 3
#col_4 = 5
#cols_test = (col_1, col_2, col_3, col_4)
#sheet_name_test = 6
#kwargs_test_type = {"result1_key":'Pass/No_Pass', "property1_key":'Machine_Name', "result2_key":'Metrology_Report'}
#dim_control_test(3,9,'OB_BASE_BLOCK',"QC_BEFORE_NI_COATING",'ZW_PDBBareCells_P1_V4.xlsx', sheet_name_test,'Base_Block', cols_test, **kwargs_test_type)


#col_1 = 0
#col_2 = 1
#col_3 = 3
#col_4 = 4
#col_5 = 5
#cols_test = (col_1, col_2, col_3, col_4, col_5)
#sheet_name_test = 17
#kwargs_test_type = {"result1_key":'Pass/No_Pass', "result2_key":"WIDTH", "result3_key":"THICKNESS", "result4_key":"LENGTH"}


#col_1 = 0
#col_2 = 16
#col_3 = 18
#col_4 = 22
#col_5 = 25 #nachfragen, ob Machine_name eingetragen werden kann in excel tabelle
#cols_test = (col_1, col_2, col_3, col_4, col_5)
#sheet_name_test = 24
#kwargs_test_type = {"result1_key":'Pass/No_Pass', "result2_key":"Glue+Cooling_Block_Thickness", "property1_key":"Machine_Name", "result3_key":"Metrology_Report"}

#dim_control_test(3,9,'OB_BARE_MODULE_CELL', "QC", 'ZW_PDBBareCells_P1_V4.xlsx',sheet_name_test, "Bare_cell", 4, cols_test,**kwargs_test_type)



def visual_control_test(start, stop, comp_type, comp_stage, filename, sheet_name, col_1, col_2, col_3, file_save, skiprows=4):
    df = pd.read_excel(filename, sheet_name=sheet_name,skiprows=skiprows, usecols=[col_1, col_2, col_3,])
    array = df.to_numpy()
    
    code=[]
    date=[]
    pass_nopass=[]
    format = "%d/%m/%Y"

    if comp_type == 'OB_BASE_BLOCK':
        key1 = 'Base_Block_Pictures'
    elif comp_type == 'OB_BARE_MODULE_CELL':
        key1 = 'Pictures_of_the_Bare_Cell'

    for i in range(start-1,stop):
        code.append(array[i][0])
        date.append(array[i][1].strftime(format))
        if array[i][2] == 'Pass':
            pass_nopass.append(True)
        elif array[i][2] == 'No Pass':
            pass_nopass.append(False)

    code, sn, temp = search_for_component(comp_type, code)

    test_results = []

    for i in range(0,len(sn)):
        test_results.append((sn[i],comp_type,comp_stage,'Visual_Inspection',date[i],'1.0',pass_nopass[i],'false',key1,'Dummy','Pass/No_Pass',pass_nopass[i]))

    df_1 =  pd.DataFrame(data=test_results,columns=['component','componentType','stage','testType','date','runNumber','passed','problems','result1_key','result1_value','result2_key','result2_value'])
    df_1.to_csv('csv_files/%s/visual_control_%s.csv'%(file_save,file_save))
    #print(df_1)

#visual_control_test(2,6,'OB_BASE_BLOCK','QC_BEFORE_NI_COATING','ZW_PDBBareCells_P1_V4.xlsx',7,0,1,4)

def thread_check_test(start, stop, comp_type, comp_stage, filename, sheet_name, col_1, col_2, col_3, col_4, file_save, skiprows=4):#needs more work
    df = pd.read_excel(filename, sheet_name=sheet_name,skiprows=skiprows, usecols=[col_1, col_2, col_3, col_4])
    array = df.to_numpy()
    code=[]
    date=[]
    format = "%d/%m/%Y"

    for i in range(start-1,stop):
        code.append(array[i][0])
        date.append(array[i][1].strftime(format))

    code, sn, temp = search_for_component(comp_type, code)

    test_results = []

    for i in range(0,len(sn)):
        test_results.append((sn[i],comp_type,comp_stage,'Thread_Check',date[i],'1.0',True,'false','Failure_Load', array[i][3], 'Failure_Model_(Thread/Pin)', array[i][2]))


    df_1 =  pd.DataFrame(data=test_results,columns=['component','componentType','stage','testType','date','runNumber','passed','problems','result1_key','result1_value','result2_key','result2_value'])
    df_1.to_csv('csv_files/%s/thread_check_%s.csv'%(file_save,file_save))
    #print(df_1)

