import xlrd
from Common.DriverBase import DirverBase

class DriverExcel(DirverBase):
    DriverName = "Excel"
    DriverDescribe = "Excel文件数据驱动"
    DriverParams = None
    
    xlsx_path = ''
    sheet_name = 'Sheet1'

    # 初始化参数
    def init_attributes(self):
        self.xlsx_path = self.DriverParams["xlsx_path"]
        sheet_name = self.DriverParams["sheet_name"]
        if sheet_name not in (None, ""):
            self.sheet_name = sheet_name

    def execute(self):
        self.init_attributes()
        
        # 打开Excel文件和工作表
        self.wb = xlrd.open_workbook(self.xlsx_path)
        self.sheet = self.wb.sheet_by_name(self.sheet_name)
        
        # 获取表头和数据
        headers = self.sheet.row_values(0)
        data = []
        
        for r_index in range(1, self.sheet.nrows):
            row_data = self.sheet.row_values(r_index)
            # 将行数据与表头组合成字典
            data.append(dict(zip(headers, row_data)))
            
        return data