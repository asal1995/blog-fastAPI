from typing import Optional, Union, List, Dict
from pydantic import BaseModel


# class OurBaseModel(BaseModel):


class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str
    email: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True


class UpdateUser(BaseModel):

    username: Union[str, None]
    first_name: Union[str, None]
    last_name: Union[str, None]
    email: Union[str, None]
