import pandas as pd
import numpy as np
import itk_pdb.dbAccess as dbAccess
import os

def search_for_component(comp_type, SN):
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
        print(i)
        comp_data = {"component" : i, 'alternativeIdentifier': True}
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
            print('Gotten component type:' + c_list.get("componentType").get("code"),'Wanted component type:' + comp_type)
            #print(c_list.get("code"), c_list.get("serialNumber"), c_list.get("alternativeIdentifier"), c_list.get("componentType").get("code"))
            
    return code, Atlas_SN, comp_type

def register_comp_csv(start, stop, comp_type, filename, sheet_name, file_save, altid_name, skiprows=4, *args, **kwargs):
    '''
    needs:  -start and stop position of components you want to read in (int)
            -the component type you want to upload (string)
            -the filename of the xlsx data you want to read in (string)
            -the table of the xlsx sheet you want to read in (string)
            -the name the output csv shall have
            -the name of the alternative identifier like CB for Cooling_Block
            -the rows of the document you want to skip (int)
            -for args the columns from the sheet you are reading out as list ((int),(int),...)
            -for kwargs the property keys need to be given {"property1_key":'',"property2_key":'',...}

    return: -CSV file that can be uploaded into the streamlit app in register component
    '''
    print(args)
    df = pd.read_excel(filename, sheet_name=sheet_name, skiprows=skiprows, usecols=args)
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

    columns = ['project','subproject','institution','componentType','type']
    columns = np.append(columns,prop_key)

    for i in range(start,stop):
        for j in range(len(prop)):
            if prop[j] == 'PART_NUMBER':
                pre_reg = np.append(pre_reg,[prop[j],'%s%s'%(altid_name, array[i][j])])
            else:
                pre_reg = np.append(pre_reg,[prop[j],array[i][j]])
                
        pre_reg_1 = ('P','PB','BONN',comp_type,comp_type)
        pre_reg_1 = np.append(pre_reg_1,pre_reg)
        register.append(pre_reg_1)

        pre_reg = []
        pre_reg_1 = []


    df =  pd.DataFrame(data=register,columns=columns)
    df.to_csv("csv_files/%s/register_%s.csv"%(file_save,file_save))


def set_stage_csv(list_of_SN, comp_type, stage, file_save):
    '''
    needs:  -list of the alternitive identifiers
            -the component type you want to change the stage of
            -the stage in what it needs to be changed
    creats: -CSV file that can be uploaded into the streamlit app in multi stage set
    '''

    code, serial_numbers, temp = search_for_component(comp_type,list_of_SN)
    stage_csv = []

    for i in range(len(list_of_SN)):
        stage_csv.append((serial_numbers[i], stage))

    df = pd.DataFrame(stage_csv,columns=['serialNumber','stage'])
    df.to_csv('csv_files/%s/stage_%s.csv'%(file_save,file_save))


def shipping(list_of_SN, comp_type, file_save):
    '''
    needs:  -list of the alternitive identifiers
            -the component type you want to ship of
    creats: -CSV file that can be uploaded into the streamlit app in multi ship set
    '''
    code, serial_numbers, temp = search_for_component(comp_type, list_of_SN) 
    ship_csv = []

    for i in range(len(list_of_SN)):
        ship_csv.append((serial_numbers[i]))

    df = pd.DataFrame(ship_csv,columns=['serialNumber'])
    df.to_csv('csv_files/%s/shipping_%s.csv'%(file_save,file_save))


def assembly(list_of_SN, comp_type, file_save, *args,**kwargs):
    '''
    needs:  -list of the alternitive identifiers
            -the component type you want to assemble of
    creats: -CSV file that can be uploaded into the streamlit app in multi assemble set
    '''
    assemble_csv = []
    children = []
    children_comp_type = []
    list_of_parent_SN = []
    columns = ['parentSN', 'parCompType']
    serial_numbers_parent = []
    list_of_children_SN = []
    serial_numbers_1 = []
    serial_numbers_2 = []
    serial_numbers_3 = []
    serial_numbers_3 = []
    list_of_children_SN = []
    
    for i in range(len(list_of_SN)):
        list_of_parent_SN = np.append(list_of_parent_SN, "%s%s"%(args[0],list_of_SN[i]))
    print(list_of_parent_SN)
    code, serial_numbers_parent, temp = search_for_component(comp_type, list_of_parent_SN)
    print(serial_numbers_parent)
    
    for key, value in kwargs.items():
        children = np.append(children, key)
        children_comp_type = np.append(children_comp_type, value)

    for i in range(1, len(children)+1):
        columns = np.append(columns,['childSN%s'%i,'childCompType%s'%i, 'slot%s'%i])

    for i in range(len(list_of_SN)):        #Max number of children still hard coded through this
        list_of_children_SN = np.append(list_of_children_SN, "%s%s"%(args[1], list_of_SN[i]))
    code, serial_numbers_1, temp = search_for_component(children_comp_type[0], list_of_children_SN)
    #print(list_of_children_SN,serial_numbers_1)
    if len(children_comp_type) > 1:
        list_of_children_SN = []
        for i in range(len(list_of_SN)):
            list_of_children_SN = np.append(list_of_children_SN, "%s%s"%(args[2], list_of_SN[i]))
        code, serial_numbers_2, temp = search_for_component(children_comp_type[1], list_of_children_SN)
        #print(list_of_children_SN,serial_numbers_2)
        if len(children_comp_type) > 2:
            list_of_children_SN = []
            for i in range(len(list_of_SN)):
                list_of_children_SN = np.append(list_of_children_SN, "%s%s"%(args[3], list_of_SN[i]))
            code, serial_numbers_3, temp = search_for_component(children_comp_type[2], list_of_children_SN)
            if len(children_comp_type) > 3:
                list_of_children_SN = []
                for i in range(len(list_of_SN)):
                    list_of_children_SN = np.append(list_of_children_SN, "%s%s"%(args[4], list_of_SN[i]))
                code, serial_numbers_4, temp = search_for_component(children_comp_type[3], list_of_children_SN)


    for i in range(len(list_of_SN)):        #Max number of children still hard coded through this
        if len(children_comp_type) == 1:
            assemble_csv.append((serial_numbers_parent[i], comp_type, serial_numbers_1[i], children_comp_type[0], 1))
        elif len(children_comp_type) == 2:
            assemble_csv.append((serial_numbers_parent[i], comp_type, serial_numbers_1[i], children_comp_type[0], 1, serial_numbers_2[i], children_comp_type[1], 1, ))
        elif len(children_comp_type) == 3:
            assemble_csv.append((serial_numbers_parent[i], comp_type, serial_numbers_1[i], children_comp_type[0], 1, serial_numbers_2[i], children_comp_type[1], 1, serial_numbers_3[i], children_comp_type[2], 1, ))
        elif len(children_comp_type) == 4:
            assemble_csv.append((serial_numbers_parent[i], comp_type, serial_numbers_1[i], children_comp_type[0], 1, serial_numbers_2[i], children_comp_type[1], 1, serial_numbers_3[i], children_comp_type[2], 1, serial_numbers_4[i], children_comp_type[3], 1))

    df = pd.DataFrame(assemble_csv,columns=columns)
    df.to_csv('csv_files/%s/assemble_%s.csv'%(file_save,file_save))


def assembly_multi_slot(start, stop, list_of_altid, list_of_SN, comp_type, file_save, altid_name, slot_nr, child_altid,**kwargs):
    '''
    needs:  -list of the alternitive identifiers
            -the component type you want to assemble of
    creats: -CSV file that can be uploaded into the streamlit app in multi assemble set
    '''
    assemble_csv = []
    children = []
    children_comp_type = []
    list_of_parent_SN = []
    columns = ['parentSN', 'parCompType']
    list_of_children_SN = []
    serial_numbers_1 = []
    list_of_children_SN = []
    list_of_parent_SN = []
    
    #print(list_of_altid)
    for i in range(0, stop-start, slot_nr):
        #print(list_of_altid[i])
        list_of_parent_SN.append('%s%s-%s'%(altid_name,list_of_altid[i],list_of_altid[i+19]))
    code, list_of_parent_SN, temp = search_for_component(comp_type, list_of_parent_SN)
        
    
    for key, value in kwargs.items():
        children = np.append(children, key)
        children_comp_type = np.append(children_comp_type, value)
        #print(children, children_comp_type)

    if len(list_of_SN) >= 20:
        for i in range(1, slot_nr+1):
            columns = np.append(columns,['childSN%s'%i,'childCompType%s'%i, 'slot%s'%i])
    else:
        for i in range(1, len(list_of_SN)+1):
            columns = np.append(columns,['childSN%s'%i,'childCompType%s'%i, 'slot%s'%i])

    for i in range(len(list_of_SN)):        #Max number of children still hard coded through this
        list_of_children_SN = np.append(list_of_children_SN, "%s%s"%(child_altid, list_of_SN[i]))
    code, serial_numbers_1, temp = search_for_component(children_comp_type[0], list_of_children_SN)
    #print(list_of_children_SN,serial_numbers_1)

    assemble_csv_1 = []
    for i in range(len(list_of_parent_SN)):        #Max number of children still hard coded through this
        assemble_csv_1 = np.append(assemble_csv_1, [list_of_parent_SN[i], comp_type])
        #print(assemble_csv_1)
        print(len(list_of_SN)-i*20)
        if len(list_of_SN)-i*20 >= 20:
            for j in range(i*20,i*20+slot_nr):
                print(serial_numbers_1[j-1])           
                assemble_csv_1 = np.append(assemble_csv_1, [serial_numbers_1[j], children_comp_type[0], j+1-i*20])
                print(assemble_csv_1)
        else:
            for j in range(i*20,len(list_of_SN)):
                print(serial_numbers_1[j-1])        
                assemble_csv_1 = np.append(assemble_csv_1, [serial_numbers_1[j], children_comp_type[0], j+1-i*20])
                print(assemble_csv_1)
        assemble_csv.append(assemble_csv_1)
        assemble_csv_1 = []
    print(assemble_csv)

    df = pd.DataFrame(assemble_csv,columns=columns)
    df.to_csv('csv_files/%s/assemble_%s.csv'%(file_save,file_save))

def register_TB(start, stop, list_of_altid, comp_type, file_save, altid_name, slot_nr, **kwargs):
    '''
    needs:  -start and stop position of components you want to read in (int)
            -list of the alternative ID
            -the component type you want to upload (string)
            -the name the output csv shall have
            -the name of the alternative identifier like CB for Cooling_Block
            -for kwargs the property keys need to be given {"property1_key":'',"property2_key":'',...}

    return: -CSV file that can be uploaded into the streamlit app in register component
    '''

    array = []
    print(list_of_altid)
    for i in range(0, stop-start, slot_nr):
        print(list_of_altid[i])
        array.append('%s%s-%s'%(altid_name,list_of_altid[i],list_of_altid[i+19]))

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

    columns = ['project','subproject','institution','componentType','type']
    columns = np.append(columns,prop_key)

    for i in range(0,len(range(start,stop-1,slot_nr))):
        print()
        for j in range(len(prop)):
            if prop[j] == 'PART_NUMBER':
                print(i,j)
                print(prop[j])
                print(array[i])
                pre_reg = np.append(pre_reg,[prop[j],'%s'%(array[i])])
            else:
                pre_reg = np.append(pre_reg,[prop[j],array[i][j]])
                
        pre_reg_1 = ('P','PB','BONN',comp_type,comp_type)
        pre_reg_1 = np.append(pre_reg_1,pre_reg)
        register.append(pre_reg_1)

        pre_reg = []
        pre_reg_1 = []


    df =  pd.DataFrame(data=register,columns=columns)
    df.to_csv("csv_files/%s/register_%s.csv"%(file_save,file_save))
