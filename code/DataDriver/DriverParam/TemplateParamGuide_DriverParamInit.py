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
            CreateDataParameter("Server", "Server", 1, 1, datadriverid, None),
            CreateDataParameter("AuthType", "AuthType", 1, 1, datadriverid, None),
            CreateDataParameter("Domain", "Domain", 1, 1, datadriverid, None),
            CreateDataParameter("UserName", "UserName", 1, 1, datadriverid, None),
            CreateDataParameter("Password", "Password", 1, 1, datadriverid, None),
            CreateDataParameter("ClientId", "ClientId", 1, 1, datadriverid, None),
            CreateDataParameter("ClientSecret", "ClientSecret", 1, 1, datadriverid, None)
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


class TemplateParamGuide_driver_excel_ParamInit(DirverParamInitBase):
    GuideName = "Template Param Data Guide"
    DriverName = "Excel"

    def __init__(self, session):
        # self.session = Session(bind=connection)
        self.session = session

    def CreateBaseParam(self, datadriverid):
        paramList = [

        ]
        for param in paramList:
            self.session.add(param)
        self.session.commit()
        self.session.close()

    def CreateExecParam(self, datadriverid, templateparamid):
        paramList = [
            CreateDataParameter("xlsx_path", "Excel路径", 3, 2, datadriverid, templateparamid),
            CreateDataParameter("sheet_name", "Sheet页名", 1, 2, datadriverid, templateparamid),
        ]
        for param in paramList:
            self.session.add(param)
        self.session.commit()
        # self.session.close()