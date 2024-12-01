from pydantic import BaseModel, Field, field_validator, model_validator
import uuid
from datetime import date, datetime, timedelta
from enums import DepartmentEnum
from typing import Literal

"""
The field_validator function in pydantic takes provides three values and three args:
    1. class (cls): the class on which the validator is applied
    2. value(value): the value of the field on which the validator is applied
    3. values(values): the values of the all fields that are validated this field on which the vcalidator is applied

The pydantic model works in a top to bottom manner, i.e. it validates all the fields one by one.
So inorder to create validtors which depends on other fields, we can't always maintain this order, so here we use root_validators, which validates the provided validation after full execution 
Below are the implemntations:
"""


class Modules(BaseModel):
    id: int | uuid.UUID
    name: str
    professor: str
    credits: Literal[10, 20]
    registration_code: str

class Student(BaseModel):
    """this performs data validation and conversion on the basis of datatypes of the BaseModel subclass"""
    id: uuid.UUID
    student_name: str = Field(alias="name")  
    GPA: float = Field(ge=0, le=4)
    course: str | None 
    department: DepartmentEnum
    modules: list[Modules] = Field(default=[], max_length=10)

    class Config:
        title = "Student Model"  
        use_enum_values = True    
        extra = "ignore"

    @model_validator    #this will be used once all the provided fields are validated 
    def check_gpa_for_science(cls, values):    #values is the dict of all the fields after vaildation 
        dept = values.get('department')
        gpa = values.get('GPA')
        dept_science = (dept == DepartmentEnum.SCIENCE_AND_ENGINEERING.value)
        gpa_science = gpa>=4.0
        
        if dept_science:
            if not gpa_science:
                raise ValueError("Not eligible for science")
        return values
    
    @field_validator('GPA')
    def validate_gpa(cls, value, values):
        print(values)  #here you will find the values of all the abovw validated fields  
        return value

    @field_validator('modules')
    def three_modules_or_not(cls, value):
        if len(value) and len(value)<3:
            raise ValueError("Length of modules should be 3!")
        return value

    @field_validator('date_of_birth')
    def ensure_16_or_over(cls, value):  
        sixteen_years_ago = datetime.now() - timedelta(365*16)  
        sixteen_years_ago = sixteen_years_ago.date()
        if value > sixteen_years_ago:
            raise ValueError("To young")
        return value