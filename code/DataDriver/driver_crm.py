from Common.DriverBase import DirverBase
import clr
import sys
class DriverCrm(DirverBase):

    DriverName = "CRM"
    DriverDescribe = "CRM连接器"
    DriverParams = None

    def execute(self):
        sys.path.append(r"C:\D\PythonWorkSpace\jinja2代码模板项目\DriverCRM\DriverCrm\bin\Debug")
        clr.AddReference("DriverCrm")

        # 导入 C# 中的命名空间和类
        from DriverCrm import DataDriverCrm
        # 调用 C# 类中的方法
        DataDriverCrm.crmConnectionString = self.DriverParams["CrmConnectionString"]
        return DataDriverCrm.excute(self.DriverParams["EntityName"])
