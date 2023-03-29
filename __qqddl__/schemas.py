from datetime import date
from typing import List, Union

from pydantic import BaseModel


class DDLBase(BaseModel):
    description: str
    text:str
    ddltime: Union[str, None] = None
    status: str
    group_num: str = "0"


class ItemCreate(DDLBase):
    pass


class Item(DDLBase):
    id: int
    # owner_id: int
    def getGN(self,gn):
        self.group_num=gn

    class Config:
        orm_mode = True

class LeastGroupModify(BaseModel):
    group_number:str

class GroupModify(LeastGroupModify):
    group_ren:Union[str,None] = None
    is_active:Union[bool,None] = None
    def activate(self,s:bool):
        self.is_active=s

class GroupBase(GroupModify):
    group_name:str    
    


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: int

    class Config:
        orm_mode = True
