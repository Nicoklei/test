#!/usr/bin/env python3
# Author: Bruce Gallop, after Ian Dyckes (assembleHybridbyFuseIDs)
#
# Originally written for assembling ASICs onto strip hybrids.
#
# In order to assemble something, we need:
#   A reference to the parent
#   A reference to the child
#   A reference to the slot
#
# We get these by describing each in a custom json format.
#
import argparse
import json
import os
import sys

import itk_pdb.dbAccess as dbAccess

def get_component(sn = None, **args):
    alt_id = args.get("alt_id")
    print("DB: GetComponent %s" % (sn or alt_id))

    try:
        if sn is not None:
            return dbAccess.doSomething("getComponent", method="GET",
                                        data={"component": sn})
        elif alt_id is not None:
            return dbAccess.doSomething("getComponent", method="GET",
                                        data={"component": alt_id,
                                              'alternativeIdentifier':True})
        sys.exit("Request to get component with no sn or alt_id! (%s!" % (args))

    except dbAccess.dbAccessError:
        sys.exit("Failed to get component info %s! Exiting!" % (sn or alt_id))

def do_disassemble_component(parent, child):
    print("DB: Disassemble component %s from %s" % (child, parent))

    try:
        dbAccess.doSomething(action='disassembleComponent',method='POST',
                             data={"parent": parent, "child": child})
    except dbAccess.dbAccessError:
        sys.exit("Failed to disassemble %s from %s" % (child, parent))

def do_assemble_component(parent_id, slot_id, child_id, child_props):
    data = {'parent': parent_id,
            'child': child_id,
            'properties': child_props}

    if slot_id is None:
        print("DB: Assemble singular component %s on %s" % (child_id, parent_id))

        action = "assembleComponent"
    else:
        print("DB: Assemble component %s on %s in slot %s" % (child_id, parent_id, slot_id))

        action = "assembleComponentBySlot"
        data['slot'] = slot_id

    print(json.dumps(data, indent=4))

    try:
        dbAccess.doSomething(action=action,
                             method='POST',
                             data=data)
    except dbAccess.dbAccessError:
        print("\n---")
        sys.exit("Assembly failed!  Exiting!")

def find_parent(p_desc, p_ref):
    print("Getting information for parent from the DB.\n")

    if type(p_desc) is str:
        # Just look up the component using string
        return get_component(p_desc)

    if "property" in p_desc:
        if p_ref is None:
            sys.exit("If using property lookup for parent, need reference on command line")

        # Find by reference to property of some other component
        if "value" not in p_desc:
            sys.exit("If looking up parent by property, need a value to compare")

        comp_type = p_desc.get("type")

        prop_name = p_desc["property"]
        prop_val = p_desc["value"]

        ref_info = get_component(p_ref)

        if "children" not in ref_info:
            sys.exit("Reference component for parent property lookup has no children slots")

        print(f"Find {prop_name} {prop_val} in {len(ref_info['children'])} slots")

        for ref_child in ref_info["children"]:
            if not ref_child["component"]:
                # No assembled component in this slot
                continue

            if not ref_child["component"]["serialNumber"]:
                # No SN in this slot
                continue

            ref_type = ref_child['componentType']['code']
            if comp_type is not None and ref_type != comp_type:
                # Wrong type
                continue

            ref_values = [prop['value']
                         for prop in ref_child['properties']
                         if prop['code'] == prop_name]
            if len(ref_values) != 1:
                print("Found properties: ", [f["code"] for f in ref_child['properties']])
                sys.exit(f"Failed to find {prop_name} property in comp {p_ref}")

            ref_value = ref_values[0]

            if ref_value != prop_val:
                continue

            child_serial = ref_child['component']['serialNumber']

            print(f"Found {child_serial}")

            return get_component(child_serial)

        sys.exit(f"TBD look up via reference panel {comp_type} {prop_name} {prop_val}")

    sys.exit(f"Don't know how to find parent from {p_desc}")

def find_parents_of_child(child_info):
    return {parent["componentType"]["code"]: parent['component']
            for parent in child_info['parents']
            if parent['component']}

def find_slot(s_desc, parent_info):
    """
    Find slot to assemble to in parent.

    @param s_desc Description of the slot
    @param parent_info Parent compoonent data
    """
    slot_type = s_desc["type"]

    # Find slots of appropriate type
    slot_children = [child for child in parent_info['children']
                     if child['type']['code'] == slot_type]

    slot_order = s_desc["order"]

    slot_children = [child for child in slot_children
                     if child["order"] == slot_order]

    if len(slot_children) != 1:
        print(f"Failed slot lookup {s_desc}")
        print(f" in {parent_info['children']}")
        print(f" is {slot_children}")
        sys.exit("Slot lookup did not identify single entry")

    return slot_children[0]

def assemble_component(desc, args):
    if "parent" not in desc:
        sys.exit("Failed to find parent ID in json options")

    parent = find_parent(desc["parent"], args.reference)

    if "children" not in desc:
        sys.exit("No chilren components specified to assemble")

    if "disassemble" in desc:
        disassemble_types = desc["disassemble"]
    else:
        disassemble_types = []

    default_properties = desc.get("properties", {})

    for c_desc in desc["children"]:
        print('---')

        assemble_child(c_desc, parent, disassemble_types, default_properties, args)

def assemble_child(c_desc, parent_info, disassemble_types, default_properties, args):
    """
    Assemble child onto parent.

    @param c_desc Description of the child and slot.
    @param parent_info Parent component.
    @param args Used to pass global parameters.
    """

    if "alt_id" in c_desc:
        child_info = get_component(alt_id = c_desc["alt_id"])
    else:
        child_info = get_component(sn = c_desc["sn"])

    parent_serial = parent_info['serialNumber']
    child_serial = child_info['serialNumber']

    ### Check institute.
    parent_institution = parent_info['institution']['code']
    parent_location = parent_info['currentLocation']['code']
    child_location = child_info['currentLocation']['code']

    if not child_location == parent_institution and not child_location == parent_location:
        print(f"Child is located at {child_location}, but the parent is currently located at {parent_location} and belongs to {parent_institution}.")
        sys.exit("The location of parent and child must match in order to do assembly.  Exiting!")

    parent_type = parent_info['componentType']['code']

    # Get list of parent component types
    child_parents = find_parents_of_child(child_info)

    ### Check if this child is already assembled to a component of correct type.
    if parent_type in child_parents.keys():
        poss_parent = child_parents[parent_type]
        poss_parent_serial = poss_parent['serialNumber']

        print(f"The child is already assembled to a component with serial {poss_parent_serial}!!!")

        ### check if the parent to which this child is already assembled matches the expected parent.
        if poss_parent_serial == parent_serial:
            print("This child is already assembled to the correct parent (not checked the slot)!")
        else:
            sys.exit('This child is already assembled to a different parent!!!')

        ### Either way, no more assembly to do right now, so continue to the next child.
        return

    # Check if this child is still assembled to something else (eg SHIPPING_CONTAINER)
    bad_parents = {ty: cp for ty, cp in child_parents.items()
                   if ty in disassemble_types}

    for ty, cp in bad_parents.items():
        container_sn = cp['serialNumber']
        print(f"This child is still assembled to a {ty} with serial {container_sn}.  Disassembling.")

        if not args.dryRun:
            do_disassemble_component(container_sn, child_serial)
        else:
            print("DRY RUN: skip disassembly")
        del child_parents[ty]

    if len(child_parents) > 0:
        print(f"Parents of child {child_serial}: {child_parents.keys()}")
        sys.exit("Child is still assembled to unexpected parent")

    # Now, need to pick a slot on the parent component
    # If there's no description of slot, then must be only one possibility
    slot_id = None

    if "slot" in c_desc:
        slot_info = find_slot(c_desc["slot"], parent_info)
        slot_id = slot_info["id"]

        print(f"   slot ID {slot_id}")

    print(f"Now assembling {child_serial} to the specified position ({slot_id}) to the specified parent ({parent_serial}).")

    # If there are properties to attach to the slot, pull them in (no processing)
    child_props = c_desc.get("properties", default_properties)

    if not args.dryRun:
        do_assemble_component(parent_serial, slot_id, child_serial, child_props)
        print(f'Successfully assembled {child_serial} to {parent_serial}!')
    else:
        print("DRY RUN: skip assembly")

help_text = """
The format for the json assembly description is custom to this command.

In order to assemble something, we need three things:
* A reference to the parent
* A reference to the child
* A reference to the slot (optional if only one possible slot)

At the top-level the file contains either an object description of these three
things, or a list of a sequence of these objects.

Each description object can have: "parent", "children", "properties", and
"disassemble".

The "parent" describes the parent to be assembled to. It can be a simple
string which will be looked up directly as a component. Otherwise, the parent
can be looked up by property, with reference to the component provided via
the --reference argument. In this case "property" is the name of the property,
"value" is the value to check for, and an option "type" can be used to allow
only a particular (child) component type.

The "children" field describes both the child component to be assembled onto
the given parent component, and which slot to be used (if there is more than
one available). The child component is found by either "sn" or "alt_id".
The "slot" field of the children object describes the slot a component should
be assembled to, with the "type" and "order" fields. The optional "properties"
field can be used to specify slot properties.

If the "properties" field is present in the top-level object, this provides
the slot properties to be used for assembly when not provided in the children
section.

If the "dissassemble" field is present, then this lists the types of components
that a prospective child should be dissassembled from (otherwise this is an
error).
"""

def main():
    ### arguments
    parser = argparse.ArgumentParser(
        description='Assembly component(s) to a parent component given description.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog = help_text,
    )

    parser.add_argument('--json', required=True, help='Description of components to assemble and what slots to use.')
    parser.add_argument('--reference', default=None, help='Serial number of parent reference (eg lookup parent as position in panel).')
    parser.add_argument('--verbose', default=False, action='store_true', help='Increase verbosity on DB interactions.')
    parser.add_argument('--dryRun', default=False, action='store_true', help='Perform a dry run.  Do not update anything in the DB.  Read only.')

    args = parser.parse_args()

    ### DB access.
    if os.getenv("ITK_DB_AUTH"):
        dbAccess.token = os.getenv("ITK_DB_AUTH")
    if args.verbose:
        dbAccess.verbose = True

    desc = json.load(open(args.json))

    # Assemble everything to one parent (Could be a list)
    if type(desc) is list:
        print("Start iterating through the assembly json...")
        for comp in desc:
            assemble_component(comp, args)
        print(" ... complete assembly json iteration")
    else:
        print("Do assembly to singular parent...")
        assemble_component(desc, args)
        print(" ... done assembly")

    print("Done assembling components.")

if __name__ == "__main__":
    main()
