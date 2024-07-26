import pandas as pd
import numpy as np
import itk_pdb.dbAccess as dbAccess
import os


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
    #c_list_1 = np.array(c_list)
    #print(c_list_1)
    #search_element = SN
    #for element in search_element:
    #    try:
            #print(element)
    #        comp_index = np.where(c_list_1[:,1] == element)
    #        print(comp_index)
            #print(comp_index, c_list_1[comp_index][0][0])
    #        code.append(c_list_1[comp_index][0][0]), Atlas_SN.append(c_list_1[comp_index][0][2])
    #        print(c_list_1[comp_index][0][0],c_list_1[comp_index][0][2])
    #        print(code, Atlas_SN)
    #        continue
    #    except ValueError:
    #        code.append(None),  Atlas_SN.append(None)
    #        #print(code, Atlas_SN)
    #    except IndexError:
    #        code.append(None),  Atlas_SN.append(None)
    #        #print(code, Atlas_SN)
    #return code, Atlas_SN

#code, serial_numbers, temp = search_for_component('OB_BASE_BLOCK', ['1-1430','1-2200','1-0120'])
#print(code, serial_numbers, temp)

def register_comp_csv(start, stop, comp_type, filename, sheet_name, file_save, skiprows=4, *args, **kwargs):
    '''
    needs:  -start and stop position of components you want to read in (int)
            -the component type you want to upload (string)
            -the filename of the xlsx data you want to read in (string)
            -the table of the xlsx sheet you want to read in (string)
            -the rows of the document you want to skip (int)
            -for args the columns from the sheet you are reading out as list ((int),(int),...)
            -for kwargs the property keys need to be given {"property1_key":'',"property2_key":'',...}

    return: -CSV file that can be uploaded into the streamlit app in register component
            -list of components with their alternitiv identifiers('1-0001') in CSV file
    '''
    df = pd.read_excel(filename, sheet_name=sheet_name, skiprows=skiprows, usecols=args[0])
    array = df.to_numpy()

    register = []
    prop = []
    prop_key = []
    pre_reg = []
    pre_reg_1 = []
    counter = 1

    for key, value in kwargs.items():
        prop = np.append(prop, value)
        prop_key = np.append(prop_key, [key,'property%s_value'%counter])
        counter += 1

    columns = ['project','subproject','institution','componentType','type']#'property1_key','property1_value','property2_key','property2_value']
    columns = np.append(columns,prop_key)

    for i in range(start,stop):
        for j in range(len(prop)):
            pre_reg = np.append(pre_reg,[prop[j],array[i][j]])
        pre_reg_1 = ('P','PB','BONN',comp_type,comp_type)
        pre_reg_1 = np.append(pre_reg_1,pre_reg)
        register.append(pre_reg_1)
        pre_reg = []
        pre_reg_1 = []


    df =  pd.DataFrame(data=register,columns=columns)
    df.to_csv("csv_files/%s/register_%s.csv"%(file_save,file_save))


#comp_stage = "QC"
#sheet_name = 15
#col_1 = 0
#col_2 = 2
#col_3 = 6
#col_4 = 7
#col_5 = 8
#col_6 = 9
#kwargs_Base_Block = {"property1_key":'PART_NUMBER', "property2_key":'PACKAGE_DATE', "property3_key":'Assembly_Date', "property4_key":'Operator_Name', "property5_key":'Assembly_Tool_Identified', "property6_key":'ASSEMBLY_TOOL_POSITION'}
#file_save = "Bare_Cell"

#register_comp_csv(4,8, "OB_BASE_BLOCK", 'ZW_PDBBareCells_P1_V4.xlsx', sheet_name, file_save, 4, col_1, col_2, **kwargs_Base_Block)
#register_comp_csv(4,8, "OB_COOLING_BLOCK", 'ZW_PDBBareCells_P1_V4.xlsx', sheet_name, file_save, 4, col_1, col_2, **kwargs_Base_Block)
#register_comp_csv(4,8, "OB_BARE_MODULE_CELL", 'ZW_PDBBareCells_P1_V4.xlsx', sheet_name, file_save, 4, (col_1, col_2, col_3, col_4, col_5, col_6), **kwargs_Base_Block)


def set_stage_csv(list_of_SN, comp_type, stage, file_save):
    '''
    needs:  -list of the alternitive identifiers
            -the component type you want to change the stage of
            -the stage in what it needs to be changed
    creats: -CSV file that can be uploaded into the streamlit app in multi stage set
    '''

    code, serial_numbers, temp = search_for_component(comp_type,list_of_SN) #liste = ['1-0001','1-0002','1-0003']
    stage_csv = []

    for i in range(len(list_of_SN)):
        stage_csv.append((serial_numbers[i], stage)) #'QC_BEFORE_NI_COATING'

    df = pd.DataFrame(stage_csv,columns=['serialNumber','stage'])
    df.to_csv('csv_files/%s/stage_%s.csv'%(file_save,file_save))

#print(register_comp_csv(4,8,'OB_BASE_BLOCK','ZW_PDBBareCells_P1_V4.xlsx', 4, 5, 7, property1_key='PART_NUMBER',property2_key='Machining_Date'))

#liste = ['1-0001','1-0002','1-0003']
#comp_type = "OB_BASE_BLOCK"

#code, serial_numbers = search_for_component(comp_type,liste)

