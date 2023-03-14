from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from .database import Base


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    groupnumber = Column(String(15), unique=True, index=True)  # 群号
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)  # 群聊消息
    ddltime = Column(Date)  # ddl时间
    status = Column(String)  # 紧急情况
    owner_id = Column(Integer, ForeignKey("groups.id"))

    owner = relationship("Group", back_populates="items")
