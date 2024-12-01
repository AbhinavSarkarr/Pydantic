import requests 
from pydantic import BaseModel, Field, field_validator
import uuid
from datetime import date, datetime, timedelta



#Validator Functions: Used to validate the given fields 
class Student2(BaseModel):
    """this performs data validation and conversion on the basis of datatypes of the BaseModel subclass"""
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

        #now in sixteen years ago we got the year that a person should be in atleast to be greater than 16 years 
        #now if the value i.e the date entered by the user is greater than the lowest value we got, means that the person is less than 16 years old 
        if value > sixteen_years_ago:
            raise ValueError("To young")
        return value


#The source dataset does not have any dates of birth that would fail this validation, but you can add one after fetching the data, as below:

url = 'https://raw.githubusercontent.com/bugbytes-io/datasets/master/students_v1.json'
data = requests.get(url).json()
data.append(
    {
        "id": "48dda775-785d-41e3-b0dd-26a4a2f7722f",
        "name": "Justin Holden",
        "date_of_birth": "2010-08-22",
        "GPA": "3.23",
        "course": "Philosophy",
        "department": "Arts and Humanities",
        "fees_paid": 'true'
    }
)


for student in data:
    data = Student2(**student)
    print(data)


"""
Error Raised:
Traceback (most recent call last):
  File "/home/jellyfish/Videos/Pydantic/validator_functions.py", line 51, in <module>
    data = Student2(**student)
  File "/home/jellyfish/Videos/Pydantic/pydantic/lib/python3.10/site-packages/pydantic/main.py", line 214, in __init__
    validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)
pydantic_core._pydantic_core.ValidationError: 1 validation error for Student2
date_of_birth
  Value error, To young [type=value_error, input_value='2010-08-22', input_type=str]
    For further information visit https://errors.pydantic.dev/2.10/v/value_error
"""