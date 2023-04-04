
import streamlit as st
from infer_data_types import infer_data_types
# Import the infer_data_types function from the previous code block

def main():
    st.title("CSV Data Type Inference")

    # Create a file uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type=".csv")

    if uploaded_file is not None:
        # Call the infer_data_types function on the uploaded file
        file_path = f"./{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        table_name = st.text_input("Enter table name:")
        delimiter = st.text_input("Enter delimiter (default is comma):", ",")

        sql_query = infer_data_types(file_path, delimiter=delimiter)
        sql_query = sql_query.replace("table_name", table_name)

        st.write("SQL query:")
        st.code(sql_query)
main()