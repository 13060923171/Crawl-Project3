from sqlalchemy import create_engine
from sqlalchemy import Column,String,Text,Integer,DATETIME
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine(
    "mysql+pymysql://root:root@127.0.0.1:3306/demo?charset=utf8",
    # 超过连接池大小外最多可以创建的链接
    max_overflow=10,
    # 连接池的大小
    pool_size=100,
    # 调试信息展示
    echo=True,
)
class COMMODITY(Base):
    #数据库的表的名字
    __tablename__ ='video'
    id = Column("id",Integer(),primary_key=True,autoincrement=True)
    #设置数据库，存储这些内容的格式，长度等
    comment= Column('comment',Text())
    play_time = Column('play_time',DATETIME())
    level = Column('level',Integer())
    type1 = Column('type',String(10))

# Base.metadata.create_all(engine)
session = sessionmaker(engine)
sess = session()