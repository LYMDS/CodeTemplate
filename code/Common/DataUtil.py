from sqlalchemy import create_engine,MetaData,Table
from sqlalchemy.orm import sessionmaker


class DataUtil:

    # 初始化函数
    def __init__(self):
         self.engine = create_engine('sqlite:///C:\\D\\PythonWorkSpace\\jinja2代码模板项目\\CodeTemplate.db', echo=True, pool_size=8, pool_recycle=60*30)

    # 获取Session
    def get_session(self):
        DbSession = sessionmaker(bind=self.engine)
        self.session = DbSession()











