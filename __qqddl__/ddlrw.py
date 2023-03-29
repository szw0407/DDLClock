from typing import List
from sqlalchemy.orm import Session
from typing import Union
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 创建依赖项

# @app.post("/groups/", response_model=schemas.Group)
def create_group(group: Union[schemas.GroupCreate,schemas.Group,schemas.GroupModify], db: Session = next(get_db())):
    k=crud.get_group_by_groupnumber(db, get_groupnumber=group.group_number)
    if k !=[]:
        if group.group_ren is not None and group.is_active is None:
            group.activate(k[0].is_active)
        if group.is_active is not None:            
            group_upd=schemas.Group(id=k[0].id,group_ren=group.group_ren if group.group_ren is not None else "",group_number=group.group_number,group_name=k[0].group_name,is_active=group.is_active)
            crud.modify_group(db=db,group=group_upd)
            return crud.modify_group(db=db,group=group_upd)
    elif group is not schemas.GroupCreate:
        return {"Err":"None of the groups match the number"}
    else:
        group.activate(False)
        return crud.create_group(db=db, group=group)


# @app.post("/groups/{group_id}/items/", response_model=schemas.Item)
def create_item_for_group(
        item: schemas.ItemCreate, db: Session = next(get_db())
):
    return crud.create_group_item(db=db, item=item)

# @app.get("/groups/", response_model=List[schemas.Group])
def read_groups(skip: int = 0, limit: int = 100, db: Session = next(get_db())):
    return crud.get_groups(db, skip=skip, limit=limit)


# @app.get("/groups/get_groups_by_groupnumber", response_model=List[schemas.Group])
def read_group_by_groupnumber(groupnumber: str, db: Session = next(get_db())):
    db_group = crud.get_group_by_groupnumber(db, get_groupnumber=groupnumber)
    return None if db_group is None else db_group

# @app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 1000000, db: Session = next(get_db())):
    return crud.get_items(db, skip=skip, limit=limit)
def read_item(id:int,db:Session=next(get_db())):
    return crud.get_item(db=db,id=id)
# @app.delete('/item/{item_id}', response_model=List[schemas.Item])
def delete_group(id: int, db: Session = next(get_db())):
    db.query(models.Group).filter(models.Group.id == id).delete(synchronize_session=False)
    db.commit()
    return {}
def delete_ddl(id:int, db:Session = next(get_db())):
    db.query(models.DDLs).filter(models.DDLs.id ==id).delete(synchronize_session=False)
    db.commit()
    return {}
# @app.put('/item/{item_id}')
def update_ddl(id: int, blog: schemas.Item, db: Session = next(get_db())):
    db.query(models.DDLs).filter(models.DDLs.id == id).update(blog.dict())
    db.commit()
    return {}

# @app.delete('/group/{group_id}', response_model=List[schemas.Group])
def delete_group(num: int, db: Session = next(get_db())):
    db.query(models.Group).filter(models.Group.group_number == num).delete(synchronize_session=False)
    db.commit()
    return {"msg": "该群已经删除"}

def delete_ddl(id:int, db : Session=next(get_db())):
    db.query(models.DDLs).filter(models.DDLs.id==id).delete(synchronize_session=False)
    db.commit()
    return {}

# @app.delete('/groups and items', response_model=List[schemas.Group])
def delete(db: Session = next(get_db())):
    db.query(models.DDLs).delete(synchronize_session=False)
    db.query(models.Group).delete(synchronize_session=False)
    db.commit()
    return {"msg": "所有群聊已经删除"}

