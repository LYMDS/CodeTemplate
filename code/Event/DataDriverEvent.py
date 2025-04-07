from sqlalchemy import event
from Models.DataDriver import DataDriver
from Common.DriverParamInitBase import DirverParamInitBase
from DataDriver.DriverParam import TemplateParamGuide_DriverParamInit
from Command.DataParameterCommand import DataParameterCommand
from sqlalchemy.orm import Session


@event.listens_for(DataDriver, "after_insert")
def after_insert(mapper, connection, target):
    print("DataDriver event_after_insert")
    session = Session(bind=connection)
    driver_param_init = DirverParamInitBase.get_driver_param_init("Template Param Data Guide",target.type)(session)
    driver_param_init.CreateBaseParam(target.datadriverid)


@event.listens_for(DataDriver, "before_delete")
def before_delete(mapper, connection, target):
    print("DataDriver event_before_delete")
    session = Session(bind=connection)
    command = DataParameterCommand()
    command.DataServer.session = session
    DataParameterList = command._getlist_by_datadriverid(target.datadriverid)
    command.delete([data.dataparameterid for data in DataParameterList])


