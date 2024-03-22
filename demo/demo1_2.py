import ifcopenshell

# Load the IFC file
ifc_file = ifcopenshell.open("ifc/rac_advanced_sample_project.ifc")

# Query for all IfcElement entities
elements = ifc_file.by_type("IfcElement")

# Iterate through each IfcElement
for element in elements:
    # Check if the element has a 'ContainedInStructure' attribute
    if hasattr(element, "ContainedInStructure"):
        # Get the first item in the list of relationships (assuming there's only one)
        relation = element.ContainedInStructure[0]
        
        # Check if the relation is an 'IfcRelContainedInSpatialStructure'
        if relation.is_a("IfcRelContainedInSpatialStructure"):
            # Get the related building storey
            building_storey = relation.RelatingStructure

            # Check if the related structure is an IfcBuildingStorey
            if building_storey.is_a("IfcBuildingStorey"):
                # Print the storey information
                print(f"Element {element.Name} is in Building Storey {building_storey.Name}")
