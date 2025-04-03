from flask import Blueprint,Flask,request
from Command.DataParameterCommand import *

DataParameterController = Blueprint('DataParameterController', __name__)

@DataParameterController.route('/api/dataparameter/getlistbydatadriverid/', methods=['GET'])
def dataparameter_getlist_by_datadriverid():
    id = request.args.get("id", "", type=str)
    return DataParameterCommand().getlist_by_datadriverid(id)

@DataParameterController.route('/api/dataparameter/getlistbytemplateparamid/', methods=['GET'])
def dataparameter_getlist_by_templateparamid():
    id = request.args.get("id", "", type=str)
    return DataParameterCommand().getlist_by_templateparamid(id)

@DataParameterController.route('/api/dataparameter/batchsave/', methods=['POST'])
def dataparameter_batchsave():
    return DataParameterCommand().batch_save(request.get_json())