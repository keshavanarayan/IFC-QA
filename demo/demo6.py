import ifcopenshell
import ifcopenshell.util.element
import ifcopenshell.util.representation

# Open the IFC file
file = ifcopenshell.open("ifc/rac_advanced_sample_project.ifc")

# Get the door element
door = file.by_type("IfcDoor")[0]

print(door)

# Get all elements nested within the door
#nested_elements = ifcopenshell.util.element.get_decomposition(door)

nested_elements = ifcopenshell.util.representation.get_representation(door)


print (nested_elements)

# Print the names of the nested elements
for element in nested_elements:
    print(element.Name)