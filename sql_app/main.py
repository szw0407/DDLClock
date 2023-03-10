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


# 读取所有数据
@app.get("/items/all", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


# 读取群号下的所有数据
@app.get("/items/{group_id}", response_model=[schemas.Item])
def read_items_by_groupid(group_id: int, db: Session = Depends(get_db)):
    db_items = crud.get_items_by_groupnumber(db, group_id)
    if db_items is None:
        raise HTTPException(status_code=404, detail="Items not found")
    return db_items

# 通过id读取数据
@app.get("/items/{id}", response_model=schemas.Item)
def read_item(id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_id(db, id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


# 通过id删除数据
@app.delete('/item/{item_id}', response_model=List[schemas.Item])
def delete(item_id: int, db: Session = Depends(get_db)):
    db.query(models.Item).filter(models.Item.id == item_id).delete(
        synchronize_session=False)
    db.commit()
    return {"msg": "该记录已经删除"}

# 通过id更新数据
@app.put('/item/{item_id}')
def update(item_id: int, blog: schemas.Item, db: Session = Depends(get_db)):
    db.query(models.Item).filter(models.Item.id == item_id).update(blog.dict())
    db.commit()
    return {"msg": "数据成功更新！"}

# 删除所有数据
@app.delete('/item/all', response_model=List[schemas.Item])
def delete(db: Session = Depends(get_db)):
    db.query(models.Item).delete(
        synchronize_session=False)
    db.commit()
    return {"msg": "所有记录已经删除"}



if __name__ == '__main__:':
    uvicorn.run("main:app", reload=True)