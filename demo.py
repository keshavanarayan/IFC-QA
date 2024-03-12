import ifcopenshell.util.element

#ifc_file_path = 'models/rac_advanced_sample_project.ifc'
ifc_file_path = 'models\AC2Ø-Institute-Var-2.ifc'
#ifc_file_path = 'models\House.ifc'
#ifc_file_path = 'models\example project location.ifc'

model = ifcopenshell.open(ifc_file_path)

for storey in model.by_type("IfcBuildingStorey"):
    elements = ifcopenshell.util.element.get_decomposition(storey)
    print(f"There are {len(elements)} located on storey {storey.Name}, they are:")
    #print (storey.containselements)
    #for element in elements:
        #print(element.Name)
        #print (element.ObjectType)
        #print (element.Tag)

        
