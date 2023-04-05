import datetime
import re

DATE_FORMATS = [
    '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%d-%b-%y', '%d-%b-%Y', '%d/%m/%Y', '%d/%m/%y',
    '%Y/%m/%d', '%Y%m%d', '%d%b%Y', '%d%b%y', '%Y/%b/%d', '%Y-%b-%d', '%Y-%b-%d %H:%M:%S',
    '%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S', '%m/%d/%Y %H:%M:%S', '%m/%d/%y %H:%M:%S',
    '%d-%b-%y %H:%M:%S', '%d-%b-%Y %H:%M:%S', '%d/%m/%Y %H:%M:%S', '%d/%m/%y %H:%M:%S',
    '%Y%m%d %H:%M:%S', '%d%b%Y %H:%M:%S', '%d%b%y %H:%M:%S', '%Y/%b/%d %H:%M:%S',
    '%Y-%b-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S.%f', '%Y/%m/%d %H:%M:%S.%f',
    '%m/%d/%Y %H:%M:%S.%f', '%m/%d/%y %H:%M:%S.%f', '%d-%b-%y %H:%M:%S.%f',
    '%d-%b-%Y %H:%M:%S.%f', '%d/%m/%Y %H:%M:%S.%f', '%d/%m/%y %H:%M:%S.%f',
    '%Y%m%d %H:%M:%S.%f', '%d%b%Y %H:%M:%S.%f', '%d%b%y %H:%M:%S.%f', '%Y/%b/%d %H:%M:%S.%f'
]

class CSVSchemaInference:
    def __init__(self):
        self.headers = []
        self.data_types = {}
        self.date_formats = []

    def infer_schema(self, csv_file_path):
        with open(csv_file_path, 'r') as f:
            lines = f.readlines()

            # extract headers
            self.headers = lines[0].strip().split(',')

            # initialize data type for each column
            for header in self.headers:
                self.data_types[header] = set()

            # loop through data rows and update data type for each column
            for line in lines[1:]:
                values = line.strip().split(',')
                for i, value in enumerate(values):
                    # try parsing as int
                    try:
                        int(value)
                        self.data_types[self.headers[i]].add(int)
                        continue
                    except ValueError:
                        pass

                    # try parsing as float
                    try:
                        float(value)
                        self.data_types[self.headers[i]].add(float)
                        continue
                    except ValueError:
                        pass

                    # try parsing as date or timestamp
                    for date_format in DATE_FORMATS:
                        try:
                            datetime.datetime.strptime(value, date_format)
                        self.data_types[self.headers[i]].add(datetime.datetime)
                        self.date_formats.append(date_format)
                        break
                    except ValueError:
                        pass

        # convert data types to single type if possible
        for header in self.headers:
            if len(self.data_types[header]) == 1:
                self.data_types[header] = next(iter(self.data_types[header]))
            else:
                self.data_types[header] = str

        return {
            'headers': self.headers,
            'data_types': self.data_types,
            'date_formats': self.date_formats
        }

