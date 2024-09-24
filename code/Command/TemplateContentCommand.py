from Common.InitDataUtil import *
from sqlalchemy import or_
from Models.new_template_content import *
import json
from objtyping import to_primitive

class TemplateContentCommand(InitDataUtil):

    # 根据模板Id获取内容明细
    def getlistbygroupid(self, id):
        templateContentList = self.DataServer.session.query(new_template_content)\
            .filter(new_template_content.new_template_group_id == id).all()
        return json.dumps(to_primitive(templateContentList))

    # 保存
    def save(self, data):
        id = data["new_template_contentid"]
        saveTable = new_template_content()

        if id != "": # 更新
            saveTable = self.DataServer.session.query(new_template_content).filter(new_template_content.new_template_contentid == id).first()
        else: # 创建
            self.DataServer.session.add(saveTable)
            saveTable.new_template_group_id = data["new_template_group_id"]

        saveTable.new_content = data["new_content"]
        saveTable.new_file_name = data["new_file_name"]
        saveTable.new_file_type = data["new_file_type"]
        saveTable.new_attachment_id = data["new_attachment_id"]

        self.DataServer.session.commit()
        id = saveTable.new_template_contentid
        self.DataServer.session.close()
        print(id)
        return id

    # 根据Id获取一条数据
    def get(self, id):
        data = self.DataServer.session.get(new_template_content, id)
        return json.dumps(to_primitive(data))