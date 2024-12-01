from pydantic import BaseModel, Field, field_validator
import uuid
from datetime import date, datetime, timedelta
from enums import DepartmentEnum
from typing import Literal

"""
field function in pydantic provides us multiple arguments:

1. default: this param in field, helps to provide a default value to the field writtnt in the pydantic module
2. default_factory: this param just like the default param, instead of giving a static val in dedault provides the ability to give dynamic value as a default val
3. alias: this is used for mapping the pydantic model fields to the fileds of the source data 
4. max_length: the max num of items that can be passed in that field 

data exports args in field function, these are helpful when we are exporting the model data into dict or json format

1. include: this when given to a field tells that only this field should be included when we export the data to any format
2. exclude: this when given to a field tells that only this field needs to be excluded when we export the data  


In the below code i have used all the above mentioned fields
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
    student_name: str = Field(alias="name")  #used alias to map the student_name from pydantic model to the name field of the source code
    date_of_birth: date = Field(default_factory=lambda: datetime.today().date())     #this is how we can use defaultfactory no whenevever there is no val for this field it will assign a dynamic that day val to it 
    GPA: float = Field(ge=0, le=4)
    course: str | None 
    department: DepartmentEnum
    fees_paid: bool = Field(exclude=True) #now this will exclude this field from the model whenever it is dumped to dict or json 
    modules: list[Modules] = Field(default=[], max_length=10)   #used the default and max_length here

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
    

# or we can exclude or include the fields during export also 

data = "so,e json data"
student = data[0]

model = Student(**student)

model.model_dump(exclude={'id', 'fees_paid'})  #it takes a set of all the field to be excluded


#in order to exclude some fields from a  list of sub models present in the model we can do the following 

model = Student(**student)

model.model_dump(exclude={
    "id": True,    #this is simple as it is present directly in the model 
    "modules": {"__all__": {'registration_code'}}  
    #now here what we wanted is to exclude the registration_code from all the model present in the list 
    #for that we used the modules field which consist of the list of all the submodels
    #we set the key as __all__ to exclude the item from all the submodels
    #then in the value we passed a set with the name of all the fields to be excluded from the sub model
})
