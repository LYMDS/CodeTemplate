from flask import Blueprint,request
from Command.AttachmentCommand import *

AttachmentController = Blueprint('AttachmentController', __name__)

@AttachmentController.route('/api/new_attachment/getattachmentbyid/', methods=['GET'])
def new_attachment_getattachmentbyid():
    id = request.args.get("id", "", type=str)
    return AttachmentCommand().get(id)

@AttachmentController.route('/api/new_attachment/upload/', methods=['POST'])
def new_attachment_upload():
    file = request.files.get("file")
    return AttachmentCommand().upload(file)

@AttachmentController.route('/api/new_attachment/download/', methods=['GET'])
def new_attachment_download():
    id = request.args.get("id", "", type=str)
    return AttachmentCommand().download(id)