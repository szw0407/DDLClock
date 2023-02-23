from sqlalchemy.orm import Session

# 从models模块中导入User和Item类
import models

# 从schemas模块中导入UserCreate和ItemCreate类
import schemas


# 定义一个get_user函数，接受一个会话对象和一个用户id作为参数
def get_user(db: Session, user_id: int):
    # 使用会话对象的query方法查询User表，并使用filter方法过滤出id等于user_id的记录，然后使用first方法返回第一条结果
    return db.query(models.User).filter(models.User.id == user_id).first()


# 定义一个get_user_by_username函数，接受一个会话对象和一个用户名作为参数
def get_user_by_username(db: Session, username: str):
    # 使用会话对象的query方法查询User表，并使用filter方法过滤出username等于username的记录，然后使用first方法返回第一条结果
    return db.query(models.User).filter(models.User.username == username).first()


# 定义一个get_users函数，接受一个会话对象和两个可选参数skip和limit作为参数，默认值分别为0和100
def get_users(db: Session, skip: int = 0, limit: int = 100):
    # 使用会话对象的query方法查询User表，并使用offset方法跳过skip条记录，然后使用limit方法限制返回limit条记录，最后使用all方法返回所有结果
    return db.query(models.User).offset(skip).limit(limit).all()


# 获取用户名单


# 定义一个create_user函数，接受一个会话对象和一个UserCreate对象作为参数
def create_user(db: Session, user: schemas.UserCreate):
    # 创建一个假密码哈希值，将用户密码加上"notreallyhashed"字符串
    fake_hashed_password = user.password + "notreallyhashed"
    # 创建一个User对象，并设置username属性为用户输入的用户名，hashed_password属性为假密码哈希值
    db_user = models.User(username=user.username, hashed_password=fake_hashed_password)
    # 使用会话对象的add方法添加User对象到数据库中
    db.add(db_user)
    # 使用会话对象的commit方法提交事务到数据库中
    db.commit()
    # 使用会话对象的refresh方法刷新User对象以获取最新数据（如自动生成的id）
    db.refresh(db_user)
    # 返回创建好的User对象
    return db_user


# 定义一个get_items函数，接受一个会话对象和两个可选参数skip和limit作为参数，默认值分别为0和100
def get_items(db: Session, skip: int = 0, limit: int = 100):
    # 使用会话对象的query方法查询Item表，并使用offset方法跳过skip条记录，然后使用limit方法限制返回limit条记录，最后使用all方法返回所有结果
    return db.query(models.Item).offset(skip).limit(limit).all()


# 获取表单


# 定义一个create_user_item函数，接受一个会话对象、一个ItemCreate对象、以及用户id作为参数
def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    # 创建一个Item 对象，并将item.dict()解包并传入构造器中，并设置owner_id属性为用户id
    db_item = models.Item(**item.dict(), owner_id=user_id)
    # 使用会话对像add 方法添加Item 对象到数据库中
    db.add(db_item)
    db.commit()
    # 使用会话对象的refresh方法刷新Item对象以获取最新数据（如自动生成的id）
    db.refresh(db_item)
    # 返回创建好的Item对象
    return db_item


# 创建并提交表格
