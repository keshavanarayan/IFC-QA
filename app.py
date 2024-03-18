import io
import streamlit as st
import ifcopenshell
import pandas as pd
from util import qc_helper as qc
from util import ada_helper as ada

wall_excel_data = []
door_excel_data =[]
floor_excel_data =[]

def main():
    st.title("DODDA Cloud Validator")
    #st.write("Upload your IFC file below:")

    st.sidebar.header("Upload your IFC file below:")

    uploaded_file = st.sidebar.file_uploader("", type=["ifc"])

    tab1, tab2, tab3 = st.tabs(["🧱 Best Practices", "♿ ADA", "🏗️ Viewer"])

    
    if uploaded_file is not None:

        # TODO: write to server if needed
        # with open(uploaded_file.name, "wb") : 
        #     f.write(uploaded_file.getvalue())

        ifc_file = uploaded_file.getvalue()
        ifc = ifcopenshell.file.from_string(ifc_file.decode("utf-8"))

        st.sidebar.write(f"Schema: {ifc.schema}") 
        st.sidebar.write(f"Project Units: {qc.get_project_units(ifc)[0]}")

        storeys = qc.get_storey_heights(ifc)

        project_data = pd.DataFrame(data=storeys, columns=['Storey Name', 'Storey Height'])
        st.sidebar.table(project_data)


        #print(storeys)
        #for storey in storeys:
         #   st.sidebar.write(f"Storey Name: {storey[0]}, Storey Height: {storey[1]}")



        # TODO: add tolerance
        # st.sidebar.slider("Tolerance", 0, 100)
        with tab1:
            
            with st.expander("Walls Check", expanded=True):
                walls, walls_major, walls_minor, walls_ok = qc.check_walls(ifc)

                st.header(f"Walls in file : {len(walls)}")

                st.header(f"Walls with Major Issues : {len(walls_major)}")
                table1_data = pd.DataFrame(data=walls_major, columns=['IDs', 'Type', 'Issues'])
                st.table(table1_data)
                wall_excel_data.append([table1_data,"Walls With Major Issues"])

                st.header(f"Walls with Minor Issues : {len(walls_minor)}")
                table2_data = pd.DataFrame(data=walls_minor, columns=['IDs', 'Type', 'Issues'])
                st.table(table2_data)
                wall_excel_data.append([table2_data,"Walls with Minor Issues"])

                st.header(f"Walls with No Issues : {len(walls_ok)}")

                st.divider()

                non_vertical_walls = qc.are_walls_vertical(ifc)
                st.header(f"Wall Verticality + Wall Modelling Issues : {len(non_vertical_walls)}")
                table3_data = pd.DataFrame(data=non_vertical_walls, columns=['IDs', 'Type', 'Issues'])
                st.table(table3_data)
                wall_excel_data.append([table3_data,"Wall Verticality + Modelling"])

                st.divider()

                # Download button for exporting data as Excel
                st.download_button(label="Download Excel", data=download_excel(wall_excel_data), file_name="wall_data.xlsx", mime="application/octet-stream")
        
        with tab2:
            with st.expander("Doors Check",expanded=True):
                doors,doors_major,doors_minor,doors_ok = ada.check_doors(ifc)
                st.header(f'Number of Doors in file : {len(doors)}')

                st.header(f"Doors with Major Issues : {len(doors)}")
                table4_data = pd.DataFrame(data=doors_major, columns=['IDs', 'Type', 'Issues'])
                st.table(table4_data)
                door_excel_data.append([table4_data,"Doors with Major Issues"])

                st.header(f"Doors with Minor Issues : {len(doors_minor)}")
                table5_data = pd.DataFrame(data=doors_minor, columns=['IDs', 'Type', 'Issues'])
                st.table(table5_data)
                door_excel_data.append([table5_data,"Doors with Minor Issues"])

                st.header(f"Doors with No Issues : {len(doors_ok)}")

                st.divider()

                 # Download button for exporting data as Excel
                st.download_button(label="Download Excel", data=download_excel(door_excel_data), file_name="door_data.xlsx", mime="application/octet-stream")
            
            with st.expander("Floors Check",expanded=True):
                floors, floors_major, floors_minor, floors_ok = ada.check_floors(ifc)
                st.header(f'Number of Floors in file : {len(floors)}')

                st.header(f"Floors with Major Issues : {len(floors_major)}")
                table6_data = pd.DataFrame(data=floors_major, columns=['IDs', 'Type', 'Issues'])
                st.table(table6_data)
                floor_excel_data.append([table6_data,"Floors with Major Issues"])


                


        
        with tab3:
            st.header("Hello")

        
def download_excel(data):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        for table_data in data:
            table_data[0].to_excel(writer, sheet_name=table_data[1],index = False)
    
    #TODO: write to server if needed
    
    #with open("wall_data.xlsx", "rb") as f:
    #    data = f.read()
    #return data

    
        
    return buffer


if __name__ == "__main__":
    main()
