from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
# 导入sqlalchemy.orm模块中的relationship函数
from sqlalchemy.orm import relationship

# 从database模块中导入Base对象
from database import Base

# 定义一个User类，继承自Base类，并设置__tablename__属性为"users"
class User(Base):
    __tablename__ = "users"

    # 定义一个id属性，使用Column类创建，并设置主键和索引为True
    id = Column(Integer, primary_key=True, index=True)
    # 定义一个username属性，使用Column类创建，并设置唯一性和索引为True
    username = Column(String, unique=True, index=True)
    # 定义一个hashed_password属性，使用Column类创建
    hashed_password = Column(String)
    # 定义一个is_active属性，使用Column类创建，并设置默认值为True
    is_active = Column(Boolean, default=True)

    # 定义一个items属性，使用relationship函数创建，并指定关联的Item类和反向关联属性名为"owner"
    items = relationship("Item", back_populates="owner")

# 定义一个Item类，继承自Base类，并设置__tablename__属性为"items"
class Item(Base):
    __tablename__ = "items"

     # 同样定义id、groupname、grouptext、ddltext等属性，使用Column类创建，并设置索引为True
    id = Column(Integer, primary_key=True, index=True)
    groupname = Column(String, index=True)
    grouptext = Column(String, index=True)
    ddltext = Column(String, index=True)
     # 定义一个owner_id属性，使用Column类创建，并设置外键约束为"users.id"
    owner_id = Column(Integer, ForeignKey("users.id"))

     # 定义一个owner属性，使用relationship函数创建，并指定关联的User类和反向关联属性名为"items"
    owner = relationship("User", back_populates="items")