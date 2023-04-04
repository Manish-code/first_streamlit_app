import csv
from typing import List
import datetime
def infer_data_types(file_path: str, delimiter: str = ',') -> str:
    """
    Infers the data types of a CSV file's columns and generates a SQL create table query.

    Args:
        file_path (str): The path to the CSV file.
        delimiter (str): The delimiter used in the CSV file. Default is ','.

    Returns:
        str: The SQL create table query.
    """

    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter=delimiter)
        header = next(reader)

        # Initialize counters for each data type
        int_count = 0
        float_count = 0
        bool_count = 0
        date_count = 0
        text_count = 0

        # Iterate through each row of data
        for row in reader:
            for i, value in enumerate(row):
                # Check if the value is an integer
                try:
                    int(value)
                    int_count += 1
                    continue  # Move on to next value if integer
                except ValueError:
                    pass

                # Check if the value is a float
                try:
                    float(value)
                    float_count += 1
                    continue  # Move on to next value if float
                except ValueError:
                    pass

                # Check if the value is a boolean
                if value.lower() in ['true', 'false']:
                    bool_count += 1
                    continue  # Move on to next value if boolean

                # Check if the value is a date
                # You may need to modify this based on the format of your dates
                try:
                    datetime.datetime.strptime(value, '%d-%m-%Y')
                    date_count += 1
                    continue  # Move on to next value if date
                except ValueError:
                    pass

                # If the value is not any of the above, assume it is text
                text_count += 1

        # Determine the data type for each column based on the counters
        data_types = []
        for i in range(len(header)):
            if int_count == len(header):
                data_types.append('int')
            elif i < len(header) - 1 and int_count == i + 1 and float_count == len(header) - i - 1:
                data_types.append('float')  # Column is int followed by float
            elif float_count == len(header):
                data_types.append('float') 
            elif bool_count == len(header):
                data_types.append('bool')
            elif date_count == len(header):
                data_types.append('date')
            else:
                data_types.append('text')

    # Use zip to iterate over both header and data_types together
    # and create a list of strings that define each column in the SQL table
    columns = [f"{col_name} {data_type}" for col_name, data_type in zip(header, data_types)]

    # Join the columns list with commas to create the final SQL create table query
    columns_str = ", ".join(columns)
    sql_query = f"CREATE TABLE table_name ({columns_str});"

    return sql_query
