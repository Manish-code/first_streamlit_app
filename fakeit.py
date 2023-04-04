import csv
from faker import Faker
import datetime

def datagenerate(records, headers):
    fake = Faker('en_IN')
    fake1 = Faker('en_IN')   # To generate phone numbers
    with open("People_data.csv", 'wt') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=headers)
        writer.writeheader()
        for i in range(records):
            full_name = fake.name()
            FLname = full_name.split(" ")
            Fname = FLname[0]
            Lname = FLname[1]
            domain_name = "@testDomain.com"
            userId = Fname +"."+ Lname + domain_name
            
            writer.writerow({
                    
                    "Name": fake.name(),
                    "Birth Date" : fake.date(pattern="%d-%m-%Y", end_datetime=datetime.date(2000, 1,1)),
                    "Phone Number" : fake1.phone_number(),
                    "Pin Code" : fake.postcode(),
                    "City" : fake.city(),
                    "State" : fake.state(),
                    "Country" : fake.country(),
                    "Year":fake.year(),
                    
                    })
    
if __name__ == '__main__':
    records = 10
    headers = ["Name", "Birth Date", "Phone Number","Pin Code", "City","State", "Country", "Year"]
    datagenerate(records, headers)
    print("CSV generation complete!")