from typing import List, Union
# 导入pydantic模块中的BaseModel类
from pydantic import BaseModel
# 导入sqlalchemy模块中的Column和String类
from sqlalchemy import Column
from sqlalchemy import String

# 定义一个ItemBase类，继承自BaseModel类
class ItemBase(BaseModel):
    # 定义一个title属性，类型为str
    title: str
    # 定义一个ddltext属性，类型为str或None，默认值为None
    ddltext: Union[str, None] = None

# 定义一个ItemCreate类，继承自ItemBase类
class ItemCreate(ItemBase):
    pass

# 定义一个Item类，继承自ItemBase类
class Item(ItemBase):
    # 定义一个id属性，类型为int
    id: int
    # 定义一个owner_id属性，类型为int
    owner_id: int
    # 定义一个groupname属性，使用sqlalchemy.Column类创建，并设置索引为True
    groupname = Column(String, index=True)
    # 定义一个grouptext属性，使用sqlalchemy.Column类创建，并设置索引为True
    grouptext = Column(String, index=True)
    # 定义一个ddltext属性，使用sqlalchemy.Column类创建，并设置索引为True
    ddltext = Column(String, index=True)

    # 定义一个Config内部类，用于配置pydantic模型行为 
    class Config:
        # 设置orm_mode属性为True，表示启用ORM模式（对象关系映射）
        orm_mode = True

# 定义一个UserBase类，继承自BaseModel类        
class UserBase(BaseModel):
    # 定义一个username属性，类型为str    
    username: str

# 定义一个UserCreate类，继承自UserBase类    
class UserCreate(UserBase):
     # 定义一个password属性，类型为str   
     password: str

# 定义一个User类，继承自UserBase类     
class User(UserBase):
     # 定义一个id属性，类型为int   
     id: int 
     # 定义一个is_active属性，类型为bool   
     is_active: bool 
     # 定义一个items属性，默认值为空列表[]  
     items: List[Item] = []

     # 同样定义Config内部类进行配置  
     class Config:
         orm_mode = True