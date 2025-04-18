#from __future__ import unicode_literals, absolute_import
from Models.Base import Base
from sqlalchemy import Column, Integer, String, DateTime, MetaData, BLOB, LargeBinary
from Common.Uuid import *
from Common.DataUtil import *
import datetime

class DataParameter(Base):
    __tablename__ = "dataparameter"

    dataparameterid = Column(String(32), primary_key=True, unique=True, default=Uuid.get_hex)
    name = Column(String(length=255))
    desc = Column(String(length=100))
    type = Column(Integer()) # 1 字符串 2 数字 3 文件
    nature = Column(Integer())# 1 基础参数 2 运行参数
    value = Column(String(length=255))
    datadriver_id = Column(String(length=32))
    new_template_param_id = Column(String(length=32))
    createdon = Column(DateTime, default=datetime.datetime.now)
    modifiedon = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

if __name__ == "__main__":
    du = DataUtil()
    Base.metadata.create_all(du.engine)