from typing import List, Union
from pydantic import BaseModel
from sqlalchemy import Column
from sqlalchemy import String


class ItemBase(BaseModel):
    title: str
    ddltext: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int
    groupname = Column(String, index=True)
    grouptext = Column(String, index=True)
    ddltext = Column(String, index=True)

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
