from pydantic import BaseModel, coint, Field

"""
For each Python primitive, pydantic has a constrained variant. For example, for the int type, there's a conint type available in pydantic. We also have confloat, constr, conlist, etc.
Each of these constrained types have some arguments that can define the constraints. We can do things such as enforce upper- or lower-case (strings), enforce lower/upper bounds on the number of items in a list/set/frozenset, and enforce lower/upper bounds on the values of numbers (ints, floats, Decimals).
"""


class User(BaseModel):
    name: str
    age: coint(gt=1, lt=130)

#The same effect can be achieved using Pydantic's Field function, too.

class User2(BaseModel):
    name: str
    age: int = Field(gt=0, lt=130)

#The Field() function is useful for specifying additional information and validation/constraints on fields.


"Let's implement this in the basics.py"