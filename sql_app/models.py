from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base



class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    group_number = Column(String, index=True)  
    text = Column(String)  
    type = Column(String)
    time = Column
    content = Column(String)

    
