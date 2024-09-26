from jinja2 import Environment, PackageLoader, DictLoader
class Jinja2Helper:
    templates = {}
    env = None

    # 添加模板
    def add(self, name, content):
        self.templates[name] = content

    # 添加并加载环境
    def add_load(self, name, content):
        self.templates[name] = content
        self.load()

    # 加载环境
    def load(self):
        loader = DictLoader(self.templates)
        self.env = Environment(loader=loader)

    # 渲染一个文件
    def render_one(self, name, params):
        template = self.env.get_template(name)
        return template.render(params)

    # 自动化渲染一个文件
    def auto_render_one(self, name, content, params):
        self.add_load(name, content)
        return self.render_one(name, params)
