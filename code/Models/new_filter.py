#from __future__ import unicode_literals, absolute_import
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, MetaData
from Common.Uuid import *
from Common.DataUtil import *
import datetime

Base = declarative_base()

class new_filter(Base):
    __tablename__ = "new_filter"

    new_filterid = Column(String(32), primary_key=True, unique=True, default=Uuid.get_hex)
    new_name = Column(String(length=255))
    new_memo = Column(String(length=1000))
    new_func = Column(String(length=5000))
    statecode = Column(Integer())
    new_createdon = Column(DateTime, default=datetime.datetime.now)
    new_modifiedon = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

if __name__ == "__main__":
    du = DataUtil()
    Base.metadata.create_all(du.engine)