import json
from objtyping import to_primitive

# sqlalchemy列表转字典对象
# 自动获取fields key并组装成字典
def sqlalchemydatalist_todclist(sqlalchemydatalist):
    return [sqlalchemydata_todict(data) for data in sqlalchemydatalist]

def sqlalchemydata_todict(sqlalchemydata):
    return {field: sqlalchemydata[sqlalchemydata._key_to_index[field]] for field in sqlalchemydata._fields}

# sqlalchemy列表或模型数据转json对象
def sqlalchemydata_tojson(sqlalchemydata):
    return tojson(toprimitive(sqlalchemydata))

def tojson(data):
    return json.dumps(data)

def toprimitive(data):
    return to_primitive(data)