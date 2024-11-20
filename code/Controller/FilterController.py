from flask import Blueprint,Flask,request
from Command.FilterCommand import *

FilterController = Blueprint('FilterController', __name__)

@FilterController.route('/api/new_filter/getlist/', methods=['GET'])
def new_filter_getlist():
    search = request.args.get("search", "", type=str)
    return FilterCommand().getlist(search)

@FilterController.route('/api/new_filter/get/', methods=['GET'])
def new_filter_get():
    id = request.args.get("id", "", type=str)
    return FilterCommand().get(id)

@FilterController.route('/api/new_filter/save/', methods=['POST'])
def new_filter_save():
    return FilterCommand().save(request.get_json())

@FilterController.route('/api/new_filter/delete/', methods=['POST'])
def new_filter_delete():
    return FilterCommand().delete(request.get_json())