from flask import Blueprint,Flask,request
from Command.DataDriverCommand import *

DataDriverController = Blueprint('DataDriverController', __name__)

@DataDriverController.route('/api/datadriver/getlist/', methods=['GET'])
def datadriver_getlist():
    search = request.args.get("search", "", type=str)
    return DataDriverCommand().getlist(search)

@DataDriverController.route('/api/datadriver/get/', methods=['GET'])
def datadriver_get():
    id = request.args.get("id", "", type=str)
    return DataDriverCommand().get(id)

@DataDriverController.route('/api/datadriver/save/', methods=['POST'])
def datadriver_save():
    return DataDriverCommand().save(request.get_json())

@DataDriverController.route('/api/datadriver/delete/', methods=['POST'])
def datadriver_delete():
    return DataDriverCommand().delete(request.get_json())

@DataDriverController.route('/api/datadriver/gettypeoptionset/', methods=['GET'])
def datadriver_get_type_optionset():
    return DataDriverCommand().get_type_optionset()