from Common.GuideBase import GuideBase
class TestGuide(GuideBase):

    GuideName = "TestGuide"
    GuideDescribe = "测试引导"

    def get(self):
        # DataDriverCrm.crmConnectionString = ""
        # return DataDriverCrm.excute("")
        return {
            "CrmConnectionString": "AuthType=AD;Server=http://121.33.201.38:10005/bain;Domain=BAINDEV;UserName=crmadmin;Password=BAin@202403",
            "EntityName": "account",

            "username": "sa",
            "password": "p@ssw0rd",
            "server": "172.20.11.156",
            "port": "1433",
            "database": "neusemi_MSCRM",
            "sql": "select top 10 FullName,new_account_id,new_account_idName,new_address from Lead",
        }