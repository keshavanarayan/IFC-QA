import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.shape
import ifcopenshell.util.element
import ifcopenshell.util.constraint
import ifcopenshell.util.unit
import ifcopenshell.entity_instance
import ifcopenshell.util

settings = ifcopenshell.geom.settings()

settings.USE_PYTHON_OPENCASCADE = True

#--------------------------------utils-------------------------------------------

from collections import Counter

def find_mode(arr):
    if not arr:
        return None
    
    counter = Counter(arr)
    max_count = max(counter.values())
    mode = [k for k, v in counter.items() if v == max_count]
    return mode[0]  # If there are multiple modes, return the first one

def find_deviations(arr, deviation_value):
    if not arr:
        return None
    
    mode_value = find_mode(arr)
    deviations = [x for x in arr if abs(x - mode_value) > deviation_value]
    return deviations


def get_elements_wrt_storey(ifc_file,categorystring):

    storey_wrt_element = get_storey_wrt_element(ifc_file)

    element_wrt_storey = {}

    for key,value in storey_wrt_element.items():
        if key.is_a(categorystring):
            #print(key)
            element_wrt_storey.setdefault(value,[]).append(key)
            #print (key,value)

    return element_wrt_storey

# Now slabs_by_storeys dictionary contains slabs sorted by storeys


def get_top_elevation(element):

    """VERSION 2 for IFC 4.0"""
    geom_items = element.Representation.Representations
    #print (geom_items)
    if not geom_items:
        return None  # No geometry found
    
    for geom_item in geom_items:
        
        shape = geom_item.Items[0]
        crv = geom_item.Items[0].SweptArea
        created_shape = ifcopenshell.geom.create_shape(settings,shape)
        return ifcopenshell.util.shape.get_top_elevation(created_shape)


                
"""
def get_profile_area(element):
    if crv.is_a('IfcArbitraryClosedProfileDef'):
        #print(dir(shape.SweptArea))
        if crv.OuterCurve.is_a('IfcPolyline'):
            print("Polyline")
            print (dir(crv.OuterCurve))
            return
        if crv.is_a('IfcCompositeCurve'):
            print("Composite Curve")
            print ((crv.OuterCurve))
            return

    if crv.is_a('IfcRectangleProfileDef'):
        area = crv.XDim * crv.YDim
        return area
    else:
        print("NEW PROBLEM - ",(crv))
"""
            

def get_storey_wrt_element(ifc_file):
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

    prefix = unit_text.Prefix
    suffix = unit_text.Name

    #return dir(unit_scale)
    #return unit_scale.Prefix,unit_scale.Name
    return unit_text.Prefix+unit_text.Name , unit_scale,prefix,suffix
    """
    if unit_scale==0.001:
        return "mm"
    elif unit_scale==1:
        return "m"
    else:
        return "(units)"
    """

def convert_to_m(ifc_file,unit):

    prefix = get_project_units(ifc_file)[2]
    suffix = get_project_units(ifc_file)[3]

    converted_unit = ifcopenshell.util.unit.convert(unit,prefix,suffix,None,"METRE")

    return converted_unit

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