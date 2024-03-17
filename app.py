import streamlit as st
import ifcopenshell
from util import ifc_helper as qc
import pandas as pd
import io

def main():
    st.title("DODDA ADA Validator")
    st.write("Upload your IFC file below:")

    uploaded_file = st.file_uploader("Upload IFC file", type=["ifc"])

    excel_data = []

    if uploaded_file is not None:

        # TODO: write to server if needed
        # with open(uploaded_file.name, "wb") : 
        #     f.write(uploaded_file.getvalue())

        ifc_file = uploaded_file.getvalue()
        ifc = ifcopenshell.file.from_string(ifc_file.decode("utf-8"))

        st.write(f"Schema: {ifc.schema}") 
        st.write(f"Project Units: {qc.get_project_units(ifc)}")

        # TODO: add tolerance
        # st.slider("Tolerance", 0, 100)

        storeys = qc.get_storey_heights(ifc)

        walls, walls_major, walls_minor, walls_ok = qc.check_wall_heights(ifc)

        st.header(f"Walls in file : {len(walls)}")

        st.header(f"Walls with Major Issues : {len(walls_major)}")
        table1_data = pd.DataFrame(data=walls_major, columns=['IDs', 'Type', 'Issues'])
        st.table(table1_data)
        excel_data.append([table1_data,"Walls With Major Issues"])

        st.header(f"Walls with Minor Issues : {len(walls_minor)}")
        table2_data = pd.DataFrame(data=walls_minor, columns=['IDs', 'Type', 'Issues'])
        st.table(table2_data)
        excel_data.append([table2_data,"Walls with Minor Issues"])

        st.header(f"Walls with No Issues : {len(walls_ok)}")

        st.divider()

        non_vertical_walls = qc.are_walls_vertical(ifc)
        st.header(f"Wall Verticality + Wall Modelling Issues : {len(non_vertical_walls)}")
        table3_data = pd.DataFrame(data=non_vertical_walls, columns=['IDs', 'Type', 'Issues'])
        st.table(table3_data)
        excel_data.append([table3_data,"Wall Verticality + Modelling"])

        st.divider()

        #print (qc.has_repeating_elements(walls_ok))
        #print (qc.has_repeating_elements(walls))
        #print (qc.has_repeating_elements(walls_major))
        #print (qc.has_repeating_elements(walls_minor))

        # Download button for exporting data as Excel
        st.download_button(label="Download Excel", data=download_excel(excel_data), file_name="wall_data.xlsx", mime="application/octet-stream")

        
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
