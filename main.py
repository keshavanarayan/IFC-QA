import ifcopenshell
import functions as qc


#ifc_file_path = 'models/rac_advanced_sample_project.ifc'
ifc_file_path = 'models\AC2Ø-Institute-Var-2.ifc'
#ifc_file_path = 'models\House.ifc'

print("Checking Verticality...")

tolerance = 1e-5
non_vertical_walls = qc.are_walls_vertical(ifc_file_path, tolerance)

if non_vertical_walls:
    print("The following walls are not vertical:")
    for wall_id in non_vertical_walls:
        print(f"Wall ID: {wall_id}")
else:
    print("All walls are vertical.")


print("Extracting Storey Heights....")
storey_heights = qc.extract_storey_info(ifc_file_path)

#print (storey_heights)

print("Checking Wall Heights....")
#qc.check_walls_in_storeys(ifc_file_path, storey_heights)
qc.check_wall_heights(ifc_file_path)



