from pydantic import BaseModel, Field, field_validator
import uuid
from datetime import date, datetime, timedelta
from _enum import DepartmentEnum
import requests

class Modules(BaseModel):
    id: uuid.UUID | int
    name: str
    professor: str
    credits: int
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
