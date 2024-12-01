import requests
from models import Student

url = 'https://raw.githubusercontent.com/bugbytes-io/datasets/master/students_v3.json'
response = requests.get(url) 
#print(response.content) #this is a byte object 

data = response.json()


for student in data:
    try:
        model = Student(**student)
        # print(model.model_dump())   
        # print(model.model_dump_json())
        print(f"Department: {model.department}, GPA: {model.GPA}")

    except ValueError as e:
            print(e)

