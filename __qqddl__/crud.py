from sqlalchemy.orm import Session
from sqlalchemy import update
from . import models, schemas


def get_group(db: Session, group_id: int):
    return db.query(models.Group).filter(models.Group.id == group_id).first()


# 通过id查询群聊

def get_group_by_groupnumber(db: Session, get_groupnumber: str):
    return db.query(models.Group).filter(models.Group.group_number == get_groupnumber).all()


# 通过号码查找群聊

def get_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Group).offset(skip).limit(limit).all()


# 查询所有群聊

def create_group(db: Session, group: schemas.GroupCreate):
    db_group = models.Group(group_number=group.group_number,group_name=group.group_name,group_ren=group.group_ren,is_active=group.is_active)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


# 创建群

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DDLs).offset(skip).limit(limit).all()


# 获取所有消息

def create_group_item(db: Session, item: schemas.ItemCreate):
    db_item = models.DDLs(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def modify_group(db:Session, group:schemas.GroupCreate):
    query = update(models.Group).where(models.Group.group_number == group.group_number).values(**group.dict())
    db.execute(query)
    db.commit()
    return query
# 创建消息

def delete(db: Session):
    db_groups = models.Group
    db.delete(db_groups)
    db.commit()
    return {"msg": "所有群聊已经删除"}

# def log_Msg(db:Session,msg=schemas.)