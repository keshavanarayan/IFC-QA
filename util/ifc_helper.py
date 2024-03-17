import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.shape
import math
import ifcopenshell.util.element
import ifcopenshell.util.constraint
import ifcopenshell.util.unit
import ifcopenshell.entity_instance
import ifcopenshell.util

settings = ifcopenshell.geom.settings()

#TODO:use dir(element) to find attributes of elements

def get_id(element):
    return ifcopenshell.entity_instance.id(element)

def get_storey_heights(ifc_file):

    # Get all IfcBuildingStorey instances
    # Get all IfcBuildingStorey instances
    storeys = ifc_file.by_type("IfcBuildingStorey")

    # Sort the storeys by elevation
    storeys.sort(key=lambda x: x.Elevation)

    storeys = []

    # Iterate over each storey and extract information
    for i in range(len(storeys)-1):
        current_storey = storeys[i]
        next_storey = storeys[i+1]

        storey_name = current_storey.Name if hasattr(current_storey, "Name") else "N/A"
        storey_height = next_storey.Elevation - current_storey.Elevation

        print(f"Storey Name: {storey_name}, Storey Height: {storey_height}")
        storeys.append([storey_name,storey_height])
    
    #print (f"Storey Name: {storeys[len(storeys)-1].Name}, Storey Height: Top Most Level")
    #storeys.append([storeys[len(storeys)-1].Name,None])
    
    return storeys

def get_brep_height(brep):

    vertices = []
    for face in brep.Outer.CfsFaces:
        bounds = face.Bounds
        for bound in bounds:
            polygon = bound.Bound.Polygon
            for vertex in polygon:
                #print(vertex.Coordinates)
                vertices.append(vertex)

    ##print(brep.Outer.CfsFaces[0].Bounds[0].Bound.Polygon[0].Coordinates)
    return (max(vertices).Coordinates[2]-min(vertices).Coordinates[2])






def get_project_units(ifc_file):
    unit_scale = ifcopenshell.util.unit.calculate_unit_scale(ifc_file)
    if unit_scale==0.001:
        return "mm"
    elif unit_scale==1:
        return "m"
    else:
        return "(units)"





#TODO: find solution if it is a Boolean Clipping result
def get_bounding_box_height(element,schema):

    """VERSION 2 for IFC 4.0"""
    geom_items = element.Representation.Representations
    #print (geom_items)
    if not geom_items:
        return None  # No geometry found
    
    for geom_item in geom_items:
        shape = geom_item.Items[0]
        if geom_item.is_a('IfcShapeRepresentation') and shape:
            representation_type = geom_item.RepresentationType
            #print (representation_type)
            match representation_type:
                case 'BoundingBox':
                    return shape.ZDim
                case 'SweptSolid':
                    return shape.Depth
                case 'Clipping':
                    if (schema =="IFC2X3"):
                        return shape.FirstOperand.Depth
                    else:
                        print(shape.FirstOperand)
                        continue
                case 'Brep':
                    return get_brep_height(shape)
                case _:
                    #print (f"EXTRA PROBLEM - {shape}")
                    continue
            

def get_extrusion_direction(element,schema):
    """VERSION 2 for IFC 4.0"""
    geom_items = element.Representation.Representations
    #print (geom_items)
    if not geom_items:
        return None  # No geometry found
    
    for geom_item in geom_items:
        shape = geom_item.Items[0]
        if geom_item.is_a('IfcShapeRepresentation') and shape:
            representation_type = geom_item.RepresentationType
            #print (representation_type)
            match representation_type:
                case 'BoundingBox':
                    return shape.ExtrudedDirection
                case 'SweptSolid':
                    return shape.ExtrudedDirection
                case 'Clipping':
                    if (schema =="IFC2X3"):
                        return shape.FirstOperand.ExtrudedDirection
                    else:
                        print(shape.FirstOperand)
                        continue
                case 'Brep':
                    #print(dir(shape.Outer))
                    return "Brep"
                    #print (f"EXTRA PROBLEM - {shape}")
                    continue
                case _:
                    #print (f"EXTRA PROBLEM - {shape}")
                    continue
    



def are_walls_vertical(ifc_file, tolerance=1e-5):

    # Get all IfcWall instances from the IFC file
    walls = ifc_file.by_type('IfcWall')
    
    non_vertical_walls = []


    # Iterate over each IfcWall instance
    for wall in walls:
        direction = get_extrusion_direction(wall,ifc_file.schema)
        if direction =="Brep":
            non_vertical_walls.append([get_id(wall),wall.Name,"Wall is modelled in place (can be ignored if intentional)"])
        else:
            direction = direction.DirectionRatios
            z = direction[2]-1
            if abs(z) > tolerance:
                non_vertical_walls.append([get_id(wall),wall.Name,"Wall is not vertical"])
                print(z)

    return non_vertical_walls


def check_wall_heights(ifc_file):

    #ALTERNATE:wall.GlobalId
    walls_major = []
    walls_minor =[]
    walls_ok = []

    all_walls_shorter = True

    units = get_project_units(ifc_file)

    # Get all IfcBuildingStorey instances
    storeys = ifc_file.by_type("IfcBuildingStorey")

    # Sort the storeys by elevation
    storeys.sort(key=lambda x: x.Elevation)

    #print (storeys)

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
                #element_to_storey[elem] = rel.RelatingStructure.GlobalId
                element_to_storey[elem] = rel.RelatingStructure

    # Iterate through each wall
    for wall in walls:
        wall_name = wall.Name if hasattr(wall, "Name") else "Unnamed"
        
        # Get the related storey from the dictionary
        current_storey = element_to_storey.get(wall)

        #print(storey_id)

        wall_height = ifcopenshell.util.element.get_psets(wall).get("Height")

        if wall_height is None:
            # If wall height is not found, use bounding box height
            # wall_height = get_bounding_box_height(wall)
            wall_height = get_bounding_box_height(wall,ifc_file.schema)
            if wall_height is None:
                print(f"Warning: Wall {get_id(wall)} height not calculatable")
                print(wall.Representation.Representations)
                walls_major.append([get_id(wall),wall.Name,"Wall height not calculatable"])
                continue
        
        # Find the corresponding storey
        if current_storey is None :
            #print(f"Warning: Could not find corresponding storey for wall {get_id(wall)}")
            walls_major.append[[get_id(wall),wall.Name,"Could not find corresponding storey for wall"]]
            continue

        current_storey_index = storeys.index(current_storey)
        if current_storey_index == len(storeys) - 1:
            #storey_height = calculate_storey_height(storeys[current_storey_index])
            #print (f"Wall {get_id(wall)} is {wall_height} {units} tall. It is in the highest level")
            walls_ok.append([get_id(wall),wall.Name,"OK"])
        else:
            next_storey = storeys[current_storey_index+1]
            storey_height = next_storey.Elevation - current_storey.Elevation 

        if wall_height > storey_height:
            #print(f"Wall {wall.GlobalId} is taller than or equal to the corresponding storey height.")
            #print (f"Wall {get_id(wall)} is {wall_height} {units} tall. The corresponding storey height is {storey_height} {units}")
            walls_minor.append([get_id(wall),wall.Name,f"Reduce height by { wall_height - storey_height} {units}"])
            all_walls_shorter = False
        else:
            walls_ok.append([get_id(wall),wall.Name,"OK"])
        
    """
    if all_walls_shorter:
        print("All walls are shorter than or equal to the corresponding storey heights.")
        
    else:
        print("Not all walls are shorter than or equal to the corresponding storey heights.")

    print (f"Number of Walls in file = {len(walls)}")
    print (f"Number of Walls with major issues = {len(walls_major)}")
    print (f"Number of Walls with minor issues ={len(walls_minor)}")
    print (f"Number of Walls with no issues ={len(walls_ok)}")
    """
    print (".................")

    return walls,walls_major,walls_minor,walls_ok


def check_doors():
    #TODO: finish door accessibility
    

    pass



def calculate_storey_height(storey):
    elements = ifcopenshell.util.element.get_decomposition(storey)
    bounding_dim = 0
    max_dim = 0
    
    for element in elements:
        if (element.is_a("IfcStair")):
            continue
        geom_items = element.Representation.Representations
        #print(element.Representation.Representations)
        #print (geom_items)
        
        if not geom_items:
            continue  # No geometry found

        for geom_item in geom_items:
            shape = geom_item.Items[0]
            
            if geom_item.is_a('IfcShapeRepresentation') and shape:
                representation_type = geom_item.RepresentationType
                #print (representation_type)
                if representation_type == 'BoundingBox':
                    if shape.ZDim > max_dim:
                        max_dim = shape.ZDim
                elif representation_type == 'SweptSolid':
                    if shape.Depth >max_dim:
                        max_dim = shape.Depth
                elif representation_type == 'Clipping':
                    continue
                elif representation_type == 'Curve2D':
                    #return geom_item.Items[0].Depth
                    #print(shape)
                    continue
                elif representation_type == 'Brep':
                    #return geom_item.Items[0].Depth
                    #print(shape)
                    continue

                else:
                    continue
                    #print (f"EXTRA PROBLEM - {geom_item.Items[0]}")
        
            if max_dim>bounding_dim:
                bounding_dim = max_dim
                
    return bounding_dim


def has_repeating_elements(list_of_lists):
    flattened_list = [item for sublist in list_of_lists for item in sublist]
    unique_items = set()
    conflicting_items = []

    for item in flattened_list:
        if item in unique_items:
            conflicting_items.append(item)
        else:
            unique_items.add(item)

    return conflicting_items