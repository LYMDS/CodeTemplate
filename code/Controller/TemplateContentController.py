from flask import Blueprint,request
from Command.TemplateContentCommand import *

TemplateContentController = Blueprint('TemplateContentController', __name__)

@TemplateContentController.route('/api/new_template_content/getlistbygroupid/', methods=['GET'])
def new_template_content_getlistbygroupid():
    id = request.args.get("id", "", type=str)
    return TemplateContentCommand().getlistbygroupid(id)

@TemplateContentController.route('/api/new_template_content/save/', methods=['POST'])
def new_template_content_save():
    return TemplateContentCommand().save(request.get_json())

@TemplateContentController.route('/api/new_template_content/get/', methods=['GET'])
def new_template_content_get():
    id = request.args.get("id", "", type=str)
    return TemplateContentCommand().get(id)

@TemplateContentController.route('/api/new_template_content/delete/', methods=['POST'])
def new_template_group_delete():
    return TemplateContentCommand().delete(request.get_json())