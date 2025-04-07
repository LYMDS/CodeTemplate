from pyodbc import drivers

from Common.DataUtil import *
from Common.DriverBase import DirverBase
from sqlalchemy import create_engine,MetaData,Table
from sqlalchemy.orm import declarative_base
import datetime
#from DataDriver.driver_sqlserver import DriverSqlServer

from sqlalchemy.sql import text
import clr
import sys
import importlib
# sys.path.append(r"C:\D\PythonWorkSpace\jinja2代码模板项目\DriverCRM\DriverCrm\bin\Debug")

#clr.AddReference("DriverCrm")
# 导入 C# 中的命名空间和类
#from DriverCrm import DataDriverCrm

# 调用 C# 类中的方法
#DataDriverCrm.crmConnectionString = ""
#name = DataDriverCrm.excute("account")
#print(name)

#d = DriverSqlServer()
#d.server = ""
#d.port = ""
#d.username = ""
#d.password = ""
#d.init_engine()
#d.get_session()

#res = d.session.execute(text('select top 2 * from account'))


# 处理结果
#for row in res:
#    print(row)
#d.session.close()

# mods = dir(DataDriver)
# for m in mods:
#     importlib.import_module(f"DataDriver.{m}")
# 动态导入模块

import pkgutil

from DataDriver.DriverGuide.TestGuide import TestGuide


def get_all_modules(package_name):
    """
    获取指定包下所有的模块
    :param package_name: 包名
    :return: 模块列表
    """
    package = __import__(package_name, fromlist=['__path__'])
    return [module for _, module, _ in pkgutil.walk_packages(package.__path__)]


# 使用示例
package_name = 'DataDriver'
modules = get_all_modules(package_name)
for module in modules:
    importlib.import_module(f"DataDriver.{module}")
ds = DirverBase.__subclasses__()
print(ds[1])
print(ds[1]().DriverName)

from DataDriver.DriverGuide.TemplateParamGuide import TemplateParamGuide

from DataDriver.driver_crm import DriverCrm


print(DirverBase.all_registered())
print(DirverBase.get_driver_optionset())
driver = DirverBase.get_driver(name="SQL Server")()
tg = TestGuide()
driver.DriverParams = tg.get()
result = driver.execute()
print(result)