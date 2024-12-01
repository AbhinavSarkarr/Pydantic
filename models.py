from pydantic import BaseModel, Field, field_validator, model_validator
import uuid
from datetime import datetime, timedelta, date
from enums import DepartmentEnum
from typing import Literal

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
    date_of_birth: date = Field(default_factory=lambda: datetime.today().date())     
    GPA: float = Field(ge=0, le=4)
    course: str | None 
    department: DepartmentEnum
    fees_paid: bool = Field(exclude=True) 
    modules: list[Modules] = Field(default=[], max_length=10)
    tags: list[str]

    class Config:
        title = "Student Model"  
        use_enum_values = True    
        str_strip_whitespace = True
        extra = "ignore"

    @model_validator(mode="after")    
    def check_gpa_for_science(cls, values):    
        dept = values.department
        gpa = values.GPA
        dept_science = (dept == DepartmentEnum.SCIENCE_AND_ENGINEERING.value)
        gpa_science = gpa>=4.0
        
        if dept_science:
            if not gpa_science:
                raise ValueError("Not eligible for science")
        return values
    
    @field_validator('tags', mode="before")
    def tags_to_list(cls, value):
        return value.split(",")

    @field_validator('tags')
    def if_slacker(cls, value):
        if value == 'slacker':
            raise ValueError("Slackers not allowed")

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