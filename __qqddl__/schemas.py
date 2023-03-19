from datetime import date
from typing import List, Union

from pydantic import BaseModel


class DDLBase(BaseModel):
    description: str
    text:str
    ddltime: Union[date, None] = None
    status: str
    owner_id:int


class ItemCreate(DDLBase):
    pass


class Item(DDLBase):
    id: int
    # owner_id: int

    class Config:
        orm_mode = True


class GroupBase(BaseModel):
    group_number: str
    group_name:str
    group_ren:str
    is_active:bool = False


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: int
    items: List[Item] = []

    class Config:
        orm_mode = True
