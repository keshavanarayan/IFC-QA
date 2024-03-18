import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.shape
import ifcopenshell.util.element
import ifcopenshell.util.constraint
import ifcopenshell.util.unit
import ifcopenshell.entity_instance
import ifcopenshell.util
settings = ifcopenshell.geom.settings()

#--------------------------------utils-------------------------------------------

settings.USE_PYTHON_OPENCASCADE = True


def element_wrt_storey(ifc_file):
    # Get all instances of IfcRelContainedInSpatialStructure
    rel_contained = ifc_file.by_type("IfcRelContainedInSpatialStructure")

    # Create a dictionary to map elements to their containing structure (storey)
    element_to_storey = {}

    # Iterate through each RelContainedInSpatialStructure relationship
    for rel in rel_contained:
        if rel.RelatedElements:
            for elem in rel.RelatedElements:
                #element_to_storey[elem] = rel.RelatingStructure.Name
                #element_to_storey[elem] = rel.RelatingStructure.GlobalId
                element_to_storey[elem] = rel.RelatingStructure
    
    return element_to_storey

def get_project_units(ifc_file):
    unit_text = ifcopenshell.util.unit.get_project_unit(ifc_file,"LENGTHUNIT")
    unit_scale = ifcopenshell.util.unit.calculate_unit_scale(ifc_file)

    #return dir(unit_scale)
    #return unit_scale.Prefix,unit_scale.Name
    return unit_text.Prefix+unit_text.Name , unit_scale
    """
    if unit_scale==0.001:
        return "mm"
    elif unit_scale==1:
        return "m"
    else:
        return "(units)"
    """


def get_id(element):
    #return element.GlobalId
    return ifcopenshell.entity_instance.id(element)


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
    return max(vertices).Coordinates[2]-min(vertices).Coordinates[2]


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
                    if schema =="IFC2X3":
                        return shape.FirstOperand.Depth
                        print(shape.FirstOperand)
                        continue
                case 'Brep':
                    return get_brep_height(shape)
                case _:
                    #print (f"EXTRA PROBLEM - {shape}")
                    continue

def get_swept_area(element,schema):
    
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
                    return ifcopenshell.util.shape.get_side_area(shape.SweptArea,settings)
                     
                case 'SweptSolid':
                    return ifcopenshell.util.shape.get_side_area(shape.SweptArea,settings)
                case 'Clipping':
                    if schema =="IFC2X3":
                        return shape.FirstOperand.SweptArea
                        #print(shape.FirstOperand)
                        continue
                case 'Brep':
                    return #get_brep_height(shape)
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




def calculate_storey_height(storey):
    elements = ifcopenshell.util.element.get_decomposition(storey)
    bounding_dim = 0
    max_dim = 0
    
    for element in elements:
        if element.is_a("IfcStair"):
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
                    max_dim = max(max_dim, shape.ZDim)
                elif representation_type == 'SweptSolid':
                    max_dim = max(max_dim, shape.Depth)
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
        
            bounding_dim = max(bounding_dim, max_dim)
                
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