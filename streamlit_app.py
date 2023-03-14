import streamlit as st
import snowflake.connector as snow
from snowpark import SparkSession
from snowpark.sql.types import *

# Connect to Snowflake
conn = snow.connect(
    user='your_username',
    password='your_password',
    account='your_account_name',
    database='your_database_name',
    schema='your_schema_name'
)

# Create a Snowpark session
spark = SparkSession.builder() \
            .option("spark.datasource.username", "your_username") \
            .option("spark.datasource.password", "your_password") \
            .option("spark.datasource.sfUrl", f"jdbc:snowflake://{your_account_name}.snowflakecomputing.com") \
            .option("spark.datasource.sfDatabase", "your_database_name") \
            .option("spark.datasource.sfSchema", "your_schema_name") \
            .getOrCreate()

# Define the schema for the Snowflake table
schema = StructType([
    StructField("col1", StringType(), True),
    StructField("col2", IntegerType(), True),
    StructField("col3", DoubleType(), True)
])



uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

# Upload file to Snowflake using Snowpark
df = spark.read.format("csv").option("header", "true").option("inferSchema", "true").schema(schema).load(uploaded_file)
df.write.format("snowflake").option("dbtable", "your_target_table").mode("append").save()

# Close the Snowpark session and Snowflake connection
spark.stop()
conn.close()





