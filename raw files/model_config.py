from pydantic import BaseModel, Field, field_validator
import uuid
from datetime import date, datetime, timedelta
from enums import DepartmentEnum
from typing import Literal

"""
there are settings that can be applied across the entire Pydantic model. These can be defined in a special inner-class within the model, called Config.
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
        title = "Student Model"  #this will define a title in the json schema 
        use_enum_values = True    #now this will treat all the values which are provided as a enum obj as a row of string 
        extra = "ignore"
        """
        The extra field can take on three values:

            ignore - do nothing when encountering extra attributes.
            allow - assign the extra attributes to the model
            forbid - cause validation to fail with a ValidationError if extra attributes are passed to the model
        """

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