import ifcopenshell

def sort_storeys_by_elevation(ifc_file):
    storeys = []
    
    # Open the IFC file
    ifc = ifcopenshell.open(ifc_file)
    
    # Get all IfcBuildingStorey entities
    ifc_storeys = ifc.by_type("IfcBuildingStorey")
    
    # Extract relevant information from each storey
    for storey in ifc_storeys:
        storeys.append({"name": storey.Name, "elevation": storey.Elevation})
    
    # Sort storeys by elevation
    sorted_storeys = sorted(storeys, key=lambda x: x["elevation"])
    
    return sorted_storeys

def get_storey_number_by_elevation(ifc_file, storey_number):
    storeys = sort_storeys_by_elevation(ifc_file)
    
    # Retrieve storey information based on the given storey number
    if storey_number <= len(storeys):
        return storeys[storey_number - 1]
    else:
        return None

# Example usage
ifc_file_path = "ifc\AC2Ø-Institute-Var-2.ifc"
storey_number = 0

storey_info = get_storey_number_by_elevation(ifc_file_path, storey_number)

if storey_info:
    print(f"Storey {storey_number}: {storey_info['name']}, Elevation: {storey_info['elevation']}")
else:
    print(f"Storey {storey_number} not found.")
