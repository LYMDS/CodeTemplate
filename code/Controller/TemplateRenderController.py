from flask import Blueprint,Flask,request
from Command.TemplateRenderCommand import *

TemplateRenderController = Blueprint('TemplateRenderController', __name__)

@TemplateRenderController.route('/api/templaterender/test/', methods=['POST'])
def templaterender_test():
    return TemplateRenderCommand().test(request.get_json())

@TemplateRenderController.route('/api/templaterender/template_content/', methods=['GET'])
def templaterender_template_content():
    id = request.args.get("id", "", type=str)
    return TemplateRenderCommand().template_content(id)