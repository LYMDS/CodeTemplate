from Common.InitDataUtil import *
from sqlalchemy import or_
from Models.new_attachment import *
import json
from objtyping import to_primitive
from flask import Response,send_file
import io



class AttachmentCommand(InitDataUtil):
    def get(self, id):
        data = self.DataServer.session.get(new_attachment, id)
        return json.dumps(to_primitive(data))

    def get_content(self, id):
        data = self.DataServer.session.get(new_attachment, id)
        return data.new_content

    def upload(self, file):

        filename = file.filename
        content_type = file.content_type
        mime_type = file.mimetype
        file_bytes = file.read()


        saveTable = new_attachment()
        self.DataServer.session.add(saveTable)

        saveTable.new_name = filename
        saveTable.new_content = file_bytes
        saveTable.new_content_type = content_type
        saveTable.new_mime_type = mime_type

        self.DataServer.session.commit()
        id = saveTable.new_attachmentid
        self.DataServer.session.close()
        return id

    def download(self, id):
        data = self.DataServer.session.get(new_attachment, id)
        bytes_io = io.BytesIO(data.new_content)
        filename = data.new_name
        return send_file(bytes_io, download_name=filename, mimetype=data.new_mime_type, as_attachment=True)
