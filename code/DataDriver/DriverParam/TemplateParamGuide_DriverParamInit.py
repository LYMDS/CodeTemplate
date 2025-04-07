from Common.DriverParamInitBase import DirverParamInitBase
from Common.DataUtil import *
from Models.DataParameter import DataParameter
from sqlalchemy.orm import sessionmaker,Session

def CreateDataParameter(name, desc, type, nature, datadriver_id, new_template_param_id):
    dp = DataParameter()
    dp.name = name
    dp.desc = desc
    dp.type = type
    dp.nature = nature
    dp.datadriver_id = datadriver_id
    dp.new_template_param_id = new_template_param_id
    dp.value = ""
    return dp

class TemplateParamGuide_driver_crm_ParamInit(DirverParamInitBase):

    GuideName = "Template Param Data Guide"
    DriverName = "CRM"

    def __init__(self, session):
        #self.session = Session(bind=connection)
        self.session = session

    def CreateBaseParam(self, datadriverid):
        paramList = [
            CreateDataParameter("CrmConnectionString", "CRM连接字符串", 1, 1,
                                datadriverid, None),
        ]
        for param in paramList:
            self.session.add(param)
        self.session.commit()
        self.session.close()

    def CreateExecParam(self, datadriverid, templateparamid):
        paramList = [
            CreateDataParameter("EntityName", "实体名", 1, 2,
                                datadriverid, templateparamid),
        ]
        for param in paramList:
            self.session.add(param)
        self.session.commit()
        #self.session.close()


class TemplateParamGuide_driver_sqlserver_ParamInit(DirverParamInitBase):

    GuideName = "Template Param Data Guide"
    DriverName = "SQL Server"

    def __init__(self, session):
        #self.session = Session(bind=connection)
        self.session = session

    def CreateBaseParam(self, datadriverid):
        paramList = [
            CreateDataParameter("server", "服务器地址", 1, 1,
                                datadriverid, None),
            CreateDataParameter("port", "端口号", 1, 1,
                                datadriverid, None),
            CreateDataParameter("username", "用户名", 1, 1,
                                datadriverid, None),
            CreateDataParameter("password", "密码", 1, 1,
                                datadriverid, None),
            CreateDataParameter("database", "数据库", 1, 1,
                                datadriverid, None),
        ]
        for param in paramList:
            self.session.add(param)
        self.session.commit()
        self.session.close()

    def CreateExecParam(self, datadriverid, templateparamid):
        paramList = [
            CreateDataParameter("sql", "SQL表达式", 1, 2,
                                datadriverid, templateparamid),
        ]
        for param in paramList:
            self.session.add(param)
        self.session.commit()
        #self.session.close()


