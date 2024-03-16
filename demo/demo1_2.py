import ifcopenshell
import ifcopenshell.api

# Open the IFC file
file = ifcopenshell.open("ifc/rac_advanced_sample_project.ifc")

# Get all walls in the file
wall = file.by_type("IfcWall")[50]

#print (ifcopenshell.entity_instance.id(walls[0]))



#for extruded solids
#print(wall.Representation.Representations[1].Items[0].ExtrudedDirection) 
#print(dir(wall.Representation.Representations[1].Items[0].ExtrudedDirection))


#for clippings
#print(wall.Representation.Representations[1].Items[0].FirstOperand.ExtrudedDirection) 
#print(dir(wall.Representation.Representations[1].Items[0].FirstOperand.ExtrudedDirection))

#for breps
print (wall.Representation.Representations)


