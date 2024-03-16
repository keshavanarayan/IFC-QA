import ifcopenshell

def get_elements_on_storey(ifc_file, storey_name):
    elements = []
    
    # Open the IFC file
    ifc = ifcopenshell.open(ifc_file)
    
    # Get all IfcBuildingStorey entities
    storeys = ifc.by_type("IfcBuildingStorey")
    
    # Find the specified storey
    target_storey = None
    for storey in storeys:
        if storey.Name == storey_name:
            target_storey = storey
            break
    
    if target_storey is None:
        print(f"Storey '{storey_name}' not found.")
        return elements
    
    # Get all elements contained in the specified storey
    for rel in target_storey.ContainsElements:
        for element in rel.RelatedElements:
            elements.append(element)
    
    return elements

# Example usage
ifc_file_path = "ifc\AC2Ø-Institute-Var-2.ifc"
storey_name = "Keller"

elements_on_storey = get_elements_on_storey(ifc_file_path, storey_name)

# Print the IDs of elements on the specified storey
for element in elements_on_storey:
    print("Element ID:", element.id())
