from typing import List, Union

from pydantic import BaseModel



class Item(BaseModel):
    id: int
    group_number: int
    text: str
    type: str
    time: List|dict
    content: str

    class Config:
        orm_mode = True


