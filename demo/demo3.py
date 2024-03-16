import ifcopenshell
import ifcopenshell.util.shape

# Open the IFC file
file = ifcopenshell.open("ifc/rac_advanced_sample_project.ifc")
#file = ifcopenshell.open("ifc\example project location.ifc")

# Get the brep
brep = file.by_type("IfcFacetedBrep")[0]

#print (dir(brep))
#print(brep.Outer)

#print (dir(brep.Outer.CfsFaces[0].Bounds[0].Bound.Polygon[0].Coordinates))


"""
for vertex in brep.Outer.CfsFaces[0].Bounds[0].Bound.Polygon:
    print(vertex.Coordinates)"""

vertices = []

for face in brep.Outer.CfsFaces:
    bounds = face.Bounds
    for bound in bounds:
        polygon = bound.Bound.Polygon
        for vertex in polygon:
            #print(vertex.Coordinates)
            vertices.append(vertex)

#ifcopenshell.util.shape.get_bbox(vertices)

#print (max(vertices, key=lambda v: v[0]))
print(max(vertices))
print(min(vertices))
#print(brep.Outer.CfsFaces[0].Bounds[0].Bound.Polygon[0].Coordinates)

print((max(vertices).Coordinates[2]-min(vertices).Coordinates[2]))

"""
#Print the vertices
for vertex in vertices:
   print(vertex.Coordinates)"""