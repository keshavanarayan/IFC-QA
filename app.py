import streamlit as st
import ifcopenshell
from util import ifc_helper as qc
import streamlit.components.v1 as components

def main():
    st.title("DODDA ADA Validator")
    st.write("Upload your IFC file below:")

    uploaded_file = st.file_uploader("Upload IFC file", type=["ifc"])

    if uploaded_file is not None:

        #TODO:write to server if needed
        #with open(uploaded_file.name, "wb") : 
        #    f.write(uploaded_file.getvalue())

        ifc_file = uploaded_file.getvalue()
        ifc = ifcopenshell.file.from_string(ifc_file.decode("utf-8"))

        st.write(f"Schema: {ifc.schema}") 
        st.write(f"Project Units: {qc.get_project_units(ifc)}")
        #print (qc.extract_storey_heights(ifc))
        #print (qc.extract_storey_heights(ifc))
        qc.get_storey_heights(ifc)
        qc.check_wall_heights(ifc)
        components.html("<hr>")



if __name__ == "__main__":
    main()
