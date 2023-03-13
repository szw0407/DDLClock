from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 创建依赖项

@app.post("/groups/", response_model=schemas.Group)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    db_group = crud.get_group_by_groupnumber(db, get_groupnumber=group.groupnumber)
    if db_group:
        raise HTTPException(status_code=400, detail="QQ already registered")
    return crud.create_group(db=db, group=group)


# 创建用户
@app.post("/groups/{group_id}/items/", response_model=schemas.Item)
def create_item_for_group(
        group_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_group_item(db=db, item=item, group_id=group_id)


# 为用户创建群聊项目


@app.get("/groups/", response_model=List[schemas.Group])
def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    groups = crud.get_groups(db, skip=skip, limit=limit)
    return groups


# 读取所有用户

@app.get("/groups/get_groups_by_groupnumber", response_model=List[schemas.Group])
def read_group_by_groupnumber(groupnumber: str, db: Session = Depends(get_db)):
    db_group = crud.get_group_by_groupnumber(db, get_groupnumber=groupnumber)
    if db_group is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_group


# 通过群号码读取群聊消息

@app.get("/groups/{group_id}", response_model=schemas.Group)
def read_group(group_id: int, db: Session = Depends(get_db)):
    db_group = crud.get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group


# 读取用户


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


# 读取全部群聊

@app.delete('/item/{item_id}', response_model=List[schemas.Item])
def delete(item_id: int, db: Session = Depends(get_db)):
    db.query(models.Item).filter(models.Item.id == item_id).delete(synchronize_session=False)
    db.commit()
    return {"msg": "该群聊已经删除"}


# 删除群聊项目
@app.put('/item/{item_id}')
def update(item_id: int, blog: schemas.Item, db: Session = Depends(get_db)):
    db.query(models.Item).filter(models.Item.id == item_id).update(blog.dict())
    db.commit()
    return {"msg": "数据成功更新！"}


# 更新群聊
@app.delete('/group/{group_id}', response_model=List[schemas.Group])
def delete(group_id: int, db: Session = Depends(get_db)):
    db.query(models.Group).filter(models.Group.id == group_id).delete(synchronize_session=False)
    db.commit()
    return {"msg": "该用户已经删除"}


# 删除用户

@app.delete('/groups and items', response_model=List[schemas.Group])
def delete(db: Session = Depends(get_db)):
    db.query(models.Item).delete(synchronize_session=False)
    db.query(models.Group).delete(synchronize_session=False)
    db.commit()
    return {"msg": "所有群聊已经删除"}
# 删除所有
