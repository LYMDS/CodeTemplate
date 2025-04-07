from Common.DataUtil import *
from sqlalchemy import create_engine,MetaData,Table
from sqlalchemy.orm import declarative_base
import datetime
from Controller.AttachmentController import *
from Common.Jinja2Helper import Jinja2Helper
from jinja2 import Environment, meta

test_template = "{{obj.name}} {{name}} {% for user in users %}<li>{{ user.username }}</li>{% endfor %}"

test_params = {
    "obj": {
        'name': 'dysonliu'
    },
    # 'name': '',
    'users': [{'username': ''},{'username': ''},{'username': ''}]
}

j = Jinja2Helper()
j.add("test", test_template)
j.load()
template = j.parse("test")
soucre = j.add_style_for_preview(template)
t = j.get_template_from_source("test", soucre)
output = t.render(test_params)
# j.load_with_extensions()
#output = j.render_one("test", test_params)
print(output)

