#from __future__ import unicode_literals, absolute_import
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, MetaData, BLOB, LargeBinary
from Common.Uuid import *
from Common.DataUtil import *
import datetime

Base = declarative_base()

class new_attachment(Base):
    __tablename__ = "new_attachment"

    new_attachmentid = Column(String(32), primary_key=True, unique=True, default=Uuid.get_hex)
    new_name = Column(String(length=255))
    new_content = Column(LargeBinary)
    new_createdon = Column(DateTime, default=datetime.datetime.now)
    new_modifiedon = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

if __name__ == "__main__":
    du = DataUtil()
    Base.metadata.create_all(du.engine)