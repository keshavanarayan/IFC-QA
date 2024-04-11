import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.shape
import ifcopenshell.util.element
import ifcopenshell.util.constraint
import ifcopenshell.util.unit
import ifcopenshell.entity_instance
import ifcopenshell.util
import numpy as np

settings = ifcopenshell.geom.settings()

settings.USE_PYTHON_OPENCASCADE = True

#--------------------------------utils-------------------------------------------



def get_box3d(origin, x_axis, extrusion_direction, length, width, height):
    """
    Calculate the 3D box vertices based on the given origin, axes, and dimensions.

    Parameters:
    origin (np.array): The origin point of the box.
    x_axis (np.array): The x-axis direction vector.
    extrusion_direction (np.array): The extrusion direction vector.
    length (float): The length of the box.
    width (float): The width of the box.
    height (float): The height of the box.

    Returns:
    np.array: An array containing the vertices of the 3D box.
    """
    # Normalize vectors
    x_axis = x_axis / np.linalg.norm(x_axis)
    #extrusion_direction = extrusion_direction / np.linalg.norm(extrusion_direction)

    # Calculate other axes
    z_axis = extrusion_direction / np.linalg.norm(extrusion_direction)
    y_axis = np.cross(z_axis, x_axis)

    length = abs(length)
    width = abs(width)
    height = abs(height)

    # Calculate vertices
    
    v0 = origin
    v1 = origin + length * x_axis
    v2 = origin + width * y_axis
    v3 = origin + height * extrusion_direction
    v4 = v1 + width * y_axis
    v5 = v1 + height * extrusion_direction
    v6 = v2 + length * x_axis
    v7 = v3 + length * x_axis

    #print(x_axis,y_axis,z_axis)

    # Return vertices
    return np.array([v0, v1, v2, v3, v4, v5, v6, v7])


def boxes_intersect(box1, box2):
  # Check for overlap along each axis
  for i in range(3):  # Check for each dimension (x, y, z)
      self_min = np.min(box1[:, i])
      self_max = np.max(box1[:, i])
      other_min = np.min(box2[:, i])
      other_max = np.max(box2[:, i])

      if self_max < other_min or self_min > other_max:
          return False

  return True

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
        #crv = geom_item.Items[0].SweptArea
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

    storeys = ifc_file.by_type("IfcBuildingStorey")


    # Create a dictionary to map elements to their containing structure (storey)
    element_to_storey = {}

    # Iterate through each RelContainedInSpatialStructure relationship

    for storey in storeys:
        rel_contained = storey.ContainsElements
        for rel in rel_contained:
            if rel.RelatedElements:
                for elem in rel.RelatedElements:
                    element_to_storey[elem] = rel.RelatingStructure
    
    return element_to_storey

def get_storey_of_element(ifc_file,element):
    """
    Get the storey of the given element in the IFC file.

    Args:
        ifc_file: The IFC file containing the element.
        element: The element to get the storey of.

    Returns:
        The storey of the given element.
    """
    storeys = get_storey_wrt_element(ifc_file)

    for each in storeys:
        if get_id(each) == get_id(element):
            return storeys[each]



def get_elements_in_space(ifc_file,spacestring):
    """
	Get all IfcSpace elements in the file and return elements contained in each space.
	
	:param ifc_file: The Ifc file to search for IfcSpace elements
	:param spacestring: The substring to search for in space names
	:return: A dictionary of elements contained in each IfcSpace
	"""

    # Get all IfcSpace elements in the file
    spaces = ifc_file.by_type("IfcSpace")
    
    substring = spacestring

    elements_in_spaces ={}

    # Iterate over the spaces and get all elements contained in each space
    for space in spaces:
        if substring.lower() in str(space.LongName).lower():
            rel_contained = space.ContainsElements
            for rel in rel_contained:
                if rel.RelatedElements:
                    #print (f"-----------{space.LongName}------------")
                    for elem in rel.RelatedElements:
                        elements_in_spaces[elem] = space
                        #print(elem.Name)
    
    return elements_in_spaces
    
from collections import defaultdict

def get_elements_with_same_values(dictionary):
    """
    Generate a dictionary where keys are unique values from the input dictionary and the values are lists of keys from the input dictionary that have the same value.
    
    :param dictionary: A dictionary to process.
    :return: A dictionary with values as keys and lists of keys from the input dictionary as values.
    """
    grouped_elements = defaultdict(list)
    for key, value in dictionary.items():
        grouped_elements[value].append(key)
    return grouped_elements



def get_project_units(ifc_file):
    """
	Get the project units and unit scale from an IFC file.

	:param ifc_file: The path to the IFC file.
	:type ifc_file: str
	:return: A tuple containing the unit and unit scale.
	:rtype: tuple(str, float)
	"""
    unit_text = ifcopenshell.util.unit.get_project_unit(ifc_file,"LENGTHUNIT")
    unit_scale = ifcopenshell.util.unit.calculate_unit_scale(ifc_file)

    if hasattr(unit_text, 'Prefix'):
        prefix = unit_text.Prefix 
    else:
        prefix = ""

    suffix = unit_text.Name

    unit = prefix+suffix


    return unit.lower() , unit_scale

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

def get_brep_vertices(brep):
    """
    Get the vertices of a B-Rep object.

    :param brep: The B-Rep object.
    :type brep: BRep
    :return: The vertices of the B-Rep object.
    :rtype: list
    """
    vertices = []
    for face in brep.Outer.CfsFaces:
        bounds = face.Bounds
        for bound in bounds:
            polygon = bound.Bound.Polygon
            for vertex in polygon:
                #print(vertex.Coordinates)
                vertices.append(vertex)
    return vertices

def get_brep_height(brep):
    """
	Calculate the height of a B-Rep object.

	:param brep: The B-Rep object.
	:type brep: BRep
	:return: The height of the B-Rep object.
	:rtype: float
	"""

    vertices = get_brep_vertices(brep)

    ##print(brep.Outer.CfsFaces[0].Bounds[0].Bound.Polygon[0].Coordinates)
    return max(vertices).Coordinates[2]-min(vertices).Coordinates[2]

def get_overall_bbox_dims(vertices_list):
    vertices = np.concatenate(vertices_list)
    min_coords = np.min(vertices, axis=0)
    max_coords = np.max(vertices, axis=0)

    return max_coords - min_coords

#TODO: find solution if it is a Boolean Clipping result
def get_bounding_box_height(element,schema):

    """
    Get the height of the bounding box of the element based on its geometry representation.
    
    Parameters:
        element (object): The element for which to calculate the bounding box height.
        schema (file.schema): The schema version to consider for certain calculations.
    
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
                case 'Brep':
                    return get_brep_height(shape)
                case 'MappedRepresentation':
                    breps = shape.MappingSource.MappedRepresentation.Items
                    vertices = []
                    for brep in breps:
                        vertices.append(get_brep_vertices(brep))

                    height = get_overall_bbox_dims(vertices)[0][2]
                    #print (height)
                    return height
                case _:
                    #print (f"EXTRA PROBLEM - {shape}")

                    continue

def get_swept_area(element,schema):
    """
    A function to calculate the swept area of a given element based on its geometry representations.
    
    Parameters:
    - element: The element for which the swept area needs to be calculated.
    - schema (file.schema): The schema version being used.
    
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
                    if (schema == "IFC2X3"):
                        return shape.ExtrudedDirection
                    else:
                        shape.ZDim
                        #print (dir(shape))
                case 'SweptSolid':
                    return shape.ExtrudedDirection
                case 'Clipping':
                    if (schema =="IFC2X3"):
                        return shape.FirstOperand.ExtrudedDirection
                    else:
                        return dir(shape.FirstOperand) #shape.FirstOperand.ExtrudedDirection
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


def get_representation(ifc_file,element,contextstring="Body"):
    contexts = ifc_file.by_type("IfcRepresentationContext")

    for each in contexts:
        if each.ContextIdentifier == contextstring:
            context = each


    nested_elements = ifcopenshell.util.representation.get_representation(element,context)

    return nested_elements

def get_object_placement_info(ifc_file,element):
    """
    Get object placement information from the given element.
    
    Parameters:
    - element: The element containing object placement information.
    
    Returns:
    - numpy array: The origin coordinates of the object placement.
    - numpy array: The axis direction ratios of the object placement.
    - numpy array: The direction ratios of the object placement.
    """
    problem = []
    
    if element.ObjectPlacement.RelativePlacement.Axis and element.ObjectPlacement.RelativePlacement.Location and element.ObjectPlacement.RelativePlacement.RefDirection:
        direction = element.ObjectPlacement.RelativePlacement.Axis.DirectionRatios
        #direction = (0,0,1)
        origin = element.ObjectPlacement.RelativePlacement.Location.Coordinates
        axis = element.ObjectPlacement.RelativePlacement.RefDirection.DirectionRatios
        #print(direction,origin,axis)
    else:
        problem = element
        direction = None
        origin = None
        axis = None
        #print (ifcopenshell.entity_instance.get_info(element.Representation.Representations[0].Items[0].MappingTarget))
        #print (element.Name,get_id(element),get_storey_of_element(ifc_file,element).Name)
    
    

    return np.array(origin),np.array(axis),np.array(direction),problem

def totuple(np_array):
    """
    Recursively converts the np.array into a tuple.

    Parameters:
        a (np.array): The input to be converted into a tuple.

    Returns:
        tuple: The converted tuple.

    Raises:
        TypeError: If the input `a` cannot be converted into a tuple.
    """
    try:
        return tuple(totuple(i) for i in np_array)
    except TypeError:
        return np_array


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