import ifcopenshell
import ifcopenshell.util.representation

# Open the IFC file
file = ifcopenshell.open("ifc/rac_advanced_sample_project.ifc")

# Get the door element
door = file.by_type("IfcDoor")[0]

contexts = file.by_type("IfcRepresentationContext")

for each in contexts:
    if each.ContextIdentifier == "Body":
        context = each


nested_elements = ifcopenshell.util.representation.get_representation(door,context)


for element in nested_elements:
    #print(element)
    if type(element) == ifcopenshell.entity_instance:
        #print(element.is_a())
        print(element.RepresentationsInContext[0].Items[0].FbsmFaces[0].CfsFaces[0].Bounds[0].Bound.Polygon)
        print (".........................")
        continue
    else:
        #print(dir(element))
        print (".........................")
        print (".........................")
        continue




