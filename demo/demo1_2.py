import ifcopenshell

def get_storey_height(ifc_file, storey_number):
    # Open the IFC file
    ifc = ifcopenshell.open(ifc_file)
    
    # Get the storey based on storey number
    storey = get_storey_by_number(ifc, storey_number)
    if storey is None:
        return None
    
    # Get all elements contained in the storey
    elements = get_elements_on_storey(ifc, storey)
    if not elements:
        return None
    
    # Initialize min and max Z coordinates
    min_z = float('inf')
    max_z = float('-inf')
    
    # Iterate through elements to find min and max Z coordinates
    for element in elements:
        bbox = element.BoundingBox
        if bbox:
            min_z = min(min_z, bbox[0][2])
            max_z = max(max_z, bbox[1][2])
    
    # Calculate storey height
    storey_height = max_z - min_z
    return storey_height
def sort_storeys_by_elevation(ifc):
    storeys = []
    

    
    # Get all IfcBuildingStorey entities
    ifc_storeys = ifc.by_type("IfcBuildingStorey")
    
    # Extract relevant information from each storey
    for storey in ifc_storeys:
        storeys.append({"name": storey.Name, "elevation": storey.Elevation})
    
    # Sort storeys by elevation
    sorted_storeys = sorted(storeys, key=lambda x: x["elevation"])
    
    return sorted_storeys

def get_storey_by_number(ifc_file, storey_number):
    storeys = sort_storeys_by_elevation(ifc_file)
    
    # Retrieve storey information based on the given storey number
    if storey_number <= len(storeys):
        return storeys[storey_number - 1]
    else:
        return None

def get_elements_on_storey(ifc, storey):
    elements = []
    
    # Get all elements contained in the storey
    for rel in storey.ContainsElements:
        for element in rel.RelatedElements:
            elements.append(element)
    
    return elements

# Example usage
ifc_file_path = "ifc\AC2Ø-Institute-Var-2.ifc"
storey_number = 0  # Provide the storey number here as a string

storey_height = get_storey_height(ifc_file_path, storey_number)

if storey_height is not None:
    print(f"The height of storey {storey_number} is {storey_height} units.")
else:
    print(f"Storey {storey_number} not found or does not contain any elements.")
