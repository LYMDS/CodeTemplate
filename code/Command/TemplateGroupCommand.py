from Common.InitDataUtil import *
from sqlalchemy import or_
from Models.new_template_group import *
import json
from objtyping import to_primitive



class TemplateGroupCommand(InitDataUtil):

    # 获取列表
    def getlist(self, search):
        templateGroupList = self.DataServer.session.query(new_template_group) \
            .filter(or_(new_template_group.new_name.like(f"%{search}%"), search == "")).all()
        return json.dumps(to_primitive(templateGroupList))

    # 保存
    def save(self, data):
        id = data["new_template_groupid"]
        saveTable = new_template_group()

        if id != "": # 更新
            saveTable = self.DataServer.session.query(new_template_group).filter(new_template_group.new_template_groupid == id).first()
        else: # 创建
            self.DataServer.session.add(saveTable)

        saveTable.new_name = data["new_name"]
        saveTable.new_note = data["new_note"]

        self.DataServer.session.commit()
        id = saveTable.new_template_groupid
        self.DataServer.session.close()
        print(id)
        return id

    # 根据Id获取一条数据
    def get(self, id):
        templateGroup = self.DataServer.session.get(new_template_group, id)
        return json.dumps(to_primitive(templateGroup))

    # 删除
    def delete(self, ids):
        self.DataServer.session.query(new_template_group).filter(new_template_group.new_template_groupid.in_(ids)).delete()
        self.DataServer.session.commit()
        self.DataServer.session.close()
        return ids
