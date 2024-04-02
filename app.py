import io
import streamlit as st
import streamlit.components as components
import ifcopenshell
import pandas as pd
import numpy as np
from util import qc_helper as qc
from util import ada_helper as ada
from util import ifc_util as util

wall_excel_data = []
door_excel_data =[]
floor_excel_data =[]
toilets_excel_data =[]

ada_data =[]
qc_data =[]


def main():
    st.title("DODDA BIM Validator")
    #st.write("Upload your IFC file below:")

    st.sidebar.header("Upload your IFC file below:")

    uploaded_file = st.sidebar.file_uploader("", type=["ifc"])

    tab1, tab2, tab3 = st.tabs(["🧱 Best Practices", "♿ ADA", "🏗️ Viewer"])

    
    if uploaded_file is not None:

        # FIXME: write to server if needed
        # with open(uploaded_file.name, "wb") : 
        #     f.write(uploaded_file.getvalue())

        ifc_file = uploaded_file.getvalue()
        ifc = ifcopenshell.file.from_string(ifc_file.decode("utf-8"))

        st.sidebar.write(f"Schema: {ifc.schema}") 
        st.sidebar.write(f"Project Units: {util.get_project_units(ifc)[0]}")

        storeys = qc.get_storey_heights(ifc)

        project_data = pd.DataFrame(data=storeys, columns=['Storey Name', 'Storey Height'])
        st.sidebar.table(project_data)

        # TODO: add tolerance in all qc+ ada functions
        tolerance = st.sidebar.slider("Tolerance in metres", 0.0, 1.0)
        


        with tab1:
            
            walls, walls_major, walls_minor, walls_ok = qc.check_walls(ifc)

            st.header(f"Total Walls in file : {len(walls)}")

            #print no. of issues as table
            st.table(pd.DataFrame(data=np.array([len(walls_ok),len(walls_major)+len(walls_minor)]).reshape(-1,2), columns=["Pass ✅","Fail ❌"]))
            
            table1_data = pd.DataFrame(data=walls_major, columns=['IDs', 'Type', 'Issues','Pass/Fail'])
            table2_data = pd.DataFrame(data=walls_minor, columns=['IDs', 'Type', 'Issues','Pass/Fail'])
            table2_1_data = pd.DataFrame(data=walls_ok, columns=['IDs', 'Type', 'Issues','Pass/Fail'])

            non_vertical_walls = qc.are_walls_vertical(ifc)
            table3_data = pd.DataFrame(data=non_vertical_walls, columns=['IDs', 'Type', 'Issues','Pass/Fail'])

            wall_excel_data = pd.concat([table2_1_data, table1_data, table2_data, table3_data], ignore_index=True)
            
            qc_data.append([wall_excel_data,"Walls Check"]) 
            
            with st.expander("View Walls Details", expanded=False): st.table(wall_excel_data)
                
            # Download button for exporting data as Excel
            st.download_button(label="Download Best Practices Issues as Excel", data=download_excel(qc_data), file_name="qc_data.xlsx", mime="application/octet-stream")
            #st.download_button(label="Download Best Practices Conventions", data=download_excel(qc_data), file_name="qc_data.xlsx", mime="application/octet-stream")

        st.divider()    
        

        
        with tab2:

                #------------DOORS------------#
            
                doors,doors_major,doors_minor,doors_ok = ada.check_doors(ifc)
                st.header(f'Number of Doors in file : {len(doors)}')

                #print no. of issues as table
                st.table(pd.DataFrame(data=np.array([len(doors_ok),len(doors_major)+len(doors_minor)]).reshape(-1,2), columns=["Pass ✅","Fail ❌"]))

                table4_data = pd.DataFrame(data=doors_major, columns=['IDs', 'Type', 'Issues','Pass/Fail'])
                table5_data = pd.DataFrame(data=doors_minor, columns=['IDs', 'Type', 'Issues','Pass/Fail'])
                table5_1_data = pd.DataFrame(data=doors_ok, columns=['IDs', 'Type', 'Issues','Pass/Fail'])

                door_excel_data = pd.concat([table5_1_data,table4_data, table5_data], ignore_index=True)

                with st.expander("View Doors Details",expanded=True): st.table(door_excel_data)

                st.divider()

                ada_data.append([door_excel_data,"Doors Check"])

                #------------FLOORS------------#
                       
                floors, floors_major, floors_minor, floors_ok = ada.check_floors(ifc)
                st.header(f'Number of Floors in file : {len(floors)}')

                #print no. of issues as table
                st.table(pd.DataFrame(data=np.array([len(floors_ok),len(floors_major)+len(floors_minor)]).reshape(-1,2), columns=["Pass ✅","Fail ❌"]))


                table6_data = pd.DataFrame(data=floors_major, columns=['IDs', 'Type', 'Issues','Pass/Fail'])
                table7_data = pd.DataFrame(data=floors_minor, columns=['IDs', 'Type', 'Issues','Pass/Fail'])
                table7_1_data = pd.DataFrame(data=floors_ok, columns=['IDs', 'Type', 'Issues','Pass/Fail'])

                floor_excel_data = pd.concat([table7_1_data,table6_data, table7_data], ignore_index=True)

                with st.expander("View Floors Details",expanded=True): st.table(floor_excel_data)

                ada_data.append([floor_excel_data,"Floors Check"])

                st.divider()
                
                #------------TOILETS------------#

                #TODO:finish toilets check

                toilets = ada.check_toilets(ifc)
                st.header(f'Number of Toilets in file : {len(toilets)}')

                
                #toilets, toilets_major, toilets_minor, toilets_ok = ada.check_toilets(ifc)
                #st.header(f'Number of Toilets in file : {len(toilets)}')

                #print no. of issues as table
                #st.table(pd.DataFrame(data=np.array([len(toilets_ok),len(toilets_major)+len(toilets_minor)]).reshape(-1,2), columns=["Pass ✅","Fail ❌"]))

                
                #st.header(f"Toilets with Major Issues : {len(toilets_major)}")
                #table8_data = pd.DataFrame(data=toilts_major, columns=['IDs', 'Type', 'Issues'])
                #st.table(table8_data)
                #floor_excel_data.append([table8_data,"Toilets with Major Issues"])

                #st.header(f"Toilets with Minor Issues : {len(toilets_minor)}")
                #table9_data = pd.DataFrame(data=toilets_minor, columns=['IDs', 'Type', 'Issues'])
                #st.table(table9_data)
                #floor_excel_data.append([table9_data,"Toilets with Minor Issues"])

                #st.header(f"Toilets with No Issues : {len(toilets_ok)}")


                #------------CORRIDORS------------#

                #TODO:finish corridors check

                #corridors, corridors_major, corridors_minor, corridors_ok = ada.check_corridors(ifc)
                corridors = ada.check_corridors(ifc)
                st.header(f'Number of Corridors in file : {len(corridors)}')

                #print no. of issues as table
                #st.table(pd.DataFrame(data=np.array([len(corridors_ok),len(corridors_major)+len(corridors_minor)]).reshape(-1,2), columns=["Pass ✅","Fail ❌"]))

                # Download button for exporting data as Excel
                st.download_button(label="Download Excel", data=download_excel(ada_data), file_name="ada_data.xlsx", mime="application/octet-stream")
        

        with tab3:
            st.header("Hello")
        
        
        

        
def download_excel(data):
    """
    Downloads the given data as an Excel file and returns the file as a buffer.
    
    Args:
        data: The data to be written to the Excel file.
    
    Returns:
        The Excel file as a buffer.
    """
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        for table_data in data:
            if table_data[1]:
                table_data[0].to_excel(writer, sheet_name=table_data[1],index = False)
            else:
                table_data[0].to_excel(writer,index = False)
    
    #FIXME: write to server if needed
    
    #with open("wall_data.xlsx", "rb") as f:
    #    data = f.read()
    #return data

    
        
    return buffer


if __name__ == "__main__":
    main()
