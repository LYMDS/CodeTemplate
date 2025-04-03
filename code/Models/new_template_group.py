#from __future__ import unicode_literals, absolute_import
from Models.Base import Base
from sqlalchemy import Column, Integer, String, DateTime, MetaData
from Common.Uuid import *
from Common.DataUtil import *
import datetime

class new_template_group(Base):
    __tablename__ = "new_template_group"

    new_template_groupid = Column(String(32), primary_key=True, unique=True, default=Uuid.get_hex)
    new_name = Column(String(255))
    new_note = Column(String(500))
    new_folder_name = Column(String(100))
    new_createdon = Column(DateTime, default=datetime.datetime.now)
    new_modifiedon = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

if __name__ == "__main__":
    du = DataUtil()
    Base.metadata.create_all(du.engine)