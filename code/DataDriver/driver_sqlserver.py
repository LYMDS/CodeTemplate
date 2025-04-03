from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
from Common.DriverBase import DirverBase
from urllib.parse import quote

class DriverSqlServer(DirverBase):
    DriverName = "SQL Server"
    DriverDescribe = "SQL Server驱动连接器"
    DriverParams = None

    server = ''
    port = ''
    username = ''
    password = ''
    database = '*'
    driver = 'SQL Server'
    DataBaseUrl = ''
    sql = ""

    # 初始化引擎
    def init_engine(self):
        self.DataBaseUrl = f'mssql+pyodbc://{quote(self.username)}:{quote(self.password)}@{self.server}:{self.port}/{self.database}?driver={self.driver}'
        self.engine = create_engine(self.DataBaseUrl, echo=True, pool_size=8, pool_recycle=60 * 30)

    # 获取Session
    def get_session(self):
        DbSession = sessionmaker(bind=self.engine)
        self.session = DbSession()

    # 初始化属性
    def init_attributes(self):
        self.username = self.DriverParams["username"]
        self.password = self.DriverParams["password"]
        self.server = self.DriverParams["server"]
        self.port = self.DriverParams["port"]
        self.database = self.DriverParams["database"]
        self.sql = self.DriverParams["sql"]

    def execute(self):
        self.init_attributes()
        self.init_engine()
        print(self.DataBaseUrl)
        self.get_session()
        result = self.session.execute(text(self.sql))
        headers  = result.keys()
        rows = result.fetchall()
        result_with_headers = [tuple(headers._keys), *rows]
        return result_with_headers
