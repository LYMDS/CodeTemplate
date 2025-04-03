#from __future__ import unicode_literals, absolute_import
from Models.Base import Base
from sqlalchemy import Column, Integer, String, DateTime, MetaData, BLOB, LargeBinary, event
from Common.Uuid import *
from Common.DataUtil import *
import datetime

class DataDriver(Base):
    __tablename__ = "datadriver"

    datadriverid = Column(String(32), primary_key=True, unique=True, default=Uuid.get_hex)
    name = Column(String(length=255))
    desc = Column(String(length=100))
    type = Column(String(length=100))
    createdon = Column(DateTime, default=datetime.datetime.now)
    modifiedon = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

if __name__ == "__main__":
    du = DataUtil()
    Base.metadata.create_all(du.engine)