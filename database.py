from sqlalchemy import create_engine
# 导入sqlalchemy.ext.declarative模块中的declarative_base函数
from sqlalchemy.ext.declarative import declarative_base
# 导入sqlalchemy.orm模块中的sessionmaker函数
from sqlalchemy.orm import sessionmaker

# 定义一个SQLALCHEMY_DATABASE_URL变量，存储数据库连接字符串
SQLALCHEMY_DATABASE_URL = "mysql://root:123456@mysqlserver/db"

# 使用create_engine函数创建一个数据库引擎对象，并传入连接字符串和其他参数
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# 使用sessionmaker函数创建一个会话工厂对象，并传入自动提交、自动刷新和绑定引擎参数
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 使用declarative_base函数创建一个基类对象，用于定义映射类
Base = declarative_base()