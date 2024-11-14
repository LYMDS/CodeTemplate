from Common.InitDataUtil import *
from sqlalchemy import or_
from Models.new_filter import *
import json
from objtyping import to_primitive



class FilterCommand(InitDataUtil):

    # 获取列表
    def getlist(self, search):
        filterList = self.DataServer.session.query(new_filter) \
            .filter(or_(new_filter.new_name.like(f"%{search}%"), search == "")).all()
        return json.dumps(to_primitive(filterList))

    # 保存
    def save(self, data):
        id = data["new_filterid"]
        saveTable = new_filter()

        if id != "": # 更新
            saveTable = self.DataServer.session.query(new_filter).filter(new_filter.new_filterid == id).first()
        else: # 创建
            self.DataServer.session.add(saveTable)

        saveTable.new_name = data["new_name"]
        saveTable.new_memo = data["new_memo"]
        saveTable.new_func = data["new_func"]

        self.DataServer.session.commit()
        id = saveTable.new_filterid
        self.DataServer.session.close()
        print(id)
        return id

    # 根据Id获取一条数据
    def get(self, id):
        filterList = self.DataServer.session.get(new_filter, id)
        return json.dumps(to_primitive(filterList))

    # 删除
    def delete(self, ids):
        self.DataServer.session.query(new_filter).filter(new_filter.new_filterid.in_(ids)).delete()
        self.DataServer.session.commit()
        self.DataServer.session.close()
        return ids
