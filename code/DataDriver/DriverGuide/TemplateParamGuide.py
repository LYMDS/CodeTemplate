from Common.GuideBase import GuideBase
from Command.DataParameterCommand import *
class TemplateParamGuide(GuideBase):

    GuideName = "Template Param Data Guide"
    GuideDescribe = "基于模板参数的数据引导"

    def get(self, datadriverid, templateparamid):
        dpc = DataParameterCommand()
        baseParams = dpc._getlist_by_datadriverid(datadriverid)
        execParams = dpc._getlist_by_templateparamid(templateparamid)
        return {p.name:p.value for p in [*baseParams, *execParams]}