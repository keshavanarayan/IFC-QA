import ifcopenshell

file = ifcopenshell.open("ifc/rac_advanced_sample_project.ifc")
contexts = file.by_type("IfcRepresentationContext")

for context in contexts:
    print(context.ContextIdentifier)
    print(context)