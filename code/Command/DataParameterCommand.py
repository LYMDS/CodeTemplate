from Common.InitDataUtil import *
from Models.DataDriver import *
from Models.DataParameter import *
from Common.DataModelMaker import *
from sqlalchemy import and_

class DataParameterCommand(InitDataUtil):
    def get(self, id):
        data = self._get(id)
        return sqlalchemydata_tojson(data)

    def _get(self, id):
        data = self.DataServer.session.get(DataParameter, id)
        return data

    def getlist_by_datadriverid(self, id):
        DataParameterList = self._getlist_by_datadriverid(id)
        return sqlalchemydata_tojson(DataParameterList)

    def _getlist_by_datadriverid(self, id):
        DataParameterList = self.DataServer.session.query(DataParameter) \
            .filter(and_(DataParameter.datadriver_id == id, DataParameter.nature == 1)).all()
        return DataParameterList

    def getlist_by_templateparamid(self, id):
        DataParameterList = self._getlist_by_templateparamid(id)
        return sqlalchemydata_tojson(DataParameterList)

    def _getlist_by_templateparamid(self, id):
        DataParameterList = self.DataServer.session.query(DataParameter) \
            .filter(and_(DataParameter.new_template_param_id == id, DataParameter.nature == 2)).all()
        return DataParameterList

    # 批量保存
    def batch_save(self, data_list):
        if not data_list:
            raise ValueError("data list为空")

        for data in data_list:
            id = data["dataparameterid"]
            saveTable = DataParameter()

            if id != "":  # 更新
                saveTable = self.DataServer.session.query(DataParameter).filter(
                    DataParameter.dataparameterid == id).first()
            else:  # 创建 （只更新数据 不创建数据）
                self.DataServer.session.add(saveTable)

            saveTable.name = data["name"]
            saveTable.value = data["value"]

        self.DataServer.session.commit()
        self.DataServer.session.close()
        return "Success"

    # 删除
    def delete(self, ids):
        self.DataServer.session.query(DataParameter).filter(DataParameter.dataparameterid.in_(ids)).delete()
        self.DataServer.session.commit()
        self.DataServer.session.close()
        return ids

    def _delete(self, ids):

        targets = self.DataServer.session.query(DataParameter).filter(
            DataParameter.dataparameterid.in_(ids)
        ).all()

        for target in targets:
            self.DataServer.session.delete(target)

        self.DataServer.session.commit()
        return ids