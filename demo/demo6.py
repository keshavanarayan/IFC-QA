import ifcopenshell
import ifcopenshell.util.representation
import ifcopenshell.entity_instance
#import util.ifc_util as util



# Open the IFC file
#file = ifcopenshell.open("ifc/3557 LAWRENCE_MAIN_R20_BASE DESIGN_detached.ifc")
file = ifcopenshell.open("ifc/rac_advanced_sample_project.ifc")

# Get the door element
door = file.by_type("IfcDoor")[2]

contexts = file.by_type("IfcRepresentationContext")

for each in contexts:
    if each.ContextIdentifier == "Body":
        context = each


nested_elements = ifcopenshell.util.representation.get_representation(door,context)
print(ifcopenshell.entity_instance.id(door))
print((door.ObjectPlacement.RelativePlacement.Axis.DirectionRatios))
print((door.ObjectPlacement.RelativePlacement.Location.Coordinates))
print((door.ObjectPlacement.RelativePlacement.RefDirection.DirectionRatios))








for element in nested_elements:
    #print(element)
    if type(element) == ifcopenshell.entity_instance:
        #print(element.is_a())
        #print(element.RepresentationsInContext[0].Items[0].FbsmFaces[0].CfsFaces[0].Bounds[0].Bound.Polygon)
        #for rep in element.RepresentationsInContext:
        #    print (rep)
        #print((element.RepresentationsInContext))
        #print (element.RepresentationsInContext[0].Items)
        #print (util.get_bounding_box_height(element,file.schema))

        print (".........................")
        continue
    else:
        #print(dir(element))
        print (".........................")
        print (".........................")
        continue




