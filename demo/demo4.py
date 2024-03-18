import ifcopenshell

def get_door_style(ifc_file_path):
    # Load the IFC file
    ifc_file = ifcopenshell.open(ifc_file_path)

    # Get the IfcDoor with the specified id
    door = ifc_file.by_type("IfcDoor")[0]

    if door is None or door.is_a() != 'IfcDoor':
        return None  # If no door found or the found object is not a door

    # Get the IfcDoorStyle of the door
    door_style = ifc_file.by_id(door.Representation.Representations[0].Items[0])

    if door_style is None or door_style.is_a() != 'IfcDoorType':
        return None  # If no door style found or the found object is not a door style

    return door_style

# Example usage
ifc_file_path = 'ifc/rac_advanced_sample_project.ifc'
door_id = 123456  # Replace with the actual IfcDoor id from your IFC file
door_style = get_door_style(ifc_file_path)

if door_style:
    print("Door Style ID:", door_style.id)
    print("Door Style Name:", door_style.Name)
else:
    print("Door style not found.")
