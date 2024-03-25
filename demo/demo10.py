import ifcopenshell
import ifcopenshell.util.element

file = ifcopenshell.open("ifc/rac_advanced_sample_project.ifc")

# Get all IfcSpace elements in the file
spaces = file.by_type("IfcSpace")

"""
substring = "Cafe"

# Iterate over the spaces and get all elements contained in each space
for space in spaces:
    if substring.lower() in str(space.LongName).lower():
        rel_contained = space.ContainsElements
        for rel in rel_contained:
            if rel.RelatedElements:
                print (f"-----------{space.LongName}------------")
                for elem in rel.RelatedElements:
                    print(elem.Name)
"""