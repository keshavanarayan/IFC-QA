import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.shape
import ifcopenshell.util.element
import ifcopenshell.util.constraint
import ifcopenshell.util.unit
import ifcopenshell.entity_instance
import ifcopenshell.util

import util.ifc_util as util



settings = ifcopenshell.geom.settings()

#TODO:use dir(element) to find attributes of elements


def check_doors(ifc_file):
    #TODO: finish door accessibility criteria
    doors = ifc_file.by_type("IfcDoor")

    

    doors_major = []
    doors_minor = []
    doors_ok = []

    units = util.get_project_units(ifc_file)[0]
    unitscale = util.get_project_units(ifc_file)[1]
    

    for door in doors:
        handicap_accessible = ifcopenshell.util.element.get_psets(door).get("HandicapAccessible")
        min_width = 0.9 * unitscale #convert project units to metres
        if door.OverallWidth < min_width:
            doors_minor.append([util.get_id(door),door.Name,f"Reduce width by {door.OverallWidth - min_width} {units}"])
            continue
        
        if not handicap_accessible:
            doors_major.append([util.get_id(door),door.Name,"Make Door with Handicap Friendly Materials"])
            continue
        
        else:
            doors_ok.append([util.get_id(door),door.Name,door.OverallWidth])

    return doors,doors_major,doors_minor,doors_ok


def check_floors(ifc_file):

    #TODO:find major slab and minor slabs
    
    floors = ifc_file.by_type("IfcSlab")

    floors_major = []
    floors_minor = []
    floors_ok = []

    floors_list = []

    # Create a dictionary to map elements to their containing structure (storey)
    element_to_storey = util.element_wrt_storey(ifc_file)

    for floor in floors:

        current_storey = element_to_storey.get(floor)


    return floors,floors_major,floors_minor,floors_ok
    

