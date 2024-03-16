import ifcopenshell

# Open the IFC file
file = ifcopenshell.open("ifc/rac_advanced_sample_project.ifc")

# Get all walls in the file
walls = file.by_type("IfcWall")[0]

#print (ifcopenshell.entity_instance.id(walls[0]))

print(dir(walls))

