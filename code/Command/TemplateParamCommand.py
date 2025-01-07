from Common.InitDataUtil import *
from sqlalchemy import or_, and_, asc, desc, alias
from sqlalchemy.orm import aliased
from Models.new_template_param import *
from Models.new_template_content import *
import json
from objtyping import to_primitive
from Common.DataModelMaker import *


class TemplateParamCommand(InitDataUtil):

    def getlistbycontentid(self, id):
        templateParamList = self._getlistbycontentid(id)
        return sqlalchemydata_tojson(sqlalchemydatalist_todclist(templateParamList))

    def _getlistbycontentid(self, id):
        new_template_content_alias = aliased(new_template_content)
        templateParamList = self.DataServer.session.query(
            new_template_param.new_template_paramid,
            new_template_param.new_name,
            new_template_param.new_type,
            new_template_param.new_value,
            new_template_param.new_template_group_id,
            new_template_param.new_template_code_id,
            new_template_param.new_createdon,
            new_template_param.new_modifiedon,
            new_template_content_alias.new_file_name) \
            .outerjoin(new_template_content_alias,
                       new_template_param.new_template_code_id == new_template_content_alias.new_template_contentid) \
            .filter(new_template_param.new_template_code_id == id) \
            .order_by(asc(new_template_param.new_createdon)) \
            .all()
        return templateParamList

    def getlistbygroupid(self, id):
        templateParamList = self._getlistbygroupid(id)
        return sqlalchemydata_tojson(sqlalchemydatalist_todclist(templateParamList))

    def _getlistbygroupid(self, id):
        new_template_content_alias = aliased(new_template_content)
        templateParamList = self.DataServer.session.query(
            new_template_param.new_template_paramid,
            new_template_param.new_name,
            new_template_param.new_type,
            new_template_param.new_value,
            new_template_param.new_template_group_id,
            new_template_param.new_template_code_id,
            new_template_param.new_createdon,
            new_template_param.new_modifiedon,
            new_template_content_alias.new_file_name) \
            .outerjoin(new_template_content_alias,
                       new_template_param.new_template_code_id == new_template_content_alias.new_template_contentid) \
            .filter(new_template_param.new_template_group_id == id) \
            .order_by(asc(new_template_param.new_template_code_id).nullsfirst(), asc(new_template_param.new_createdon)) \
            .all()
        return templateParamList


    def _getlist_with_global_param(self, groupid, contentid):
        templateParamList = self.DataServer.session.query(new_template_param).filter(
            or_(new_template_param.new_template_code_id == contentid, # 当前文件级本地参数
                and_(new_template_param.new_template_group_id == groupid, # 当前模板级全局参数
                     new_template_param.new_template_code_id == ""
                     )
                )
        ).all()
        return templateParamList



    # 根据Id获取一条数据
    def get(self, id):
        data = self.DataServer.session.get(new_template_param, id)
        return json.dumps(to_primitive(data))

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

    # 批量保存
    def batch_save(self, data_list):
        if not data_list:
            raise ValueError("data list为空")

        for data in data_list:
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
        self.DataServer.session.close()
        return "Success"

    # 删除
    def delete(self, ids):
        self.DataServer.session.query(new_template_param).filter(
            new_template_param.new_template_paramid.in_(ids)).delete()
        self.DataServer.session.commit()
        self.DataServer.session.close()
        return ids

