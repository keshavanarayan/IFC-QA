import ifcopenshell
import math

def get_storey_heights(ifc_file_path):
    # Open the IFC file
    ifc_file = ifcopenshell.open(ifc_file_path)

    # Get all IfcBuildingStorey instances from the IFC file
    storeys = ifc_file.by_type('IfcBuildingStorey')

    storey_heights = {}

    # Iterate over each IfcBuildingStorey instance
    for storey in storeys:
        # Retrieve the storey height
        if hasattr(storey, 'Elevation'):
            elevation = storey.Elevation
            storey_heights[storey] = elevation

    return storey_heights

def get_storey_name(storey):
    # Retrieve the name of the storey
    if hasattr(storey, 'Name'):
        return storey.Name
    else:
        return "Unnamed"

def check_walls_in_storeys(ifc_file_path):
    # Open the IFC file
    ifc_file = ifcopenshell.open(ifc_file_path)

    # Get all IfcBuildingStorey instances from the IFC file
    storeys = ifc_file.by_type('IfcBuildingStorey')

    # Initialize a dictionary to store walls in each storey
    walls_in_storeys = {storey: [] for storey in storeys}

    # Get all IfcWall instances from the IFC file
    walls = ifc_file.by_type('IfcWall')

    # Iterate over each IfcWall instance
    for wall in walls:
        # Find the storey associated with the wall
        storey = None
        if hasattr(wall, 'ContainedInStructure'):
            for rel in wall.ContainedInStructure:
                if hasattr(rel, 'RelatingStructure') and isinstance(rel.RelatingStructure, ifcopenshell.entity_instance('IfcBuildingStorey')):
                    storey = rel.RelatingStructure
                    break

        if storey:
            # Add the wall to the appropriate storey
            walls_in_storeys[storey].append(wall)

    # Check if walls in each storey exceed the storey height
    for storey, walls in walls_in_storeys.items():
        storey_name = get_storey_name(storey)
        if storey in storey_heights:
            storey_height = storey_heights[storey]
            for wall in walls:
                if hasattr(wall, 'OverallHeight') and wall.OverallHeight > storey_height:
                    print(f"Wall ID {wall.GlobalId} in storey '{storey_name}' exceeds storey height")


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