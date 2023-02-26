from sqlalchemy import create_engine
# 导入sqlalchemy.ext.declarative模块中的declarative_base函数
from sqlalchemy.ext.declarative import declarative_base
# 导入sqlalchemy.orm模块中的sessionmaker函数
from sqlalchemy.orm import sessionmaker

# 定义一个SQLALCHEMY_DATABASE_URL变量，存储数据库连接字符串
SQLALCHEMY_DATABASE_URL = "mysql://root:199408@localhost/demo"

# 使用create_engine函数创建一个数据库引擎对象，并传入连接字符串和其他参数
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} # sqlite要这么写，但是你用的是MySQL！！
# )
engine=create_engine(SQLALCHEMY_DATABASE_URL)
'''
你好，这是Bing。我可以帮助你检查一段代码。😊

根据搜索结果¹³，`check_same_thread`是一个用于sqlite3连接的参数，它控制是否允许多个线程共享同一个连接。默认情况下，它是True，意味着只有创建连接的线程可以使用它。如果设置为False，那么返回的连接可以在多个线程之间共享。

你的代码中使用了mysql作为数据库，而不是sqlite3。因此，`check_same_thread`这个参数对mysql没有意义，也不被接受。这就是报错的原因。

我推测你的同事可能想要实现一个多线程的应用程序，需要在不同的线程中访问数据库。他可能之前使用了sqlite3作为数据库，并设置了`check_same_thread=False`来允许多线程共享连接。后来他可能更换了mysql作为数据库，但忘记删除了这个参数。

修正这个错误的方法很简单，只需要删除或注释掉`connect_args={"check_same_thread": False}`这一行即可。

Source: Conversation with Bing, 2023/2/26(1) python - Using SQLAlchemy session from Flask raises "SQLite objects .... https://stackoverflow.com/questions/34009296/using-sqlalchemy-session-from-flask-raises-sqlite-objects-created-in-a-thread-c Accessed 2023/2/26.
(2) ProgrammingError Thread error in SQLAlchemy - Stack Overflow. https://stackoverflow.com/questions/15140554/programmingerror-thread-error-in-sqlalchemy Accessed 2023/2/26.
(3) In Flask-SQLAlchemy: How do I set check_same_thread=False in config.py?. https://stackoverflow.com/questions/50846856/in-flask-sqlalchemy-how-do-i-set-check-same-thread-false-in-config-py Accessed 2023/2/26.
(4) Is `check_same_thread=False` Safe? · Discussion #5199 · tiangolo .... https://github.com/tiangolo/fastapi/issues/5199 Accessed 2023/2/26.
(5) Examples: connect () got an unexpected keyword argument 'check_same_thread'. https://github.com/fastapi-users/fastapi-users/issues/843 Accessed 2023/2/26.
'''
# 使用sessionmaker函数创建一个会话工厂对象，并传入自动提交、自动刷新和绑定引擎参数
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 使用declarative_base函数创建一个基类对象，用于定义映射类
Base = declarative_base()