from flask import Flask
from flask_cors import CORS
from Controller.TemplateGroupController import *
from Controller.TemplateContentController import *
from Controller.TemplateParamController import *
from Controller.TemplateRenderController import *
from Controller.AttachmentController import *
from Controller.VueController import *
from Controller.FilterController import *

app = Flask(__name__)
CORS(app, resources=r'/*')

app.register_blueprint(TemplateGroupController)
app.register_blueprint(TemplateContentController)
app.register_blueprint(TemplateParamController)
app.register_blueprint(TemplateRenderController)
app.register_blueprint(AttachmentController)
app.register_blueprint(IndexController)
app.register_blueprint(AssetsController)
app.register_blueprint(FilterController)

app.debug = True
app.run(host='localhost', port=8008)