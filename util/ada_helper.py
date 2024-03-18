import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.shape
import ifcopenshell.util.element
import ifcopenshell.util.constraint
import ifcopenshell.util.unit
import ifcopenshell.entity_instance
import ifcopenshell.util

settings = ifcopenshell.geom.settings()

#TODO:use dir(element) to find attributes of elements


def check_doors(ifc_file):
    #TODO: finish door accessibility
    doors = ifc_file.by_type("IfcDoor")

    print (dir(doors[0]))


    pass