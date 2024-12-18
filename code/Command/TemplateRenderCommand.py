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
import html

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
                if p.new_type == 1: # 文本
                    params[p.new_name] = p.new_value
                elif p.new_type == 2: # 对象
                    params[p.new_name] = json.loads(p.new_value)
                elif p.new_type == 3: # 列表
                    params[p.new_name] = json.loads(p.new_value)
        return j.auto_render_one(content_data.new_file_name, template_content, params)

    def preview_template_content(self, id):
        j = Jinja2Helper()
        content_data = TemplateContentCommand()._get(id)
        params_data = TemplateParamCommand()._getlistbycontentid(id)

        if content_data.new_attachment_id is None or content_data.new_attachment_id == "":
            return ""
            # raise ValueError("未上传模板文件")
        bytes = AttachmentCommand().get_content(content_data.new_attachment_id)
        template_content = bytes.decode("utf-8")
        # html转义
        template_content = html.escape(template_content)
        #与{{obj["name"]}}的参数写法冲突 html.escape将"转义了
        params = {}
        # if params_data != None and len(params_data) > 0:
        #     for p in params_data:
        #         params[p.new_name] = "<span style='color: red'>" + p.new_name + "</span>"
        j.add(content_data.new_file_name, template_content)
        j.load()
        template = j.parse(content_data.new_file_name)
        soucre = j.add_style_for_preview(template)
        t = j.get_template_from_source(content_data.new_file_name, soucre)
        return t.render(params)
        # return j.auto_render_one(content_data.new_file_name, template_content, params)

    def edit_template_content(self, id):
        j = Jinja2Helper()
        content_data = TemplateContentCommand()._get(id)

        if content_data.new_attachment_id is None or content_data.new_attachment_id == "":
            return ""
        bytes = AttachmentCommand().get_content(content_data.new_attachment_id)
        template_content = bytes.decode("utf-8")
        return template_content
