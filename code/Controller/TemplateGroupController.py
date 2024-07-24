from flask import Blueprint,Flask,request
from Command.TemplateGroupCommand import *

TemplateGroupController = Blueprint('TemplateGroupController', __name__)

@TemplateGroupController.route('/api/new_template_group/getlist/', methods=['GET'])
def new_template_group_getlist():
    search = request.args.get("search", "", type=str)
    return TemplateGroupCommand().getlist(search)

@TemplateGroupController.route('/api/new_template_group/get/', methods=['GET'])
def new_template_group_get():
    id = request.args.get("id", "", type=str)
    return TemplateGroupCommand().get(id)

@TemplateGroupController.route('/api/new_template_group/save/', methods=['POST'])
def new_template_group_save():
    return TemplateGroupCommand().save(request.get_json())

@TemplateGroupController.route('/api/new_template_group/delete/', methods=['POST'])
def new_template_group_delete():
    return TemplateGroupCommand().delete(request.get_json())