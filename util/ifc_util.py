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
    """
    Find the mode(s) in a given list 'arr' and return the mode with the highest frequency.
    
    Parameters:
    arr (list): A list of elements to find the mode(s) from.
    
    Returns:
    int or float: The mode with the highest frequency in the input list.
    """
    if not arr:
        return None
    
    counter = Counter(arr)
    max_count = max(counter.values())
    mode = [k for k, v in counter.items() if v == max_count]
    return mode[0]  # If there are multiple modes, return the first one

def find_deviations(arr, deviation_value):
    """
    Find deviations in the input array based on the given deviation value.

    :param arr: The input array to find deviations in.
    :param deviation_value: The threshold for deviations.
    :return: A list of values in the input array that deviate from the mode by more than the specified deviation value.
    """
    if not arr:
        return None
    
    mode_value = find_mode(arr)
    deviations = [x for x in arr if abs(x - mode_value) > deviation_value]
    return deviations


def get_elements_wrt_storey(ifc_file,categorystring):
    """
	Get elements with respect to a specific storey based on the category provided.

	Parameters:
	- ifc_file: the IFC file containing the elements
	- categorystring: the category of elements to filter by

	Returns:
	- A dictionary where the keys are storeys and the values are lists of elements belonging to that storey
	"""

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
    """
    Get the top elevation of the given element.

    Parameters:
    - element: The element for which to retrieve the top elevation.

    Returns:
    - The top elevation of the element, or None if no geometry is found.
    """

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
    """
    Retrieve the storey (containing structure) for each element in the given IFC file.

    Parameters:
    - ifc_file: The IFC file to extract storey information from.

    Returns:
    - element_to_storey: A dictionary mapping each element to its containing structure (storey).
    """
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
    """
    A function that retrieves the project units from the provided ifc_file.
    It obtains the unit text and scale, extracts the prefix and suffix from the unit text,
    and returns a tuple containing the concatenated prefix and suffix, unit scale, prefix, and suffix.
    """
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

#TODO:complete unit conversion to metres

def convert_to_m(ifc_file,unit):
    """
	Converts a given unit to METRE using project units from the provided ifc_file.
	
	:param ifc_file: The ifc file containing project units information.
	:param unit: The unit to be converted.
	:return: The unit converted to METRE.
	"""

    prefix = get_project_units(ifc_file)[2]
    suffix = get_project_units(ifc_file)[3]

    converted_unit = ifcopenshell.util.unit.convert(unit,prefix,suffix,None,"METRE")

    return converted_unit

def get_id(element):
    """
    Get the ID of the element.

    Args:
        element: The element to retrieve the ID from.

    Returns:
        The ID of the element.
    """
    #return element.GlobalId
    return ifcopenshell.entity_instance.id(element)


def get_brep_height(brep):
    """
	Calculate the height of a B-Rep object.

	:param brep: The B-Rep object.
	:type brep: BRep
	:return: The height of the B-Rep object.
	:rtype: float
	"""

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

    """
    Get the height of the bounding box of the element based on its geometry representation.
    
    Parameters:
        element (object): The element for which to calculate the bounding box height.
        schema (str): The schema version to consider for certain calculations.
    
    Returns:
        float or None: The height of the bounding box if found, None if no geometry is found or if the representation type is not recognized.
    """

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
    """
    A function to calculate the swept area of a given element based on its geometry representations.
    
    Parameters:
    - element: The element for which the swept area needs to be calculated.
    - schema: The schema version being used.
    
    Returns:
    - The swept area of the element if found, otherwise returns None.
    """

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
    """
	A function to get the extrusion direction based on the shape representation type.
	
	Parameters:
	    element: The element for which the extrusion direction is needed.
	    schema: The schema version for which the extrusion direction is being calculated.
	
	Returns:
	    The extrusion direction based on the shape representation type, or None if no geometry is found.
	"""

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
    """
    Calculate the height of a storey based on its elements' geometry representations.
    
    Parameters:
    - storey: an IfcStorey object
    
    Returns:
    - The maximum bounding dimension of the storey

    """

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
    """
    Given a list of lists, this function checks if any element in the flattened list appears more than once.
    It returns a list of all the repeating elements.

    Parameters:
    - list_of_lists (list): A list of lists, where each sublist contains elements that may be repeated.

    Returns:
    - conflicting_items (list): A list of all the repeating elements in the flattened list.

    Example:
    has_repeating_elements([[1, 2, 3], [4, 5, 6], [2, 7, 8]]) -> [2]
    
    """
    flattened_list = [item for sublist in list_of_lists for item in sublist]
    unique_items = set()
    conflicting_items = []

    for item in flattened_list:
        if item in unique_items:
            conflicting_items.append(item)
        else:
            unique_items.add(item)

    return conflicting_items