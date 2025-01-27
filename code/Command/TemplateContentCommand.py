from Common.InitDataUtil import *
from sqlalchemy import or_
from Models.new_template_content import *
import json
from objtyping import to_primitive
from Command.AttachmentCommand import *

class TemplateContentCommand(InitDataUtil):

    # 根据模板Id获取内容明细
    def getlistbygroupid(self, id):
        templateContentList = self.DataServer.session.query(new_template_content)\
            .filter(new_template_content.new_template_group_id == id).all()
        return json.dumps(to_primitive(templateContentList))

    # 根据模板Id获取内容明细
    def _getlistbygroupid(self, id):
        templateContentList = self.DataServer.session.query(new_template_content) \
            .filter(new_template_content.new_template_group_id == id).all()
        return templateContentList

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

    def _get(self, id):
        return self.DataServer.session.get(new_template_content, id)

    # 删除
    def delete(self, ids):
        self.DataServer.session.query(new_template_content).filter(
            new_template_content.new_template_contentid.in_(ids)).delete()
        self.DataServer.session.commit()
        self.DataServer.session.close()
        return ids

    # 保存代码
    def savecode(self, data):
        id = data["id"]
        content = data["content"]
        template_content = self.DataServer.session.get(new_template_content, id)
        attachmentId = AttachmentCommand().save(template_content.new_attachment_id, template_content.new_file_name + ".txt", content.encode())
        if template_content.new_attachment_id != attachmentId:
            template_content.new_attachment_id = attachmentId
            self.DataServer.session.commit()
        self.DataServer.session.close()
        return ""