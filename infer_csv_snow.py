import csv

def infer_data_types(csv_file):
    """
    Infer the data types of each column in a CSV file.
    
    Parameters:
        csv_file (str): The path to the CSV file.
        
    Returns:
        A list of data types, one for each column in the CSV file.
    """
    # initialize list of data types
    data_types = [None] * num_columns(csv_file)
    
    # iterate over each row in the CSV file
    with open(csv_file) as f:
        reader = csv.reader(f)
        for row in reader:
            # iterate over each value in the row
            for i, value in enumerate(row):
                # if value is None or empty, skip
                if not value:
                    continue
                
                # check for boolean values
                if value.lower() in ['true', 'false']:
                    data_types[i] = bool
                    
                # check for integer values
                elif value.isdigit() or (value[0] == '-' and value[1:].isdigit()):
                    data_types[i] = int
                    
                # check for floating point values
                elif '.' in value or 'e' in value:
                    try:
                        float_value = float(value)
                        data_types[i] = float
                    except ValueError:
                        pass
                
                # if none of the above match, assume it's a string
                else:
                    data_types[i] = str
    
    # reset file pointer to beginning of file
    f.seek(0)
    
    # iterate over each row in the CSV file again
    with open(csv_file) as f:
        reader = csv.reader(f)
        for row in reader:
            # iterate over each value in the row
            for i, value in enumerate(row):
                # if data type is already set, skip
                if data_types[i] is not None:
                    continue
                
                # check for date values
                if is_date(value):
                    data_types[i] = 'date'
                
                # check for time values
                elif is_time(value):
                    data_types[i] = 'time'
    
    return data_types

def num_columns(csv_file):
    """
    Count the number of columns in a CSV file.
    
    Parameters:
        csv_file (str): The path to the CSV file.
        
    Returns:
        The number of columns in the CSV file.
    """
    with open(csv_file) as f:
        reader = csv.reader(f)
        header = next(reader)
        return len(header)

def is_date(string, fmt='%Y-%m-%d'):
    """
    Check if a string represents a valid date.
    
    Parameters:
        string (str): The string to check.
        fmt (str): The date format to use (default is YYYY-MM-DD).
    
    Returns:
        True if the string is a valid date, False otherwise.
    """
    try:
        datetime.strptime(string, fmt)
        return True
    except ValueError:
        return False

def is_time(string, fmt='%H:%M:%S'):
    """
    Check if a string represents a valid time.
    
    Parameters:
        string (str): The string to check.
        fmt (str): The time format to use (default is HH:MM:SS).
    
    Returns:
        True if the string is a valid time
