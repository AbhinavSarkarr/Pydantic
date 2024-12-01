from pydantic import BaseModel, Field, field_validator
import uuid
from datetime import date, datetime, timedelta
from _enum import DepartmentEnum
import requests
from typing import Literal

"""
There are two additional validations we want to add to our Module model, as noted earlier:

1. The credits field can only have the possible values of 10 or 20.
2. If a student has modules, there must only be 3 modules for the academic year.
"""


class Modules(BaseModel):
    id: int | uuid.UUID
    name: str
    professor: str
    credits: Literal[10, 20]   #now it will take the value of credits as only 10 or 20
    registration_code: str

class Student4(BaseModel):
    """this performs data validation and conversion on the basis of datatypes of the BaseModel subclass"""
    id: uuid.UUID
    name: str
    date_of_birth: date
    GPA: float = Field(ge=0, le=4)
    course: str | None 
    department: DepartmentEnum
    fees_paid: bool
    modules: list[Modules] = []    #here now we have referenced the above modules object as a list with a default val of empty list if modules are not present


    @field_validator('modules')
    def three_modules_or_not(cls, value):
        if len(value) and len(value)!=3:
            raise ValueError("List of modules should have length 3!")
        return value
    
    @field_validator('date_of_birth')
    def ensure_16_or_over(cls, value):  
        sixteen_years_ago = datetime.now() - timedelta(365*16)  
        sixteen_years_ago = sixteen_years_ago.date()
        if value > sixteen_years_ago:
            raise ValueError("To young")
        return value
    



url = 'https://raw.githubusercontent.com/bugbytes-io/datasets/master/students_v2.json'
response = requests.get(url) 
print(response.content) #this is a byte object 

data = response.json()


for student in data:
    student_module = Student4(**student)

    for module in student_module.modules:
        print(module.id)
