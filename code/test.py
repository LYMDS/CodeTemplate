from Common.DataUtil import *
from Models.new_template_group import *
from sqlalchemy import create_engine,MetaData,Table
from sqlalchemy.orm import declarative_base
import datetime


du = DataUtil()
du.get_session()
tg = new_template_group()
tg.new_name = "测试模板组"
tg.new_folder_name = "Dyson"
tg.new_note = "用于测试"

du.session.add(tg)
du.session.commit()

