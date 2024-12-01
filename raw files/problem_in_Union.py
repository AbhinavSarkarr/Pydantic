"""It's very important to know the following,
#however - when Pydantic encounters a union as a type, it will attempt to cast data in the order defined in the union. """

#Imagine we defined a union as follows:
from pydantic import BaseModel


class Number(BaseModel):
    value: int | float

number = Number({'value': 2.2}) 
print(number)  # number = 2

"""
Even though the value passed is a floating point number, 2.2.
The Pydantic model has first attempted to convert this number to an integer(as it was defined first in the union), therefore the value is now equal to 2.
This is likely undesirable behaviour. Be careful with the order of union types 
"""