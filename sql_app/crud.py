from sqlalchemy.orm import Session

from . import models, schemas


def get_item_by_id(db:Session,id:int):
    return db.query(models.Item).filter(models.Item.id == id).first()

def get_items_by_groupnumber(db:Session,gr:int):
    return db.query(models.Item).filter(models.Item.group_number == gr).all()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def creat_items(db:Session,item:schemas.Item):
    db_item = models.Item(group_number = item.group_number,text = item.text,time=item.time,type=item.type,content=item.content)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
