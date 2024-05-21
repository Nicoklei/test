#!/usr/bin/env python3
### Author: Ian Dyckes, with help from Matthew Gignac and Bruce Gallop, API update by Craig Sawyer
###
### Pulls the ABC configuration used during probe tests from the production DB, then writes an ITSDAQ config.
### Finds hybrid in DB, iterates through children, finds ABCSTARV1 serials, pulls their info, and writes the itsdaq config.
###
### Can give hybrid assembly's local name OR serial number.
###
### Example usage:
### python getAsicConfig.py --serial 20USBHX2000791
### python getAsicConfig.py --local GPC1938_X_002_B_H2

if __name__ == '__main__':
    from __path__ import updatePath
    updatePath()
    
import os
import pathlib
import sys

import itk_pdb.dbAccess as dbAccess

############################################    
############################################    
############################################    

def getHybridJSON(hybridSerial):
    ### Get full info on hybrid
    try:
        hybridJSON = dbAccess.doSomething(action='getComponent',method='GET',data={"component":hybridSerial})
    except dbAccess.dbAccessError as e:
        print("Failed when trying to get STAR Hybrid Assembly info from the DB.  Serial:", hybridSerial, e)
        sys.exit("Exiting!")

    return hybridJSON

def main(local=None, serial=None, verbose=False, outDir="./hybrid_configs/", speed640=False, encode=False):

    ### DB verbosity.
    if verbose:
        dbAccess.verbose = True
        
    ### Get DB token
    if os.getenv("ITK_DB_AUTH"):
        dbAccess.token = os.getenv("ITK_DB_AUTH")

    ### Can provide the serial of a single hybrid
    if serial:
        hybridSerial = serial
        
    ### Can provide the local name of a single hybrid.
    elif local: 
        ### Find the STAR Hybrid Assembly matching this local name and type.
        matchingList = getHybridAssemblyByLocalName(local)
        
        if len(matchingList)==0:
            print("Found no STAR Hybrid Assembly in the database matching local name:", local)
            sys.exit("Exiting!")
        elif len(matchingList)>1:
            print("Found multiple STAR Hybrid Assemblies in the database matching local name:", local,". Maybe provide the serial instead!")
            print("Or maybe add a check here of the institute to see if only one is yours.")
            sys.exit("Exiting")
        matching = matchingList[0]
        hybridSerial = matching['serialNumber'] # serial of STAR Hybrid Assembly matching this local name.
        print("Found exactly one STAR Hybrid Assembly matching this local name with serial:", hybridSerial)

    ### Not enough info provided
    else:
        sys.exit("Must provide either a --serial or --local of a single STAR Hybrid Assembly!  Exiting!")

    hybridJSON = getHybridJSON(hybridSerial)

    ### Get test results for all ABCs on the hybrid
    testType = "DAC_TEST"
    testResults = getAsicTestResults(hybridJSON, testType) # list of dictionaries.  Includes position on hybrid and all config info.

    testType = "IMUX_TEST"
    imuxResults = getAsicTestResults(hybridJSON, testType)

    ### Careful about maintaining order! Should be 9 to 0!  Sort.
    ### Does order matter?  Position is an int, so should sort properly.
    testResults = sorted(testResults, key=lambda d: d['position'], reverse=True)

    positions = [d['position'] for d in testResults]
       
    ### Check HCCStar version (v0 or v1).
    ### Technically, both could be assembled to a single hybrid b/c they are separate child slots, but no one should do this.
    if allChildrenAssembled(hybridJSON, 'HCCSTARV1'):
        print("An HCCStarV1 chip is assembled.  Will set chipset, mask, and order accordingly.")
        chipset = 10 # ABCSTARV1 and HCCSTARV1
    elif allChildrenAssembled(hybridJSON, 'HCCSTAR'): 
        print("An HCCStarV0 chip is assembled.  Will set chipset, mask, and order accordingly.")
        chipset = 9 # ABCSTARV1 and HCCSTARV0
    else: # No HCC virtually assembled (not forcing HCC to be assembled since some HCCSTARV0 had issues with DB vs. actual fuse IDs)
        print("No HCC is assembled to this hybrid.  Will assume it is HCCStarV0 and will set chipset, mask, and order accordingly")
        chipset = 9 # ABCSTARV1 and HCCSTARV0

    ### if chipset==10 (PPB, ABCSTARV1 and HCCSTARV1), have to reverse Order line, so 1-10, not 9-0 like PPA (chipset 9).
    if chipset==10:
        positions = list(reversed(positions))

    ### Now write itsdaq config
    hybridConfig = hybrid_header(chipset, positions, speed640, encode)

    ### if chipset==10 (PPB, ABCSTARV1 and HCCSTARV1), have to reverse order of ABC configuration blocks... and number 0-9, not 1-10...
    if chipset==10:
        testResults = reversed(testResults) # May want to recast as a list like I do for positions.
    
    for abc in testResults: # abc is a dictionary.
        location = abc['position']
        results = {result["code"]:result["value"] for result in abc['testJSON']['results']} # get just the vital info.

        imuxChipResult = {res["code"]:res["value"]
                          for iabc in imuxResults
                          for res in iabc['testJSON']['results']
                          if iabc['position'] == location}

        if chipset==10:
            location = abc['position']-1 # still have to be numbered 0-9 for some reason, not 1-10...           

        chip = "###### \n"
        chip =  f"Chip {location} : Act. Comp. T_range Mask_r Drive PR LP LCB_Threshold\n"
        chip += "            1    0     0       0      4     1  1  134\n"
        chip += "Delay: Delay DelStep VThr VCal CalPol Latency BCOffset MaxCluster\n"
        chip += "       13\t2\t13\t0\t0\t3\t65\t-1\n"
        chip += "Bias : BVREF\tBIREF\tB8REF\tCOMBIAS\tBIFEED\tBIPRE\tADC_BIAS\tLDOD\tLDOA\n"

        dac_names = ['VREF_DAC', 'IREF_DAC', 'R8B_DAC', 'COM_DAC', 'LDOD_DAC', 'LDOA_DAC']
        dacs = [int(results[d_n]) for d_n in dac_names]
        # BIFEED, BIPRE, ADC_BIAS
        dacs[4:4] = [15, 6, int(imuxChipResult['ADC_RANGE_BEST'])]
        chip += "       " + "\t".join("%d" % d for d in dacs) + "\n"
        chip += "######\n"
        hybridConfig+=chip

    ### Save the config
    outDir = pathlib.Path(outDir)
    if not os.path.exists(outDir):
        os.mkdir(outDir)
    # Current itsdaq doesn't like module name starting with 2
    # Also useful to let it know it's a serial number
    outFile = outDir / ('SN'+hybridSerial+'.det')
    print("Saving itsdaq config to", outFile)
    with open(outFile,"w") as f:
        f.write(hybridConfig)

        
##########################################
##########################################
##########################################

### Looks up hybrid assemblies in the database with given local name.
### Returns list of matching elements.  Hopefully only ever of length 0 or 1.
def getHybridAssemblyByLocalName(local):
  
    try:
            d = {
                "project": "S",
                "componentType": "HYBRID_ASSEMBLY",
                "propertyFilter": [
                    {
                	"code": "LOCAL_NAME",
                	"operator": "=",
                	"value": local
                    }
                ]
            }
            result = dbAccess.doSomething("listComponentsByProperty",method='GET',data=d)
    except dbAccess.dbAccessError as e:
        sys.exit("\nFailed when looking for existing hybrid with local name", local, " in database.  Exiting.", e)

    matching = result["pageItemList"]
    
    return matching # this is a list of matching components.


############################################    
############################################    
############################################    
        
### Get results for <testType> test for all ASICs on hybrid with serial <hybridSerial>.
### Returns a list of dictionaries.  Each element is of the form {'serial':<ABC serial>, 'position':<ABC position>, 'testType':<testType>, "testJSON": <full test JSON>}
def getAsicTestResults(hybridJSON, testType):
        

    ### Check if all ABCSTARV1 are assembled to the hybrid
    if not allChildrenAssembled(hybridJSON, 'ABCSTARV1'):
        print("Not all ABCSTARV1 chips were assembled in the database.  Fix this first!.")
        # continue
        sys.exit("Exiting!")

    ### Declare output list (use list instead of dict b/c order matters.  Could use an orderedDict I guess...).
    abcConfigList = []
    
    ### Go through ABCSTARV1 children and get info on each.
    for child in hybridJSON['children']:
        thisType = child['type']['code']
        if not thisType=="ABCSTARV1":
            continue
        if child['component']: # already assembled a chip here, else it's null.  Should be true due to check earlier.
            existingChipSerial = child['component']['serialNumber']
            existingChipPosition = [prop["value"] for prop in child['properties'] if prop['code']=="ABC_POSITION"][0]
            maybeExistingChipWafer = [prop["value"] for prop in child['properties'] if prop['code']=="WAFER_NUMBER"]
            if len(maybeExistingChipWafer) == 1:
                existingChipWafer = maybeExistingChipWafer[0]
            else:
                existingChipWafer = "UNKNOWN"
            print(f"Found ABCStarV1: {existingChipSerial}, position: {existingChipPosition}, wafer: {existingChipWafer}")
            
            ### Get all runs matching testType.
            try:
                #update from Craig for new API
                #testRuns = dbAccess.doSomething(action="listTestRunsByComponent",method='GET', data={'component': existingChipSerial, "testType":testType} )
                testRuns = dbAccess.doSomething(action="listTestRunsByComponent",method='GET', data={"filterMap": {"serialNumber": existingChipSerial, "state": ["ready", "requestedToDelete"], "testType": testType}} )
            except dbAccess.dbAccessError as e:
                print("Failed when trying to get test info from the DB for ABCSTARV1 with serial:", existingChipSerial, "and test type:", testType, e)
                sys.exit("Should not happen, so exiting.")

            ### Now get all the info from a particular run.
            ### Not sure how to handle multiple runs of the same test.  Maybe just pull the latest one (highest run number)?  Sort first?
            #update from Craig for new API
            #run =  testRuns['pageItemList'][-1] # get latest run if multiple?
            run =  testRuns['itemList'][-1] # get latest run if multiple?
            runNumber, runID = run["runNumber"], run['id']
            try:
                runInfo = dbAccess.doSomething(action="getTestRun",method='GET', data={'testRun': runID} )
            except dbAccess.dbAccessError as e:
                print("Failed to get results for following test. Test code/type:", testType, ", Run:", runNumber, ", ID:", runID, e)
                sys.exit("Exiting.")

            ### Convert existingChipPostion to an integer if necessary.  Some may use this format: ABC_<hybrid_type>_<chip_number>
            try:
                existingChipPosition = int(existingChipPosition)
            except ValueError:
                try:
                    existingChipPosition = int(existingChipPosition.split('_')[-1])
                except ValueError:
                    print("Cannot parse this chip's position property:", existingChipPosition)
                    print("Not an integer or in the ABC_<hybrid_type>_<chip_number> format.")
                    sys.exit("Exiting!")
            
            ### Return everything.
            resultsDict =  {'serial':existingChipSerial, 'position':existingChipPosition, 'testType':testType, "testJSON": runInfo}
            
            abcConfigList.append( resultsDict )
            
            
    return abcConfigList

################################
################################
################################

def allChildrenAssembled(hybridJSON, childType): # Use 'type' instead of component type to differentiate ASIC versions.
        
    ### First get the number of slots for this child type.
    nChildSlots = len([child['type']['code'] for child in hybridJSON['children'] if child['type']['code']==childType])
    print("Number of", childType, "child slots:", nChildSlots)
    if nChildSlots==0:
        print("No child slots of type:", childType)
        sys.exit("Exiting!")
    
    nAssembled = 0
    for child in hybridJSON['children']:
        if not child['type']['code']==childType: # skip any child that doesn't match the desired child type.
            continue
        if child['component']: # None if nothing assembled in this slot.
            if not child['component']['serialNumber']: # somehow someone assembled a chip without a serial somehow??? So add this check
                continue
            if childType=="ABCSTARV1": # then position of chip matters.
                position = [prop['value'] for prop in child['properties'] if prop['code']=='ABC_POSITION'][0]
                print("Already an ABCStarV1 assembled to position", position )
            nAssembled += 1
            
    if childType=="ABCSTARV1":                
        if not nAssembled == nChildSlots:
            print("Only found", nAssembled, childType, "already assembled.  Expect ", nChildSlots, ". Please assemble more first.")
            return False
        else:
            print("Found", nAssembled, childType, "already assembled.")
            return True
    else: # only expect 1 of these.
        if nAssembled==0:
            print("Did not find any", childType, "already assembled.  Please assemble more first.")
            return False
        else:
            print("Found", nAssembled, childType, "already assembled.")
            return True
    
####################
####################
####################

def hybrid_header(chipset, positions, speed640, encode):
    chipMask = 0
    for p in positions:
        chipMask |= 1 << p

    ### Default:
    ### trigger mode = single level trigger and
    ### encode cntl = use register to control output encoding
    r4142 = 0b010000000000000001

    # speed
    speed = 320
    if speed640:
        speed = 640
        r4142 |= 1 << 4

    # 8b10b encoding
    if encode:
        r4142 |= 1 << 17        

    header  = "Module : Chipset \n"
    header +=f"           {chipset} \n \n"
    
    header += "# Speed of readout from HCC \n"
    header += f"Speed {speed} \n \n"
    
    header += "HCC 15 auto \n \n"
    
    header += "#   R32        R33        R34        R35 \n"
    header += "    0x02400000 0x44444444 0x00000444 0x00ff3b05 \n"
    header += "#   R36        R37        R38        R39 \n"
    header += "    0x00000000 0x00000004 0x0fffffff 0x00000014 \n"
    header += "#   R40        R41        R42        R43 \n"
    header += "    0x%08x 0x%08x 0x%08x 0x00000000 \n" % (chipMask, r4142, r4142)
    header += "#   R44        R45        R46        R47 \n"
    header += "    0x0000018e 0x00710003 0x00710003 0x00000000 \n"
    header += "#   R48 \n"
    header += "    0x00406600 \n \n"

    header += "Order " + ' '.join([str(x) for x in positions]) + " \n \n"
    
    return header


################################
################################
################################

if __name__ == "__main__":
    ### arguments
    import argparse
    parser = argparse.ArgumentParser(description='For pulling ABC configuration during probe testing from DB and writing itsdaq config.')
    parser.add_argument('--local', default=None, help='Local name of STAR Hybrid Assembly (e.g. GPC1938_X_009_A_H1).')
    parser.add_argument('--serial', default=None, help='Serial name of STAR Hybrid Assembly.')
    parser.add_argument('--verbose', default=False, action='store_true', help='Increase verbosity of DB interactions.')
    parser.add_argument('--speed640', default=False, action='store_true', help='Increase speed to 640 MHz.')
    parser.add_argument('--encode', default=False, action='store_true', help='Use 8b10b encoding.')
    parser.add_argument('--outDir', default='./hybrid_configs/', help='Output directory for configs.')
    args = parser.parse_args()
    ###
    main(args.local, args.serial, args.verbose, args.outDir, args.speed640, args.encode)
