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

def get_storey_heights(ifc_file):

    # Get all IfcBuildingStorey instances
    storeys = ifc_file.by_type("IfcBuildingStorey")

    # Sort the storeys by elevation
    storeys.sort(key=lambda x: x.Elevation)

    storeys_list = []


    # Iterate over each storey and extract information
    for i in range(len(storeys)-1):
        current_storey = storeys[i]
        next_storey = storeys[i+1]

        storey_name = current_storey.Name if hasattr(current_storey, "Name") else "N/A"
        storey_height = next_storey.Elevation - current_storey.Elevation

        #print(f"Storey Name: {storey_name}, Storey Height: {storey_height}")
        storeys_list.append([storey_name,storey_height])
    
    #print (f"Storey Name: {storeys[len(storeys)-1].Name}, Storey Height: Top Most Level")
    storeys_list.append([storeys[len(storeys)-1].Name,None])
    
    return storeys_list


def are_walls_vertical(ifc_file, tolerance=1e-5):

    # Get all IfcWall instances from the IFC file
    walls = ifc_file.by_type('IfcWall')
    
    non_vertical_walls = []


    # Iterate over each IfcWall instance
    for wall in walls:
        direction = util.get_extrusion_direction(wall,ifc_file.schema)
        if direction =="Brep":
            non_vertical_walls.append([util.get_id(wall),wall.Name,"Wall is modelled in place (can be ignored if intentional)"])
            """
            #TODO:check if wall has axis, then ignore, else add to list
            origin,axis,direction,problem = util.get_object_placement_info(ifc_file,wall)
            #print(direction)
            if direction.any():
                direction = util.totuple(direction)
                z = direction[2]-1
                if abs(z) > tolerance:
                    non_vertical_walls.append([util.get_id(wall),wall.Name,"Wall is not vertical"])
                    print(z)
            """
        else:
            continue
    

    return non_vertical_walls


def check_walls(ifc_file):

    walls_major = []
    walls_minor =[]
    walls_ok = []

    all_walls_shorter = True

    units = util.get_project_units(ifc_file)[0]

    # Get all IfcBuildingStorey instances
    storeys = ifc_file.by_type("IfcBuildingStorey")

    # Sort the storeys by elevation
    storeys.sort(key=lambda x: x.Elevation)

    # Query for all instances of IfcWall
    walls = ifc_file.by_type("IfcWall")

    # Get all instances of IfcRelContainedInSpatialStructure
    #rel_contained = ifc_file.by_type("IfcRelContainedInSpatialStructure")

    # Create a dictionary to map elements to their containing structure (storey)
    element_to_storey = util.get_storey_wrt_element(ifc_file)

    # Iterate through each wall
    for wall in walls:
        
        # Get the related storey from the dictionary
        current_storey = element_to_storey.get(wall)

        #print(storey_id)

        wall_height = ifcopenshell.util.element.get_psets(wall).get("Height")

        if wall_height is None:
            # If wall height is not found, use bounding box height
            # wall_height = get_bounding_box_height(wall)
            wall_height = util.get_bounding_box_height(wall,ifc_file.schema)
            if wall_height is None:
                print(f"Warning: Wall {util.get_id(wall)} height not calculatable")
                print(wall.Representation.Representations)
                walls_major.append([util.get_id(wall),wall.Name,"Wall height not calculatable"])
                continue
        
        # Find the corresponding storey
        if current_storey is None :
            #print(f"Warning: Could not find corresponding storey for wall {get_id(wall)}")
            walls_major.append([util.get_id(wall),wall.Name,"Could not find corresponding storey for wall"])
            continue

        current_storey_index = storeys.index(current_storey)
        if current_storey_index == len(storeys) - 1:
            #storey_height = calculate_storey_height(storeys[current_storey_index])
            #print (f"Wall {get_id(wall)} is {wall_height} {units} tall. It is in the highest level")
            walls_ok.append([util.get_id(wall),wall.Name,"OK"])
        else:
            next_storey = storeys[current_storey_index+1]
            storey_height = next_storey.Elevation - current_storey.Elevation 

        if wall_height > storey_height:
            #print(f"Wall {wall.GlobalId} is taller than or equal to the corresponding storey height.")
            #print (f"Wall {get_id(wall)} is {wall_height} {units} tall. The corresponding storey height is {storey_height} {units}")
            walls_minor.append([util.get_id(wall),wall.Name,f"Reduce height by { wall_height - storey_height} {units}"])
            all_walls_shorter = False
        else:
            walls_ok.append([util.get_id(wall),wall.Name,"OK"])
        
    """
    if all_walls_shorter:
        print("All walls are shorter than or equal to the corresponding storey heights.")
        
    else:
        print("Not all walls are shorter than or equal to the corresponding storey heights.")

    print (f"Number of Walls in file = {len(walls)}")
    print (f"Number of Walls with major issues = {len(walls_major)}")
    print (f"Number of Walls with minor issues ={len(walls_minor)}")
    print (f"Number of Walls with no issues ={len(walls_ok)}")
    
    print (".................")
    """

    return walls,walls_major,walls_minor,walls_ok




