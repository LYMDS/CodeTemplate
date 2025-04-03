from Common.DriverBase import DirverBase
from DataDriver.driver_crm import *
from DataDriver.driver_sqlserver import *
from Common.InitDataUtil import *
from Models.DataDriver import *
from Models.DataParameter import *
from Common.DataModelMaker import *
from sqlalchemy import or_
from Event.DataDriverEvent import after_insert
from Event.DataDriverEvent import before_delete


class DataDriverCommand(InitDataUtil):
    def get(self, id):
        data = self._get(id)
        return sqlalchemydata_tojson(data)

    def _get(self, id):
        data = self.DataServer.session.get(DataDriver, id)
        return data

    # 获取列表
    def getlist(self, search):
        datadriverList = self.DataServer.session.query(DataDriver) \
            .filter(or_(DataDriver.name.like(f"%{search}%"), search == "")).all()
        return sqlalchemydata_tojson(datadriverList)

    # 保存
    def save(self, data):
        id = data["datadriverid"]
        saveTable = DataDriver()

        if id != "":  # 更新
            saveTable = self.DataServer.session.query(DataDriver).filter(DataDriver.datadriverid == id).first()
        else:  # 创建
            self.DataServer.session.add(saveTable)

        saveTable.name = data["name"]
        saveTable.desc = data["desc"]
        saveTable.type = data["type"]

        self.DataServer.session.commit()
        id = saveTable.datadriverid
        self.DataServer.session.close()
        print(id)
        return id

    # 删除
    def delete(self, ids):
        targets = self.DataServer.session.query(DataDriver).filter(
            DataDriver.datadriverid.in_(ids)
        ).all()

        for target in targets:
            self.DataServer.session.delete(target)

        self.DataServer.session.commit()
        self.DataServer.session.close()
        return ids

    # 获取驱动器类型列表
    def get_type_optionset(self):
        return DirverBase.get_driver_optionset()