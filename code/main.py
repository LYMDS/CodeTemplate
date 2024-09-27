from flask import Flask
from flask_cors import CORS
from Controller.TemplateGroupController import *
from Controller.TemplateContentController import *
from Controller.TemplateParamController import *
from Controller.TemplateRenderController import *
from Controller.AttachmentController import *

app = Flask(__name__)
CORS(app, resources=r'/*')

app.register_blueprint(TemplateGroupController)
app.register_blueprint(TemplateContentController)
app.register_blueprint(TemplateParamController)
app.register_blueprint(TemplateRenderController)
app.register_blueprint(AttachmentController)


app.debug = True
app.run(host='127.0.0.1', port=8008)