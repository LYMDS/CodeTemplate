from flask import Flask
from flask_cors import CORS
from Controller.TemplateGroupController import *
from Controller.TemplateContentController import *

app = Flask(__name__)
CORS(app, resources=r'/*')

app.register_blueprint(TemplateGroupController)
app.register_blueprint(TemplateContentController)


app.debug = True
app.run(host='127.0.0.1', port=8008)