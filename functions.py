import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.shape
import math
import numpy as np
import ifcopenshell.util.element

settings = ifcopenshell.geom.settings()

def extract_storey_info(ifc_file):
    # Open the IFC file
    ifc_file = ifcopenshell.open(ifc_file)

    # Get all IfcBuildingStorey instances
    storeys = ifc_file.by_type("IfcBuildingStorey")

    # Sort the storeys by elevation
    storeys.sort(key=lambda x: x.Elevation)

    storey_heights = []

    # Iterate over each storey and extract information
    for i in range(len(storeys)-1):
        current_storey = storeys[i]
        next_storey = storeys[i+1]

        storey_name = current_storey.Name if hasattr(current_storey, "Name") else "N/A"
        storey_height = next_storey.Elevation - current_storey.Elevation

        print(f"Storey Name: {storey_name}, Storey Height: {storey_height}")
        storey_heights.append(storey_height)
    
    return storey_heights


def get_storey_name(storey):
    # Retrieve the name of the storey
    if hasattr(storey, 'Name'):
        return storey.Name
    else:
        return "Unnamed"


def calculate_bounding_box_height(wall):

    geom = wall.Representation.Representations[0].Items[0]
    #return ifcopenshell.util.shape.get_z(geom)
    

    if geom.is_a("IfcExtrudedAreaSolid"):
        #print (geom.Depth)
        return (geom.Depth)

    #TODO: find solution if it is a Boolean Clipping result





def check_wall_heights(ifc_file):
    # Open the IFC file
    ifc_file = ifcopenshell.open(ifc_file)

    walls_with_major_issues = 0
    walls_with_minor_issues = 0

    # Get all IfcWall instances
    walls = ifc_file.by_type("IfcWall")

    # Get all IfcBuildingStorey instances
    storeys = ifc_file.by_type("IfcBuildingStorey")

    # Sort the storeys by elevation
    storeys.sort(key=lambda x: x.ObjectPlacement.RelativePlacement.Location.Coordinates[2])

    # Initialize a flag to track if all walls are shorter than corresponding storey heights
    all_walls_shorter = True

    # Iterate over each wall and compare its height with the corresponding storey height
    for wall in walls:
        wall_height = ifcopenshell.util.element.get_psets(wall).get("Height")
        if wall_height is None:
            # If wall height is not found, use bounding box height
            # wall_height = get_bounding_box_height(wall)
            wall_height = calculate_bounding_box_height(wall)
            if wall_height is None:
                print(f"Warning: Wall {wall.GlobalId} height not found.")
                walls_with_major_issues += 1
                continue

        # Find the corresponding storey
        storey = None
        for current_storey, next_storey in zip(storeys, storeys[1:]):
            if current_storey.ObjectPlacement.RelativePlacement.Location.Coordinates[2] <= wall.ObjectPlacement.RelativePlacement.Location.Coordinates[2] < next_storey.ObjectPlacement.RelativePlacement.Location.Coordinates[2]:
                storey = current_storey
                break

        if storey is None:
            print(f"Warning: Could not find corresponding storey for wall {wall}")
            walls_with_major_issues += 1
            continue

        storey_height = next_storey.ObjectPlacement.RelativePlacement.Location.Coordinates[2] - current_storey.ObjectPlacement.RelativePlacement.Location.Coordinates[2]

        if wall_height > storey_height:
            #print(f"Wall {wall.GlobalId} is taller than or equal to the corresponding storey height.")
            print (f"Wall {wall.GlobalId} is {wall_height} meters tall")
            all_walls_shorter = False
            walls_with_minor_issues +=1

    if all_walls_shorter:
        print("All walls are shorter than or equal to the corresponding storey heights.")
    else:
        print("Not all walls are shorter than or equal to the corresponding storey heights.")

    print (f"Number of Walls in file = {len(walls)}")
    print (f"Number of Walls with major issues = {walls_with_major_issues}")
    print (f"Number of Walls with minor issues ={walls_with_minor_issues}")


# You would need to implement the calculate_bounding_box_height function
# according to your specific requirements.
# def calculate_bounding_box_height(wall):
#     pass








def are_walls_vertical(ifc_file_path, tolerance=1e-5):
    # Open the IFC file
    ifc_file = ifcopenshell.open(ifc_file_path)

    # Get all IfcWall instances from the IFC file
    walls = ifc_file.by_type('IfcWall')
    
    non_vertical_walls = []

    # Iterate over each IfcWall instance
    for wall in walls:
        # Retrieve the orientation of the wall
        if hasattr(wall, 'Axis'):
            axis = wall.Axis

            # Check if the wall is vertical (axis direction is close to vertical)
            if not math.isclose(axis[0], 0.0, abs_tol=tolerance) or not math.isclose(axis[1], 0.0, abs_tol=tolerance):
                non_vertical_walls.append(wall.GlobalId)

    return non_vertical_walls