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
import zipfile
from flask import make_response
from Command.DataDriverCommand import DataDriverCommand
from DataDriver.DriverGuide.TemplateParamGuide import TemplateParamGuide
from Common.DriverBase import DirverBase

class TemplateRenderCommand(InitDataUtil):

    def test(self, data):
        j = Jinja2Helper()
        return j.auto_render_one("test", data["template"], data["params"])

    def template_content(self, id):
        j = Jinja2Helper()
        content_data = TemplateContentCommand()._get(id)
        # params_data = TemplateParamCommand()._getlistbycontentid(id)
        params_data = TemplateParamCommand()._getlist_with_global_param(content_data.new_template_group_id ,id)
        if content_data.new_attachment_id is None or content_data.new_attachment_id == "":
            raise ValueError("未上传模板文件")
        bytes = AttachmentCommand().get_content(content_data.new_attachment_id)
        template_content = bytes.decode("utf-8")
        params = {}
        if params_data != None and len(params_data) > 0:
            for p in params_data:
                if p.new_datadriver_id not in (None, ""):
                    # 获取驱动器基本信息
                    driver = DataDriverCommand()._get(p.new_datadriver_id)
                    # 获取驱动参数
                    guide = TemplateParamGuide()
                    driver_params = guide.get(p.new_datadriver_id, p.new_template_paramid)
                    # 获取驱动实例
                    driver_inst = DirverBase.get_driver(name=driver.type)()
                    # 设置参数并执行
                    driver_inst.DriverParams = driver_params
                    driver_result = driver_inst.execute()
                    # 处理驱动结果
                    p.new_value = driver_result
                if p.new_type == 1: # 文本
                    params[p.new_name] = p.new_value
                elif p.new_type == 2: # 对象
                    params[p.new_name] = json.loads(p.new_value)
                elif p.new_type == 3: # 列表
                    params[p.new_name] = json.loads(p.new_value)
        return j.auto_render_one(content_data.new_file_name, template_content, params)

    def template_group(self, id):
        templatecontentList = TemplateContentCommand()._getlistbygroupid(id)
        if templatecontentList != None and len(templatecontentList) > 0:
            # 创建一个内存中的文件对象
            memory_file = io.BytesIO()
            # 创建一个 ZIP 文件对象
            with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for content_data in templatecontentList:
                    j = Jinja2Helper()
                    params_data = TemplateParamCommand()._getlist_with_global_param(content_data.new_template_group_id, content_data.new_template_contentid)
                    if content_data.new_attachment_id is None or content_data.new_attachment_id == "":
                        raise ValueError("未上传模板文件")
                    attachment = AttachmentCommand()._get(content_data.new_attachment_id)
                    bytes = attachment.new_content
                    template_content = bytes.decode("utf-8")
                    params = {}
                    if params_data != None and len(params_data) > 0:
                        for p in params_data:
                            if p.new_datadriver_id not in (None, ""):
                                # 获取驱动器基本信息
                                driver = DataDriverCommand()._get(p.new_datadriver_id)
                                # 获取驱动参数
                                guide = TemplateParamGuide()
                                driver_params = guide.get(p.new_datadriver_id, p.new_template_paramid)
                                # 获取驱动实例
                                driver_inst = DirverBase.get_driver(name=driver.type)()
                                # 设置参数并执行
                                driver_inst.DriverParams = driver_params
                                driver_result = driver_inst.execute()
                                # 处理驱动结果
                                p.new_value = driver_result
                            if p.new_type == 1:  # 文本
                                params[p.new_name] = p.new_value
                            elif p.new_type == 2:  # 对象
                                params[p.new_name] = json.loads(p.new_value)
                            elif p.new_type == 3:  # 列表
                                params[p.new_name] = json.loads(p.new_value)
                    render_str = j.auto_render_one(content_data.new_file_name, template_content, params)
                    zipf.writestr(attachment.new_name ,render_str.encode())
            # 将内存中的文件对象移动到起始位置
            memory_file.seek(0)
            # 创建一个响应对象，将 ZIP 文件作为附件发送
            response = make_response(memory_file.getvalue())
            response.headers['Content-Disposition'] = 'attachment; filename=files.zip'
            response.headers['Content-Type'] = 'application/zip'
            return response
        else:
            raise ValueError("没有文件可以生成")


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
        #template_content = html.escape(template_content) 牺牲源代码中本来有的html代码被展示
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
