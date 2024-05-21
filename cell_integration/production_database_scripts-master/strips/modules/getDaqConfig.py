#!/usr/bin/env python3
### Author: Bruce Gallop, simplified version of getAsicConfig.py
###
### Pulls the ASIC configuration produced during probe tests.
###
### Example usage:
### python getDAQConfig.py ABC42f046 HCC40106a AMAC40502f 0x00005044

if __name__ == '__main__':
    from __path__ import updatePath
    updatePath()

import json
import os
import pathlib
import sys

import itk_pdb.dbAccess as dbAccess

# Pattern matching to get ASIC type from serial
import re
re_sn_abc = re.compile('20USGAA[0-9]+')
re_sn_hcc = re.compile('20USGAH[0-9]+')
re_sn_amac= re.compile('20USGAM[0-9]+')
# Store info for debugging (first object for stats)
auxInfo = [{}]

component_map = {}

def find_parent_sn(component_json):
    '''
    Find parent SN of component
    '''

    sn = None
    if ('parents' not in component_json or component_json['parents'] is None):
        return None
    else:
        plist = component_json['parents']
        for pi in plist:
            # No component in parent slot or Parent component has no serialNumber
            if (pi['component'] is None or 'serialNumber' not in pi['component']):
                continue
            sn = pi['component']['serialNumber']
        
    return sn

def get_component_json(identifier):
    '''
    Get component json.
    if component contains SN, don't use alternativeIdentifier
    '''
  
    data = {'component' : identifier}

    if 'ABC' in identifier or 'HCC' in identifier or 'AMAC' in identifier:
        # This is the alternative identifier of an ASIC
        data["alternativeIdentifier"] = True

    # ABCv2a are hex "0x00005044"
    if len(identifier) == 10:
        try:
            int(identifier, 16)
            data["alternativeIdentifier"] = True
        except ValueError:
            pass

    try:
        component_json = do_get_component(data)
    except dbAccess.dbAccessError as e:
        print(f'Failed when trying to get component {identifier} info from the DB. Error {e}')
        sys.exit("Exiting!")

    return component_json

def build_family_tree(asicJSON, fuse):
    '''
    Builds family tree for ASIC
    Will find parent, grandparent, and great-grandparent if they exist
    '''

    print(f'Building family tree for ASIC {fuse}')

    family_members = parent_list()

    family_member_json = asicJSON
    family_SNs = []
    for family_member in family_members:
        parent_sn = find_parent_sn(family_member_json)
        family_SNs.append(parent_sn)
        if parent_sn is None:
            break

        family_member_json = get_component_json(parent_sn)

    return family_SNs

def do_get_component(data):
    """
    Call getComponent, using cache to avoid duplicate lookups.
    """

    identifier = data["component"]

    if identifier in component_map:
        chit = auxInfo[0].get("cache_hit", 0)
        auxInfo[0]["cache_hit"] = chit+1

        return component_map[identifier]

    miss = auxInfo[0].get("cache_miss", 0)
    auxInfo[0]["cache_miss"] = miss+1

    data = dbAccess.doSomething(action='getComponent',
                                method='GET',
                                data=data)

    component_map[identifier] = data
    component_map[data["serialNumber"]] = data

    return data

def find_property(properties,code, default=None):
    """
    Find the priopery value in a list of properties with a matching code.

    Return `default` if no property is found.
    """
    try:
        return next(filter(lambda prop: prop['code']==code, properties))['value']
    except StopIteration:
        return default

def find_asics(identifier):
    """
    Return the a list of ASICs associated with an identifier. The identifier can be either
    a serial number of a module, hybrid or ASIC, or an alternative identifier (aka fuse ID)
    of the ASIC itself.

    In case of an assembly (hybrid or module), all associated ASICs are returned.

    The return list will contain the serial number of the associated ASICs.
    """

    # Look up information on the identifier
    # Get full info on component
    data = get_component_json(identifier)

    asic_types = ['ABC','HCC','AMAC']
    container_types = ['HYBRID_ASSEMBLY','MODULE','PWB']
    asic_container_types = asic_types + container_types

    # Process the result
    if data['componentType']['code'] in asic_types:
        # This is a single ASIC
        return [data['serialNumber']]
    elif data['componentType']['code'] in container_types:
        # Get list of assembled children
        children=filter(lambda child: child['component'] is not None, data['children'])
        # Get list of children that are ASICs or can contain ASICs
        asicchildren=filter(lambda child: child['componentType']['code'] in asic_container_types, children)
        # Get the serial numbers of candidates
        identifiers=map(lambda child: child['component']['serialNumber'], asicchildren)
        # Recursively find ASICs in the children
        return sum(map(find_asics,identifiers),[])
    else:
        raise Exception(f"Unknown component type for {identifier} {data['componentType']['code']}")
    return []

def parent_list():
    yield "parent"

    next_name = 'grand_parent'
    while True:
        yield str(next_name)
        next_name = "great_" + next_name
        if len(next_name) > 100:
            # Unrealistic depth 
            break

def process_sn(sn):
    isABC = re_sn_abc .match(sn) is not None
    isHCC = re_sn_hcc .match(sn) is not None
    isAMAC= re_sn_amac.match(sn) is not None

    testTypes = []
    if isABC:
        testTypes = ["DAC_TEST", "IMUX_TEST"]
    elif isHCC:
        pass
    elif isAMAC:
        testTypes = ["USEFUL_PARAMETERS"]

    ### Get full info on component
    asicJSON = get_component_json(sn)

    results = {}
    auxInfo.append({f"getComponent_{sn}" : asicJSON})

    # Build family tree (should make it all the way to "top" module parent)
    family_SNs     = build_family_tree(asicJSON, sn)
    # Fill in family members and their SNs
    for family_member,family_SN in zip(parent_list(), family_SNs):
        if (family_SN is not None):
            if (family_member in results):
                print("Warning, already have a parent serial number")
                print(f"Replacing {results[family_member]['SN']} with {family_SN}")
            results[family_member] = {'SN' : family_SN}

    # Information about the ASIC itself
    results["self"] = {}
    if "alternativeIdentifier" in asicJSON:
        results["self"]["fuse"]=asicJSON["alternativeIdentifier"]
    if "serialNumber" in asicJSON:
        results["self"]["SN"]=asicJSON["serialNumber"]

    # Information about the test results
    results["test_info"] = []

    for t in testTypes:
        testResults = getAsicTestResults(sn, t)
        # In case test was empty
        if (testResults == {}): continue
        if testResults is None:
            continue

        asicInfo = {"fuse": results["self"]["fuse"],
                    "test": t}

        auxInfo.append(testResults)

        # Maybe check something in parent info?
        # location = abc['position']

        res = testResults['results']

        if t == "USEFUL_PARAMETERS":
            res = testResults["properties"]
            auxInfo.append(f"Using properties for {t}")
            auxInfo.append(res)

        if res is None:
            propDict = {}
        else:
            # Transpose results into property dictionary
            propDict = {result["code"]:result["value"]
                        for result in res}

        auxInfo.append(propDict)

        asicInfo["properties"] = propDict

        results["test_info"].append(asicInfo)

    return results

def main(identifiers, outDir, debug):
    ### Get DB token
    if os.getenv("ITK_DB_AUTH"):
        dbAccess.token = os.getenv("ITK_DB_AUTH")

    info = {}

    asics = sum(map(find_asics,identifiers),[])
    for sn in asics:
        try:
            asicInfo = process_sn(sn)
            info[asicInfo['self']['fuse']] = asicInfo
        except Exception as e:
            if not debug:
                raise

            print(f"*** Continuing through error from {sn} {e}")
            auxInfo.append(f"ERROR {e}")
            import traceback
            auxInfo.append(traceback.format_exc().split("\n"))

    ### Save the config
    outDir = pathlib.Path(outDir)
    if not os.path.exists(outDir):
        os.mkdir(outDir)

    if debug:
        outFile = outDir / "temp_info.json"
        print(f"Saving debug data to {outFile}")
        with open(outFile,"w") as f:
            json.dump(auxInfo, f, indent = 4)

    outFile = outDir / "asic_info.json"
    print(f"Saving data to {outFile}")
    with open(outFile,"w") as f:
        json.dump(info, f, indent = 4)

def getAsicTestResults(sn, testType):
    """
    Get results for <testType> test for ASIC with serial number <sn>

    Returns a dictionary containing the extracted information.
    """

    print(f"Found Chip ({testType}): {sn}")

    ### Get all runs matching testType.
    try:
        data={"filterMap":
              {"serialNumber": sn,
               "state": ["ready"],
               "testType": testType}}

        testRuns = dbAccess.doSomething(action="listTestRunsByComponent",
                                        method='GET', data=data)
    except dbAccess.dbAccessError as e:
        print(f"Failed to look up test run info for {sn} test type {testType} ({e})")
        sys.exit("Should not happen (return empty list if missing), so exiting.")

    testRunList = testRuns["itemList"]

    if testType is None:
        auxInfo.append({f"all tests for {sn}" : testRunList})
        return None

    ### Now get all the info from a particular run.
    ### Not sure how to handle multiple runs of the same test.  Maybe just pull the latest one (highest run number)?  Sort first?
    if len(testRunList) > 1:
      print(f"More than one run of type {testType}, using last")

    runInfo = {}
    # Just in case it's empty
    if (testRunList != []): 
        testRunInfo =  testRunList[-1]
        runNumber, runID = testRunInfo["runNumber"], testRunInfo['id']
        try:
            runInfo = dbAccess.doSomething(action="getTestRun",method='GET', data={'testRun': runID} )
        except dbAccess.dbAccessError as e:
            print("Failed to get results for following test.")
            print(f"Test code/type: {testType}, Run: {runNumber}, ID: {runID}, {e}")
            sys.exit("Exiting, was told the info was there!")

    ### Return everything.

    return runInfo

if __name__ == "__main__":
    ### arguments
    import argparse
    parser = argparse.ArgumentParser(description='Pull probe test data for ASICs.')
    parser.add_argument('fuse', nargs="+", type=str,
                        help='Alt ID of ASIC in Hybrid Assembly.')
    parser.add_argument('--verbose', default=False, action='store_true', help='Increase verbosity of DB interactions.')
    parser.add_argument('--debug', default=False, action='store_true', help='Save debug information).')
    parser.add_argument('--outDir', default='./daq_asics/', help='Output directory for data.')
    args = parser.parse_args()

    if args.verbose:
        dbAccess.verbose = True

    ###
    main(args.fuse, args.outDir, args.debug)
