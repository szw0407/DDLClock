from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import Engine
from sqlalchemy.orm import Session
import uvicorn

from database import SessionLocal
from . import crud, models, schemas



models.Base.metadata.create_all(bind=Engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 创建依赖项

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_qqnumber(db, qqnumber=user.qqnumber)
    if db_user:
        raise HTTPException(status_code=400, detail="QQ already registered")
    return crud.create_user(db=db, user=user)


# 创建用户
@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
        user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


# 为用户创建群聊项目
@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


# 读取所有用户

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# 读取用户

@app.get("/users/get_users_by_qqnumber", response_model=schemas.User)
def read_user_by_qqnumber(qqnumber: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_qqnumber(db, qqnumber=qqnumber)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# 通过QQ号码读取用户


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


# 读取全部群聊

@app.delete('/item/{item_id}', response_model=List[schemas.Item])
def delete(item_id: int, db: Session = Depends(get_db)):
    db.query(models.Item).filter(models.Item.id == item_id).delete(
        synchronize_session=False)
    db.commit()
    return {"msg": "该群聊已经删除"}


# 删除群聊项目
@app.put('/item/{item_id}')
def update(item_id: int, blog: schemas.Item, db: Session = Depends(get_db)):
    db.query(models.Item).filter(models.Item.id == item_id).update(blog.dict())
    db.commit()
    return {"msg": "数据成功更新！"}


# 更新群聊
@app.delete('/user/{user_id}', response_model=List[schemas.User])
def delete(user_id: int, db: Session = Depends(get_db)):
    db.query(models.User).filter(models.User.id == user_id).delete(synchronize_session=False)
    db.commit()
    return {"msg": "该用户已经删除"}


# 删除用户


@app.delete('/item/all', response_model=List[schemas.Item])
def delete(db: Session = Depends(get_db)):
    db.query(models.Item).delete(
        synchronize_session=False)
    db.commit()
    return {"msg": "所有群聊已经删除"}


# 清除所有群聊

@app.delete('/user/all', response_model=List[schemas.User])
def delete(db: Session = Depends(get_db)):
    db.query(models.User).delete(synchronize_session=False)
    db.query(models.Item).delete(synchronize_session=False)
    db.commit()
    return {"msg": "所有用户已经删除,所有群聊已经删除"}

if __name__ == '__main__:':
    uvicorn.run("main:app", reload=True)