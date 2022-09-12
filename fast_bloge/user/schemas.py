from typing import Optional, Union, List, Dict
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str
    email: str
