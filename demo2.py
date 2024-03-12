import ifcopenshell

#ifc_file_path = 'models/rac_advanced_sample_project.ifc'
#ifc_file_path = 'models\AC2Ø-Institute-Var-2.ifc'
#ifc_file_path = 'models\House.ifc'
ifc_file_path = 'models\example project location.ifc'
ifc_file = ifcopenshell.open(ifc_file_path)

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
            element_to_storey[elem] = rel.RelatingStructure.GlobalId

# Iterate through each wall
for wall in walls:
    wall_id = wall.GlobalId
    wall_name = wall.Name if hasattr(wall, "Name") else "Unnamed"
    
    # Get the related storey from the dictionary
    storey_name = element_to_storey.get(wall, "Not found")
    
    # Append the wall ID and storey as a list to wall_storey_pairs
    wall_storey_pairs.append([wall_id, storey_name])

# Print the list of wall ID and storey pairs
print(wall_storey_pairs)
