"""
#Validator Functions: Used to validate the given fields 
class Student2(BaseModel):
    "this performs data validation and conversion on the basis of datatypes of the BaseModel subclass"
    id: uuid.UUID
    name: str
    date_of_birth: date
    GPA: float = Field(ge=0, le=4)
    #or GPA: confloat(ge=0, le=4)
    course: str | None 
    department: str
    fees_paid: bool

    @field_validator('date_of_birth')
    def ensure_16_or_over(cls, value):  #cls is the class and value is the value of the field given in the field_validator
        sixteen_years_ago = datetime.now() - timedelta(365*16)  #this is a datetime object 
        #convert datetime to date 
        sixteen_years_ago = sixteen_years_ago.date()
        if value > sixteen_years_ago:
            raise ValueError("To young")
        return value
    """

#Till now in this code we can see that the department is taking any value which is a string 
# But we don't want so as there are a number of departments only, we want the Student class to take input out of only those few departments

#For this we use Enum (We can also use literal)

from enum import Enum
from pydantic import BaseModel, field_validator, confloat
import uuid
from datetime import date, datetime, timedelta

#We're going to assume the college/university has a small set of three departments - Science and Engineering, Arts and Humanities, and Life Sciences.
class DepartmentEnum(Enum):
    ARTS_AND_HUMANITIES = 'Arts and Humanities'
    LIFE_SCIENCES = 'Life Sciences'
    SCIENCE_AND_ENGINEERING = 'Science and Engineering'


class Student(BaseModel):
    id: uuid.UUID
    name: str
    date_of_birth: date
    GPA: confloat(ge=0, le=4)
    course: str | None
    #this will now convert the json key value of department to a DepartmentEnum Class Object
    department: DepartmentEnum     #here you can see that now couse will take only those value as an input which are present in the Department Enum 
    fees_paid: bool

    @field_validator('date_of_birth')
    def ensure_16_or_over(cls, value):
        sixteen_years_ago = datetime.now() - timedelta(days=365*16)

        # convert datetime object -> date
        sixteen_years_ago = sixteen_years_ago.date()
        
        # raise error if DOB is more recent than 16 years past.
        if value > sixteen_years_ago:
            raise ValueError("Too young to enrol, sorry!")
        return value