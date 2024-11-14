from jinja2 import Environment, PackageLoader, DictLoader

from Command.FilterCommand import FilterCommand
from Common.Extensions.CustomVariableExtension import CustomVariableExtension
from Common.Extensions.StyledExpressionExtension import StyledExpressionExtension
from jinja2.nodes import TemplateData, Template, Output, For, Name, Getitem, Getattr
import sys

class Jinja2Helper:
    templates = {}
    env = None

    #region preview样式参数
    StyleNamePrefix = "<span style='color: red'>"
    StyleNamePostfix = "</span>"
    StyleGetitemPrefix = "<span style='color: green'>"
    StyleGetitemPostfix = "</span>"
    StyleGetattrPrefix = "<span style='color: green'>"
    StyleGetattrPostfix = "</span>"
    StyleForPrefix = "<div style='border-radius: 16px;border: 1px dashed red;padding: 16px;background: #ccc'>"
    StyleForPostfix = "</div>"
    StyleIterPreFix = "<div style='background: cornsilk'>"
    StyleIterPostFix = "</div>"
    #endregion

    # 添加模板
    def add(self, name, content):
        self.templates[name] = content

    # 添加并加载环境
    def add_load(self, name, content):
        self.templates[name] = content
        self.load()
        self.load_filter()

    # 加载环境
    def load(self):
        loader = DictLoader(self.templates)
        self.env = Environment(loader=loader)

    # 加载自定义拓展环境
    def load_with_extensions(self):
        loader = DictLoader(self.templates)
        self.env = Environment(loader=loader, extensions=[StyledExpressionExtension,CustomVariableExtension])

    # 渲染一个文件
    def render_one(self, name, params):
        template = self.env.get_template(name)
        return template.render(params)

    # 自动化渲染一个文件
    def auto_render_one(self, name, content, params):
        self.add_load(name, content)
        return self.render_one(name, params)

    # 获取模板
    def get_template(self, name):
        template_source = self.templates[name]
        filename = "<template>"
        globals = {}
        source = self.env.parse(template_source, name, filename)
        source = self.env._generate(source, name, filename)
        code = self.env._compile(source, filename)
        return self.env.template_class.from_code(self.env, code, globals)

    # 获取模板
    def get_template_from_source(self, name, source):
        filename = "<template>"
        globals = {}
        source = self.env._generate(source, name, filename)
        code = self.env._compile(source, filename)
        return self.env.template_class.from_code(self.env, code, globals)

    # 解析模板
    def parse(self, name):
        template_source = self.templates[name]
        filename = "<template>"
        source = self.env.parse(template_source, name, filename)
        return source

    # 添加模板样式
    def add_style_for_preview(self, template):
        if not isinstance(template, Template):
            raise ValueError("template must be class Template")
        for i in range(len(template.body)):
            self.add_style_for_nodes(template.body, i)
        return template

    # 添加node样式
    def add_style_for_nodes(self, nodes, i):
        node = nodes[i]
        if isinstance(node, Output):
            pass
        elif isinstance(node, For):
            o = Output()
            t_s = TemplateData()
            t_s.data = f"{self.StyleForPrefix}{self.StyleIterPreFix}循环 {node.target.name} 从 {node.iter.name}{self.StyleIterPostFix}"
            o.nodes = []
            o.nodes.append(t_s)
            for b in node.body:
                o.nodes = o.nodes + b.nodes
            t_e = TemplateData()
            t_e.data = f"{self.StyleForPostfix}"
            o.nodes.append(t_e)
            nodes[i] = o
        elif isinstance(node, Name):
            t = TemplateData()
            t.data = f"{self.StyleNamePrefix}{node.name}{self.StyleNamePostfix}"
            t.lineno = node.lineno
            nodes[i] = t
        elif isinstance(node, TemplateData):
            pass
        elif isinstance(node, Getitem):
            t = TemplateData()
            t.data = f"{self.StyleGetitemPrefix}{node.node.name}['{node.arg.value}']{self.StyleGetitemPostfix}"
            t.lineno = node.lineno
            nodes[i] = t
        elif isinstance(node, Getattr):
            t = TemplateData()
            t.data = f"{self.StyleGetattrPrefix}{node.node.name}.{node.attr}{self.StyleGetattrPostfix}"
            t.lineno = node.lineno
            nodes[i] = t
        if hasattr(nodes[i], "nodes"):
            for j in range(len(nodes[i].nodes)):
                self.add_style_for_nodes(nodes[i].nodes, j)

    # 加载过滤器
    def load_filter(self):
        list = FilterCommand().getlist("")
        for data in list:
            exec(data.new_func)
            self.env.filters[data.new_name] = getattr(sys.modules[__name__], data.new_name)












