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

def check_doors(ifc_file,door_width_metres=0.9):
    #TODO: finish door accessibility criteria
    
    doors = ifc_file.by_type("IfcDoor")
    doors_major = []
    doors_minor = []
    doors_ok = []

    units = util.get_project_units(ifc_file)[0]
    unitscale = util.get_project_units(ifc_file)[1]
    

    for door in doors:
        handicap_accessible = ifcopenshell.util.element.get_psets(door).get("HandicapAccessible")
        min_width = door_width_metres * unitscale #convert project units to metres
        if door.OverallWidth < min_width:
            doors_minor.append([util.get_id(door),door.Name,f"Reduce width by {door.OverallWidth - min_width} {units}"])
            continue
        
        if not handicap_accessible:
            doors_major.append([util.get_id(door),door.Name,"Make Door with Handicap Friendly Materials"])
            continue
        
        else:
            doors_ok.append([util.get_id(door),door.Name,door.OverallWidth])

    return doors,doors_major,doors_minor,doors_ok


def check_floors(ifc_file,floor_height_metres=0.15):

    #TODO:find major slab and minor slabs
    

    floors_major = []
    floors_minor = []
    floors_ok = []

    units = util.get_project_units(ifc_file)[0]
    unitscale = util.get_project_units(ifc_file)[1]

    floor_height = floor_height_metres * unitscale

    print (f"Floor Height Difference to be checked= {floor_height} {units}")




    #slabs_by_storeys = util.get_elements_wrt_storey(ifc_file,"IfcSlab")
    slabs_by_storeys = util.get_elements_wrt_storey(ifc_file,"IfcSlab")

    storeys = ifc_file.by_type("IfcBuildingStorey")

    storeys.sort(key=lambda x: x.Elevation)

    
    """
    for storey in storeys:
        print (storey)
    """
    
    for storey in storeys:
        temp = []
        floors = []
        #print (storey.Name)
        
        if storey in slabs_by_storeys.keys():
            #print (storey)
            
            slabs = slabs_by_storeys[storey]
            for slab in slabs:
                temp.append(util.get_top_elevation(slab))
                #print(util.get_top_elevation(slab))
                floors.append(slab)
            
            
            
            deviations = util.find_deviations(temp,floor_height)
            print (deviations)
            
            floor_height_average = util.find_mode(temp)
            print(floor_height_average)
            """
            for dev in deviations:
                floor_indices = temp.index(deviations)
                for index in floor_indices:
                    floors_major.append([util.get_id(floors[index]),floors[index].Name,f"Change height by {floor_height_average - dev} {units}"])
            """

    return slabs_by_storeys,floors_major,floors_minor,floors_ok
    
    
    
    
    

