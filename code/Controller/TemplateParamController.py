from flask import Blueprint,Flask,request
from Command.TemplateParamCommand import *

TemplateParamController = Blueprint('TemplateParamController', __name__)


@TemplateParamController.route('/api/new_template_param/getlistbycontentid/', methods=['GET'])
def new_template_param_getlistbycontentid():
    id = request.args.get("id", "", type=str)
    return TemplateParamCommand().getlistbycontentid(id)

@TemplateParamController.route('/api/new_template_param/save/', methods=['POST'])
def new_template_param_save():
    return TemplateParamCommand().save(request.get_json())

@TemplateParamController.route('/api/new_template_param/get/', methods=['GET'])
def new_template_param_get():
    id = request.args.get("id", "", type=str)
    return TemplateParamCommand().get(id)

@TemplateParamController.route('/api/new_template_param/delete/', methods=['POST'])
def new_template_param_delete():
    return TemplateParamCommand().delete(request.get_json())
