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

def check_doors(ifc_file,door_width_mm=900,handicap_clear_mm= 1000):
    """
    A function to check door accessibility criteria.

    Parameters:
    - ifc_file: The IFC file to extract doors from.
    - door_width_mm: The width threshold for door accessibility in mm (default is 900 mm).

    Returns:
    - doors: List of all doors extracted from the IFC file.
    - doors_major: List of doors that require major modifications for accessibility.
    - doors_minor: List of doors that require minor modifications for accessibility.
    - doors_ok: List of doors that meet the accessibility criteria.
    """
    #TODO: finish door accessibility criteria
    
    doors = ifc_file.by_type("IfcDoor")
    doors_major = []
    doors_minor = []
    doors_ok = []

    units = util.get_project_units(ifc_file)[0]
    unitscale = util.get_project_units(ifc_file)[1]
    

    for door in doors:
        handicap_accessible = ifcopenshell.util.element.get_psets(door).get("HandicapAccessible")
        min_width = door_width_mm #* unitscale #TODO:convert project units to metres

        #util.get_object_placement_info(ifc_file,door)

        origin,axis,direction,problem = util.get_object_placement_info(ifc_file,door)

        #print(origin,axis,direction,problem)



        if door.OverallWidth < min_width:
            doors_minor.append([util.get_id(door),door.Name,f"Reduce width by {door.OverallWidth - min_width} {units}"])
            continue
        
        """if not handicap_accessible:
            doors_minor.append([util.get_id(door),door.Name,"Make Door with Handicap Friendly Materials"])
            continue"""

        if problem:
            doors_major.append([util.get_id(door),door.Name,f"Door {door.Name} with id {util.get_id(door)} does not have transformation attached to it"])
            continue

        else:
            bbox = util.get_box3d(origin,axis,direction,door.OverallWidth,handicap_clear_mm,door.OverallHeight)
            print(bbox)
            doors_ok.append([util.get_id(door),door.Name,"OK"])

    return doors,doors_major,doors_minor,doors_ok


def check_floors(ifc_file,floor_height_mm=150):
    """
	Check the floors in the given IFC file and return the floors that have major deviations, minor deviations, and those that are okay.
	
	:param ifc_file: The IFC file to check the floors in.
	:type ifc_file: str
	:param floor_height_metres: The floor height in metres, defaults to 0.15.
	:type floor_height_metres: float
	:return: A tuple containing the floors grouped by storeys, the floors with major deviations, the floors with minor deviations, and the floors that are okay.
	:rtype: tuple
	"""

    floors_f = []
    floors_major = []
    floors_minor = []
    floors_ok = []

    units = util.get_project_units(ifc_file)[0]
    unitscale = util.get_project_units(ifc_file)[1]

    floor_height = floor_height_mm #* unitscale #TODO:convert project units to metres

    print (f"Floor Height Difference to be checked= {floor_height} {units}")

    #slabs_by_storeys = util.get_elements_wrt_storey(ifc_file,"IfcSlab")
    slabs_by_storeys = util.get_elements_wrt_storey(ifc_file,"IfcSlab")

    storeys = ifc_file.by_type("IfcBuildingStorey")

    storeys.sort(key=lambda x: x.Elevation)

    for storey in storeys:
        temp = []
        floors = []
        #print (storey.Name)
        
        if storey in slabs_by_storeys.keys():
            #print (storey.Name)
            
            slabs = slabs_by_storeys[storey]
            for slab in slabs:
                floors_f.append(slab)
                if "Sunscreen" not in slab.Name:
                    temp.append(util.get_top_elevation(slab))
                    #print(util.get_top_elevation(slab))
                    floors.append(slab)
                else:
                    floors_minor.append([util.get_id(slab),slab.Name,f"Remove Sunscreen from Slabs with id {util.get_id(slab)} in {storey.Name}"])
            
            
            deviations = util.find_deviations(temp,floor_height)
            #print (deviations)
            
            floor_height_average = util.find_mode(temp)
            #print(floor_height_average)

            if deviations:
                for dev in deviations:
                    floor_indices = temp.index(deviations)
                    for index in floor_indices:
                        floors_major.append([util.get_id(floors[index]),floors[index].Name,f"Change height by {floor_height_average - dev} {units} in {storey.Name}"])
            else:
                for floor in floors:
                    floors_ok.append([util.get_id(floor),floor.Name,"OK"])
            
            
            

    return floors_f,floors_major,floors_minor,floors_ok
    
    
    
    
    

