import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.shape
import ifcopenshell.util.element
import ifcopenshell.util.constraint
import ifcopenshell.util.unit
import ifcopenshell.entity_instance
import ifcopenshell.util
settings = ifcopenshell.geom.settings()

def get_id(element):
    #return element.GlobalId
    return ifcopenshell.entity_instance.id(element)


def get_brep_height(brep):

    vertices = []
    for face in brep.Outer.CfsFaces:
        bounds = face.Bounds
        for bound in bounds:
            polygon = bound.Bound.Polygon
            for vertex in polygon:
                #print(vertex.Coordinates)
                vertices.append(vertex)

    ##print(brep.Outer.CfsFaces[0].Bounds[0].Bound.Polygon[0].Coordinates)
    return max(vertices).Coordinates[2]-min(vertices).Coordinates[2]


#TODO: find solution if it is a Boolean Clipping result
def get_bounding_box_height(element,schema):

    """VERSION 2 for IFC 4.0"""
    geom_items = element.Representation.Representations
    #print (geom_items)
    if not geom_items:
        return None  # No geometry found
    
    for geom_item in geom_items:
        shape = geom_item.Items[0]
        if geom_item.is_a('IfcShapeRepresentation') and shape:
            representation_type = geom_item.RepresentationType
            #print (representation_type)
            match representation_type:
                case 'BoundingBox':
                    return shape.ZDim
                case 'SweptSolid':
                    return shape.Depth
                case 'Clipping':
                    if schema =="IFC2X3":
                        return shape.FirstOperand.Depth
                        print(shape.FirstOperand)
                        continue
                case 'Brep':
                    return get_brep_height(shape)
                case _:
                    #print (f"EXTRA PROBLEM - {shape}")
                    continue

def get_extrusion_direction(element,schema):
    """VERSION 2 for IFC 4.0"""
    geom_items = element.Representation.Representations
    #print (geom_items)
    if not geom_items:
        return None  # No geometry found
    
    for geom_item in geom_items:
        shape = geom_item.Items[0]
        if geom_item.is_a('IfcShapeRepresentation') and shape:
            representation_type = geom_item.RepresentationType
            #print (representation_type)
            match representation_type:
                case 'BoundingBox':
                    return shape.ExtrudedDirection
                case 'SweptSolid':
                    return shape.ExtrudedDirection
                case 'Clipping':
                    if (schema =="IFC2X3"):
                        return shape.FirstOperand.ExtrudedDirection
                        print(shape.FirstOperand)
                        continue
                case 'Brep':
                    #print(dir(shape.Outer))
                    return "Brep"
                    #print (f"EXTRA PROBLEM - {shape}")
                    continue
                case _:
                    #print (f"EXTRA PROBLEM - {shape}")
                    continue