from flask import Blueprint,Flask,request

IndexController = Blueprint('IndexController', __name__, static_folder="..\Publish")
AssetsController = Blueprint('AssetsController', __name__, static_folder="..\Publish\\assets")

@IndexController.route('/')
def index():
    return IndexController.send_static_file('index.html')

@IndexController.route('/<path:fallback>')
def fallback(fallback):       # Vue Router 的 mode 为 'hash' 时可移除该方法
    # if fallback.startswith('css/') or fallback.startswith('js/')\
    #         or fallback.startswith('img/') or fallback == 'favicon.ico':
    #     return IndexController.send_static_file(fallback)
    # else:
    return IndexController.send_static_file('index.html')

# @AssetsController.route('/assets/<path:filename>')
# def assets(filename):
#     return AssetsController.send_static_file('assets/' + filename)




