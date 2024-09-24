from Common.InitDataUtil import *
from sqlalchemy import or_
from Models.new_template_param import *
import json
from objtyping import to_primitive


class TemplateParamCommand(InitDataUtil):

    def getlistbycontentid(self, id):
        templateParamList = self.DataServer.session.query(new_template_param) \
            .filter(new_template_param.new_template_code_id == id).all()
        return json.dumps(to_primitive(templateParamList))

    # 保存
    def save(self, data):
        id = data["new_template_paramid"]
        saveTable = new_template_param()

        if id != "":  # 更新
            saveTable = self.DataServer.session.query(new_template_param).filter(
                new_template_param.new_template_paramid == id).first()
        else:  # 创建
            self.DataServer.session.add(saveTable)
            saveTable.new_template_group_id = data["new_template_group_id"]
            saveTable.new_template_code_id = data["new_template_code_id"]

        saveTable.new_name = data["new_name"]
        saveTable.new_type = data["new_type"]
        saveTable.new_value = data["new_value"]

        self.DataServer.session.commit()
        id = saveTable.new_template_paramid
        self.DataServer.session.close()
        print(id)
        return id

