from Common.GuideBase import GuideBase
class TestGuide(GuideBase):

    GuideName = "TestGuide"
    GuideDescribe = "测试引导"

    def get(self):
        # DataDriverCrm.crmConnectionString = ""
        # return DataDriverCrm.excute("")
        return {
            "CrmConnectionString": "",
            "EntityName": "account",

            "username": "sa",
            "password": "",
            "server": "",
            "port": "",
            "database": "",
            "sql": "",
        }