import ifcopenshell
import functions as qc


ifc_file_path = 'your_ifc_file.ifc'

storey_heights = qc.get_storey_heights(ifc_file_path)

# Print the heights of all storeys
for i, height in enumerate(storey_heights, 1):
    print(f"Storey {i} Height: {height}")

qc.check_walls_in_storeys(ifc_file_path)

tolerance = 1e-5

non_vertical_walls = qc.are_walls_vertical(ifc_file_path, tolerance)

if non_vertical_walls:
    print("The following walls are not vertical:")
    for wall_id in non_vertical_walls:
        print(f"Wall ID: {wall_id}")
else:
    print("All walls are vertical.")