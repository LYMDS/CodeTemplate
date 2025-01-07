from jinja2 import Environment, PackageLoader, DictLoader
from Command.FilterCommand import FilterCommand
from Common.Extensions.CustomVariableExtension import CustomVariableExtension
from Common.Extensions.StyledExpressionExtension import StyledExpressionExtension
from jinja2.nodes import (TemplateData, Template, Output, For, If, Name, Getitem, Getattr, Filter,
                          Compare, And, Or, Operand, Const)
from jinja2.compiler import operators

class Jinja2Helper:
    templates = {}
    env = None
    filterGlobals = {}

    #region preview样式参数
    StyleNamePrefix = "<span style='color: red'>"
    StyleNamePostfix = "</span>"
    StyleGetitemPrefix = "<span style='color: green'>"
    StyleGetitemPostfix = "</span>"
    StyleGetattrPrefix = "<span style='color: green'>"
    StyleGetattrPostfix = "</span>"
    StyleForPrefix = "<div style='border-radius: 16px;border: 2px dashed #6f7178;padding: 16px;background: #a4f7aa;'>"
    StyleForPostfix = "</div>"
    StyleIterPreFix = "<div style='background: #bfc3ef;border-radius: 10px;padding: 6px;color: white;'>"
    StyleIterPostFix = "</div>"
    StyleFilterPrefix = "<span style='color: yellow'>"
    StyleFilterPostfix = "</span>"
    StyleIfPrefix = "<div style='border-radius: 16px;border: 2px dashed #6f7178;padding: 16px;background: #faffe4;margin-top: 5px;margin-bottom: 5px;'>"
    StyleIfPostfix = "</div>"
    StyleIfBodyPrefix = "<div style='background: #bee8eb;border-radius: 10px;padding: 6px;'>"
    StyleIfBodyPostfix = "</div>"
    #endregion

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
        self.load_filter()

    # 加载环境
    def load_without_filter(self):
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
            #self.add_style_for_nodes(template.body, i)
            template.body[i] = self.add_style_for_node(template.body[i])
        return template

    # 添加node样式
    def add_style_for_node(self, node):
        if isinstance(node, Output):
            pass
        elif isinstance(node, Filter):
            node = self.set_templatedata(f"{self.StyleNamePrefix}{node.node.name}{self.StyleNamePostfix}|{self.StyleFilterPrefix}{node.name}{self.StyleFilterPostfix}")
        elif isinstance(node, For):
            o = Output()
            o.nodes = []
            o.nodes.append(self.set_templatedata(f"{self.StyleForPrefix}{self.StyleIterPreFix}循环"))
            o.nodes.append(node.target)
            o.nodes.append(self.set_templatedata("从"))
            o.nodes.append(node.iter)
            if hasattr(node, "body"):  # 递归处理body
                for j in range(len(node.body)):
                    node.body[j] = self.add_style_for_node(node.body[j])
                    if hasattr(node.body[j], "nodes"):
                        o.nodes = o.nodes + node.body[j].nodes
            o.nodes.append(self.set_templatedata(f"{self.StyleIterPostFix}{self.StyleForPostfix}"))
            node = o
        elif isinstance(node, If):
            o = Output()
            o.nodes = []
            o.nodes.append(self.set_templatedata(f"{self.StyleIfPrefix}If "))
            test = self.add_style_for_node(node.test)
            o.nodes += test.nodes
            o.nodes.append(self.set_templatedata(f"{self.StyleIfBodyPrefix}"))
            if hasattr(node, "body"):  # 递归处理body
                for j in range(len(node.body)):
                    node.body[j] = self.add_style_for_node(node.body[j])
                    if hasattr(node.body[j], "nodes"):
                        o.nodes = o.nodes + node.body[j].nodes
            o.nodes.append(self.set_templatedata(f"{self.StyleIfBodyPostfix}"))

            if len(node.elif_) > 0:
                for j in range(len(node.elif_)):
                    #o.nodes.append(self.set_templatedata(f"{self.StyleIfBodyPrefix}否则"))
                    node.elif_[j] = self.add_style_for_node(node.elif_[j])
                    if hasattr(node.elif_[j], "nodes"):
                        o.nodes = o.nodes + node.elif_[j].nodes
                    #o.nodes.append(self.set_templatedata(f"{self.StyleIfBodyPostfix}"))


            if len(node.else_) > 0:
                o.nodes.append(self.set_templatedata("else"))
                o.nodes.append(self.set_templatedata(f"{self.StyleIfBodyPrefix}"))
                for j in range(len(node.else_)):
                    node.else_[j] = self.add_style_for_node(node.else_[j])
                    if hasattr(node.else_[j], "nodes"):
                        o.nodes = o.nodes + node.else_[j].nodes
                o.nodes.append(self.set_templatedata(f"{self.StyleIfBodyPostfix}"))

            o.nodes.append(self.set_templatedata(self.StyleIfPostfix))

            node = o
        elif isinstance(node, Compare):
            o = Output()
            o.nodes = []
            o.nodes.append(self.add_style_for_node(node.expr))
            if len(node.ops) > 0:
                for j in range(len(node.ops)):
                    ops = self.add_style_for_node(node.ops[j])
                    o.nodes += ops.nodes
            node = o
        elif isinstance(node, Operand):
            o = Output()
            o.nodes = []
            o.nodes.append(self.show_Operand(node))
            o.nodes.append(node.expr)
            node = o
        elif isinstance(node, Const):
            node = self.set_templatedata(f"{node.value}")
        elif isinstance(node, And):
            o = Output()
            o.nodes = []
            left = self.add_style_for_node(node.left)
            o.nodes += left.nodes
            o.nodes.append(self.set_templatedata(" AND "))
            right = self.add_style_for_node(node.right)
            o.nodes += right.nodes
            node = o
        elif isinstance(node, Or):
            o = Output()
            o.nodes = []
            left = self.add_style_for_node(node.left)
            o.nodes += left.nodes
            o.nodes.append(self.set_templatedata(" OR "))
            right = self.add_style_for_node(node.right)
            o.nodes += right.nodes
            node = o
        elif isinstance(node, Name):
            node = self.set_templatedata(f"{self.StyleNamePrefix}{node.name}{self.StyleNamePostfix}")
        elif isinstance(node, TemplateData):
            pass
        elif isinstance(node, Getitem):
            node = self.set_templatedata(f"{self.StyleGetitemPrefix}{node.node.name}['{node.arg.value}']{self.StyleGetitemPostfix}")
        elif isinstance(node, Getattr):
            node = self.set_templatedata(f"{self.StyleGetattrPrefix}{node.node.name}.{node.attr}{self.StyleGetattrPostfix}")
        if hasattr(node, "nodes"): # 递归处理Nodes
            for j in range(len(node.nodes)):
                node.nodes[j] = self.add_style_for_node(node.nodes[j])
        return node

    # 加载过滤器
    def load_filter(self):
        list = FilterCommand().get_all_list()
        for data in list:
            exec(data.new_func, locals(), self.filterGlobals)
            self.env.filters[data.new_name] = self.filterGlobals[data.new_name]

    # 生成文本数据
    def set_templatedata(self, s):
        t = TemplateData()
        t.data = s
        return t

    # 显示操作符
    def show_Operand(self, node):
        return self.set_templatedata(f" {operators[node.op]} ")













