from Common.DataUtil import *

from Models.DataDriver import DataDriver
from Models.DataParameter import DataParameter
from Models.new_attachment import new_attachment
from Models.new_filter import new_filter
from Models.new_template_content import new_template_content
from Models.new_template_group import new_template_group
from Models.new_template_param import new_template_param
from Models.Base import Base

du = DataUtil()
Base.metadata.create_all(du.engine)
