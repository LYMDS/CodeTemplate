from sqlalchemy import event
from Models.new_template_param import new_template_param
from Common.DriverParamInitBase import DirverParamInitBase
from DataDriver.DriverParam import TemplateParamGuide_DriverParamInit
from Command.DataDriverCommand import DataDriverCommand
from Command.DataParameterCommand import DataParameterCommand
from sqlalchemy.orm import Session


@event.listens_for(new_template_param.new_datadriver_id, 'set')
def new_datadriver_id_set(target, value, oldvalue, initiator):
    session = Session.object_session(target)
    dataparameter_command = DataParameterCommand()
    dataparameter_command.DataServer.session = session
    need_delete = dataparameter_command._getlist_by_templateparamid(target.new_template_paramid)

    if value != oldvalue and need_delete != None and len(need_delete) > 0:
        dataparameter_command._delete([d.dataparameterid for d in need_delete])

    if value != "" and value != oldvalue:
        datadriver_command = DataDriverCommand()
        datadriver_command.DataServer.session = session
        datadriver = datadriver_command._get(value)
        driver_param_init = DirverParamInitBase.get_driver_param_init("Template Param Data Guide", datadriver.type)(session)
        driver_param_init.CreateExecParam(value, target.new_template_paramid)