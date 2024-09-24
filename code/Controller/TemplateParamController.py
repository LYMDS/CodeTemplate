from flask import Blueprint,Flask,request
from Command.TemplateParamCommand import *

TemplateParamController = Blueprint('TemplateParamController', __name__)


@TemplateParamController.route('/api/new_template_param/getlistbycontentid/', methods=['GET'])
def new_template_param_getlistbycontentid():
    id = request.args.get("id", "", type=str)
    return TemplateParamCommand().getlistbycontentid(id)




