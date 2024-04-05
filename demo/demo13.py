import ifcopenshell
import ifcopenshell.geom

# Open the IFC file
ifc_file = ifcopenshell.open("ifc/rac_advanced_sample_project.ifc")
settings = ifcopenshell.geom.settings()
settings.set(settings.USE_PYTHON_OPENCASCADE, True)

products = ifc_file.by_type("IfcWall")[0]

for i, product in enumerate(products):
    if product.Representation is not None:
        try:
            created_shape = geom.create_shape(settings, inst=product)
            shape = created_shape.geometry # see #1124
            shape_gpXYZ = shape.Location().Transformation().TranslationPart() # These are methods of the TopoDS_Shape class from pythonOCC
            print(shape_gpXYZ.X(), shape_gpXYZ.Y(), shape_gpXYZ.Z()) # These are methods of the gpXYZ class from pythonOCC
        except:
            print("Shape creation failed")