import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.shape
import math
import numpy as np
import ifcopenshell.util.element
import ifcopenshell.util.constraint
import ifcopenshell.util.unit
import ifcopenshell.entity_instance

settings = ifcopenshell.geom.settings()


def extract_storey_heights(ifc_file):

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



def get_project_units(ifc_file):
    unit_scale = ifcopenshell.util.unit.calculate_unit_scale(ifc_file)
    if unit_scale==0.001:
        return "mm"
    elif unit_scale==1:
        return "m"
    else:
        return "(units)"





def are_walls_vertical(ifc_file, tolerance=1e-5):

    # Get all IfcWall instances from the IFC file
    walls = ifc_file.by_type('IfcWall')
    
    non_vertical_walls = []

    # Iterate over each IfcWall instance
    for wall in walls:
        #print (wall)
        #print(wall.Representation.Representations)
        #print(wall.Representation.Representations[2].Items[0])
        # Retrieve the orientation of the wall
        """if hasattr(wall, 'Axis'):
            axis = wall.Axis

            # Check if the wall is vertical (axis direction is close to vertical)
            if not math.isclose(axis[0], 0.0, abs_tol=tolerance) or not math.isclose(axis[1], 0.0, abs_tol=tolerance):
                non_vertical_walls.append(wall.GlobalId)"""

    return non_vertical_walls


def calculate_bounding_box_height(wall):

    """VERSION 2 for IFC 4.0"""
    geom_items = wall.Representation.Representations
    #print (geom_items)
    if not geom_items:
        return None  # No geometry found
    
    for geom_item in geom_items:
        shape = geom_item.Items[0]
        if geom_item.is_a('IfcShapeRepresentation') and shape:
            representation_type = geom_item.RepresentationType
            #print (representation_type)
            if representation_type == 'BoundingBox':
                return shape.ZDim
            elif representation_type == 'SweptSolid':
                return shape.Depth
            elif representation_type == 'Clipping':
                #return geom_item.Items[0].Depth
                #print(shape.FirstOperand)
                #print (f"FOUND DEPTH    {shape.FirstOperand.Depth}")
                return shape.FirstOperand.Depth

            elif representation_type == 'Curve2D':
                #return geom_item.Items[0].Depth
                continue
            elif representation_type == 'Brep':
                #return geom_item.Items[0].Depth
                continue

            else:
                print (f"EXTRA PROBLEM - {geom_item.Items[0]}")

    
    """
    VERSION1 for IFC 4.0
    geom = wall.Representation.Representations[0].Items[0]
    print (geom)
    
    if geom.is_a("IfcExtrudedAreaSolid"):
        #print (geom.Depth)
        return (geom.Depth)
    else:
        #print(geom)
        geom = wall.Representation.Representations[1].Items[0]
        #print (geom.ZDim)
        return geom.ZDim
        #print(geom)
        
    """

    #TODO: find solution if it is a Boolean Clipping result


"""VERSION 1.0 """

def check_wall_heights(ifc_file):

    walls_with_major_issues = 0
    walls_with_minor_issues = 0
    walls_with_no_issues = 0
    ids = []

    units = get_project_units(ifc_file)

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
                ids.append(wall.GlobalId)
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
            print (f"Wall {wall.GlobalId} is {wall_height} {units} tall. The corresponding storey height is {storey_height} {units}")
            all_walls_shorter = False
            walls_with_minor_issues +=1
        else:
            walls_with_no_issues += 1

    if all_walls_shorter:
        print("All walls are shorter than or equal to the corresponding storey heights.")
    else:
        print("Not all walls are shorter than or equal to the corresponding storey heights.")

    print (f"Number of Walls in file = {len(walls)}")
    print (f"Number of Walls with major issues = {walls_with_major_issues}")
    print (f"Number of Walls with minor issues ={walls_with_minor_issues}")
    print (f"Number of Walls with no issues ={walls_with_no_issues}")
    print (f"IDs of walls with major issues = {ids}")



"""VERSION 2.0
def check_wall_heights(ifc_file):

    walls_with_major_issues = 0
    walls_with_minor_issues = 0
    walls_with_no_issues = 0
    ids = []

    units = get_project_units(ifc_file)

    # Get all IfcWall instances
    walls = ifc_file.by_type("IfcWall")

    # Get all IfcBuildingStorey instances
    storeys = ifc_file.by_type("IfcBuildingStorey")

    # Sort the storeys by elevation
    storeys.sort(key=lambda x: x.ObjectPlacement.RelativePlacement.Location.Coordinates[2])

    # Initialize a flag to track if all walls are shorter than corresponding storey heights
    all_walls_shorter = True

    sorted_walls = walls_by_stories(ifc_file)


    print (f"Number of Walls in file = {len(walls)}")
    print (f"Number of Walls with major issues = {walls_with_major_issues}")
    print (f"Number of Walls with minor issues ={walls_with_minor_issues}")
    print (f"Number of Walls with no issues ={walls_with_no_issues}")
    print (f"IDs of walls with major issues = {ids}")
"""

def walls_by_stories(ifc_file):
        # Query for all instances of IfcWall
    walls = ifc_file.by_type("IfcWall")

    # Get all instances of IfcRelContainedInSpatialStructure
    rel_contained = ifc_file.by_type("IfcRelContainedInSpatialStructure")

    # Create a list to store wall ID and storey pairs
    wall_storey_pairs = []

    # Create a dictionary to map elements to their containing structure (storey)
    element_to_storey = {}

    # Iterate through each RelContainedInSpatialStructure relationship
    for rel in rel_contained:
        if rel.RelatedElements:
            for elem in rel.RelatedElements:
                #element_to_storey[elem] = rel.RelatingStructure.Name
                element_to_storey[elem] = rel.RelatingStructure.GlobalId

    # Iterate through each wall
    for wall in walls:
        wall_id = wall.GlobalId
        wall_name = wall.Name if hasattr(wall, "Name") else "Unnamed"
        
        # Get the related storey from the dictionary
        storey_name = element_to_storey.get(wall, "Not found")
        
        # Append the wall ID and storey as a list to wall_storey_pairs
        wall_storey_pairs.append([wall_id, storey_name])
    
    return wall_storey_pairs


def wallht_storeyht(wall_id,storey_id,ifc_file):
    wall = ifc_file.by_guid(wall_id)
    storey = ifc_file.by_guid(storey_id)

    print (wall,storey)

   