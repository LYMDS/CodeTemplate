from Common.InitDataUtil import *
from Common.Jinja2Helper import *
from sqlalchemy import or_
from Models.new_template_param import *
from Models.new_attachment import *
from Models.new_template_content import *
from Models.new_template_group import *
from Command.TemplateContentCommand import *
from Command.TemplateParamCommand import *
from Command.AttachmentCommand import *
import json
from objtyping import to_primitive

class TemplateRenderCommand(InitDataUtil):

    def test(self, data):
        j = Jinja2Helper()
        return j.auto_render_one("test", data["template"], data["params"])

    def template_content(self, id):
        j = Jinja2Helper()
        content_data = TemplateContentCommand()._get(id)
        params_data = TemplateParamCommand()._getlistbycontentid(id)

        if content_data.new_attachment_id is None or content_data.new_attachment_id == "":
            raise ValueError("未上传模板文件")
        bytes = AttachmentCommand().get_content(content_data.new_attachment_id)
        template_content = bytes.decode("utf-8")
        params = {}
        if params_data != None and len(params_data) > 0:
            for p in params_data:
                params[p.new_name] = p.new_value
        return j.auto_render_one(content_data.new_file_name, template_content, params)

