import ifcopenshell
import ifcopenshell.util.element
import ifcopenshell.util.representation
import ifcopenshell.api
import ifcopenshell.api.context.add_context
import ifcopenshell.entity_instance

# Open the IFC file
file = ifcopenshell.open("ifc/rac_advanced_sample_project.ifc")

# Get the door element
door = file.by_type("IfcDoor")[0]

contexts = file.by_type("IfcRepresentationContext")

context = contexts[0]

for each in contexts:
    if each.ContextIdentifier == "Body":
        context = each

#print(context)


nested_elements = ifcopenshell.util.representation.get_representation(door,context)
#print (nested_elements)

# Print the names of the nested elements
for element in nested_elements:
    #print(element)
    print(ifcopenshell.entity_instance.is_a(element))
    """
    if element.is_a("IfcShapeRepresentation"):
        print(element.RepresentationType)
        #print(element.Name)
"""



