import csv
import datetime

def infer_data_types(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        data_types = []
        for i in range(len(headers)):
            data_type = None
            for row in reader:
                if row[i] == '':
                    continue
                if data_type is None:
                    if row[i].lower() in ('true', 'false'):
                        data_type = bool
                    elif row[i].isdigit():
                        data_type = int
                    else:
                        try:
                            float(row[i])
                            data_type = float
                        except ValueError:
                            try:
                                datetime.datetime.strptime(row[i], '%Y-%m-%d')
                                data_type = datetime.date
                            except ValueError:
                                try:
                                    datetime.datetime.strptime(row[i], '%Y-%m-%d %H:%M:%S.%f')
                                    data_type = datetime.datetime
                                except ValueError:
                                    data_type = str
                elif data_type == bool:
                    if row[i].lower() not in ('true', 'false'):
                        data_type = str
                elif data_type == int:
                    if not row[i].isdigit():
                        try:
                            float(row[i])
                            data_type = float
                        except ValueError:
                            data_type = str
                elif data_type == float:
                    try:
                        float(row[i])
                    except ValueError:
                        data_type = str
                elif data_type == datetime.date:
                    try:
                        datetime.datetime.strptime(row[i], '%Y-%m-%d')
                    except ValueError:
                        data_type = str
                elif data_type == datetime.datetime:
                    try:
                        datetime.datetime.strptime(row[i], '%Y-%m-%d %H:%M:%S.%f')
                    except ValueError:
                        data_type = str
            data_types.append(data_type)
    return data_types

data_types = infer_data_types('sample_data.csv')
print(data_types)

# Expected output
# [<class 'bool'>, <class 'int'>, <class 'datetime.date'>, <class 'datetime.time'>, <class 'datetime.datetime'>, <class 'str'>, <class 'dict'>, <class 'list'>]
