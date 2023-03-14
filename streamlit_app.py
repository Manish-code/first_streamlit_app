# streamlit_app.py

import streamlit as st
import snowflake.connector as sf

# Connect to Snowflake
conn = sf.connect(
    user = "SUGARDATA",
    password = "HomeAlone@1",
    account = "ub37293",
    warehouse = "COMPUTE_WH",
    database = "TEST",
    schema = "PUBLIC"
)

# Create a cursor object
cur = conn.cursor()

# Execute a query
cur.execute('SELECT * FROM your_table')

# Fetch the data
data = cur.fetchall()
cur.execute("SELECT current_version()")
one_row = cur.fetchone()
print(one_row[0])

# Display the data in a Streamlit table
st.table(data)

uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    st.write(bytes_data)
