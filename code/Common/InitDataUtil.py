from Common.DataUtil import *
class InitDataUtil:
    def __init__(self):
        self.DataServer = DataUtil()
        self.DataServer.get_session()