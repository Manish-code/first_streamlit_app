# streamlit_app.py

import streamlit as st
import snowflake.connector as sf
import pandas as pd

# Connect to Snowflake
conn = sf.connect(
    user = "SUGARDATA",
    password = "HomeAlone@1",
    account = "ub37293.ap-southeast-1",
    warehouse = "COMPUTE_WH",
    database = "TEST",
    schema = "PUBLIC"
)

# Create a cursor object
cur = conn.cursor()


uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    st.write(bytes_data)

if uploaded_file  is not None:
    table_name =uploaded_file.name.split(".")[0].replace(" ","_").upper()
    columns = ",".join([f"{col} string" for col in df.columns])
    
    cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name}c({columns})")
    cur.commit()                   
                      
    cur.execute(f"PUT {uploaded_file} @~ auto_compress=false;")
    cur.commit()                     
    cur.execute(f"COPY INTO {table_name} FROM '@~/{uploaded_file}' FILE_FORMAT = (TYPE = 'CSV');")
    cur.commit()                     
    cur.execute(f"LIST @%{table_name);")
    cur.commit() 
                        



# Execute a query
cur.execute(f"SELECT * FROM {table_name}")

# Fetch the data
data = cur.fetchall()
cur.execute("SELECT current_version()")
one_row = cur.fetchone()
print(one_row[0])

# Display the data in a Streamlit table
st.table(data)


