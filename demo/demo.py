import ifcopenshell.util.element

#ifc_file_path = 'models/rac_advanced_sample_project.ifc'
ifc_file_path = 'ifc\AC2Ø-Institute-Var-2.ifc'
#ifc_file_path = 'models\House.ifc'
#ifc_file_path = 'models\example project location.ifc'

model = ifcopenshell.open(ifc_file_path)

for storey in model.by_type("IfcBuildingStorey"):
    print(f"Elevation = {storey.Elevation}")
    elements = ifcopenshell.util.element.get_decomposition(storey)
    print(f"There are {len(elements)} elements located on storey {storey.Name}")

    bounding_dim = 0
    max_dim = 0
    
    for element in elements:
        if (element.is_a("IfcStair")):
            continue
        geom_items = element.Representation.Representations
        #print(element.Representation.Representations)
        #print (geom_items)
        
        if not geom_items:
            continue  # No geometry found

        for geom_item in geom_items:
            shape = geom_item.Items[0]
            
            if geom_item.is_a('IfcShapeRepresentation') and shape:
                representation_type = geom_item.RepresentationType
                #print (representation_type)
                if representation_type == 'BoundingBox':
                    if shape.ZDim > max_dim:
                        max_dim = shape.ZDim
                elif representation_type == 'SweptSolid':
                    if shape.Depth >max_dim:
                        max_dim = shape.Depth
                elif representation_type == 'Clipping':
                    continue
                elif representation_type == 'Curve2D':
                    #return geom_item.Items[0].Depth
                    #print(shape)
                    continue
                elif representation_type == 'Brep':
                    #return geom_item.Items[0].Depth
                    #print(shape)
                    continue

                else:
                    continue
                    #print (f"EXTRA PROBLEM - {geom_item.Items[0]}")
        
            if max_dim>bounding_dim:
                bounding_dim = max_dim
    print (f"Bounding Dim = {bounding_dim}")
    print ("..")
        
