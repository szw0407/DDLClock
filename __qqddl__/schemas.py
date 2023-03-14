from datetime import date
from typing import List, Union

from pydantic import BaseModel


class ItemBase(BaseModel):
    text: str
    ddltime: Union[date, None] = None
    status: str


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class GroupBase(BaseModel):
    groupnumber: str


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
