from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud
import models
import schemas
from database import SessionLocal, engine


# 创建数据库表格（如果不存在）——此处有报错！！
models.Base.metadata.create_all(bind=engine) # 为什么要这样import？不理解，直接用base不就好了（恼）

# 创建FastAPI应用对象
app = FastAPI()

# 定义一个依赖函数，用于获取数据库会话对象
def get_db():
    db = SessionLocal()
    try:
        yield db # 返回db对象给调用者，并保持连接开启状态，直到调用者执行完毕
    finally:
        db.close() # 关闭数据库连接

# 定义一个路由函数，用于创建用户，并返回用户信息（使用POST方法）
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 从数据库中查询是否已经存在同名的用户
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        # 如果存在，则抛出HTTP异常，状态码为400，提示用户名已注册
        raise HTTPException(status_code=400, detail="Username already registered")
    # 如果不存在，则调用crud模块中的函数创建用户，并返回用户信息
    return crud.create_user(db=db, user=user)

# 定义一个路由函数，用于读取用户列表，并返回用户信息（使用GET方法）
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # 调用crud模块中的函数获取用户列表，可以指定跳过和限制的数量，默认为0和100
    users = crud.get_users(db, skip=skip, limit=limit)
    # 返回用户列表信息
    return users

# 定义一个路由函数，用于读取指定id的用户，并返回用户信息（使用GET方法）
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    # 调用crud模块中的函数获取指定id的用户信息
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        # 如果不存在，则抛出HTTP异常，状态码为404，提示用户未找到
        raise HTTPException(status_code=404, detail="User not found")
    # 如果存在，则返回用户信息 
    return db_user

# 定义一个路由函数，用于为指定id的用户创建项目，并返回项目信息（使用POST方法）
@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
        user_id: int,
        item: schemas.ItemCreate,
        db: Session = Depends(get_db),
):
   return crud.create_user_item(db=db,item=item,user_id=user_id)

# 定义一个路由函数，用于读取项目列表，并返回项目信息（使用GET方法）
@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip:int=0 ,limit:int=100 ,db :Session=Depends(get_db)):
   items=crud.get_items(db ,skip=skip ,limit=limit )
   return items 