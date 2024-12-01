from pydantic import BaseModel, Field, field_validator
import uuid
from datetime import date, datetime, timedelta
from _enum import DepartmentEnum
import requests


class Student(BaseModel):
    """this performs data validation and conversion on the basis of datatypes of the BaseModel subclass"""
    id: uuid.UUID
    name: str
    date_of_birth: date
    GPA: float = Field(ge=0, le=4)
    course: str | None 
    department: DepartmentEnum
    fees_paid: bool

    @field_validator('date_of_birth')
    def ensure_16_or_over(cls, value):  
        sixteen_years_ago = datetime.now() - timedelta(365*16)  
        sixteen_years_ago = sixteen_years_ago.date()
        if value > sixteen_years_ago:
            raise ValueError("To young")
        return value
    

url = 'https://raw.githubusercontent.com/bugbytes-io/datasets/master/students_v1.json'
response = requests.get(url) 
print(response.content) #this is a byte object 

"""
Prefix b: Indicates that the data is in bytes format, not a standard string.
Structure: Inside the bytes object, the content appears to be a JSON-formatted string. Once decoded, it will represent a JSON array of objects, where each object has fields like id, name, date_of_birth, GPA, etc.
"""


#converting the data from json to python json using .json 
data = response.json()


for student in data:
    res = Student(**student)
    # print(res.model_dump())   #convert data to dict 
    print(res.model_dump_json())

    #the diff bw json and dict is that the json serializes the more complex object to less complex object that can be esasily understood by the program 
    #like the uuid obj will be converted to str, the date time obj will be converted to str too 
    #you can check the diff between dict and json can be seen in the output given below  
"""
1. Dict Response:
{'id': UUID('7ffe2ceb-562b-4edd-b74c-3741e1b08453'), 'name': 'Michelle Thompson', 'date_of_birth': datetime.date(1995, 8, 5), 'GPA': 3.9, 'course': 'Film Studies', 'department': <DepartmentEnum.ARTS_AND_HUMANITIES: 'Arts and Humanities'>, 'fees_paid': True}
2. Json Response:
{"id":"7ffe2ceb-562b-4edd-b74c-3741e1b08453","name":"Michelle Thompson","date_of_birth":"1995-08-05","GPA":3.9,"course":"Film Studies","department":"Arts and Humanities","fees_paid":true}

So, from here we concluded that dict supports all the complex data types and sends them as it is, while the json doesn't support all the types of complex data types, so it converts all the complex data types to the primitive data types 
"""


