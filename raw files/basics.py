import requests 
from pydantic import BaseModel, Field #, confloat
import uuid
from datetime import date
#from typing import Union, Optional   #these can be used if you are using ptyhon less than 3.9

#getting the data from github uploaded data
url = 'https://raw.githubusercontent.com/bugbytes-io/datasets/master/students_v1.json'
response = requests.get(url) 

#converting the data from json to python dict using .json 
data = response.json()
#print(data)

#defining pydantic class by inheriting its basemodel
class Student(BaseModel):
    """this performs data validation and conversion on the basis of datatypes of the BaseModel subclass"""
    id: uuid.UUID
    name: str
    date_of_birth: date
    GPA: float 
    course: str | None #(Either the value will be str or None if not provided   # or Union[str, None](below python 3.9) or use Optional from python 
    #Optional[str] = Union[str, None] = str | None all are same 
    department: str
    fees_paid: bool


for student in data: #student will be a dict now with some key val pairs 
    model = Student(**student)  #sending all the k-v pairs(kwargs) to Student pydantic model
    #this converts all the dict fields into the provided object type in the Pydantic Model 
    print(model)  
    #as the dob is convert to data object in the result date_of_birth=datetime.date(1995, 5, 25)



#https://www.bugbytes.io/posts/introduction-to-pydantic/ blog post for more info


"""input json object :
   {
        "id": "d15782d9-3d8f-4624-a88b-c8e836569df8",
        "name": "Eric Travis",
        "date_of_birth": "1995-05-25",
        "GPA": "3.0",
        "course": "Computer Science",
        "department": "Science and Engineering",
        "fees_paid": false
    }

Output Pydantic Model Object:
Student(
    id=UUID('d15782d9-3d8f-4624-a88b-c8e836569df8'),
    name='Eric Travis',
    date_of_birth=datetime.date(1995, 5, 25),
    GPA=3.0,
    course='Computer Science',
    department='Science and Engineering',
    fees_paid=False
)"""



"""
Implementing the constraint that we learnt from constrained_types.py
"""

class Student1(BaseModel):
    """this performs data validation and conversion on the basis of datatypes of the BaseModel subclass"""
    id: uuid.UUID
    name: str
    date_of_birth: date
    GPA: float = Field(ge=0, le=4)
    #or GPA: confloat(ge=0, le=4)
    course: str | None 
    department: str
    fees_paid: bool



