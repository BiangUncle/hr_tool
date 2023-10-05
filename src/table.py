import json
from .colunm_resolver import *
from .constant import *
from .config import *
from .util import *
import pandas as pd

# 表基类
class Table:

    def __init__(self) -> None:
        self.header = 0
        self.columns = []
        self.sheet_name = Default_Sheet
        self.df = None
        self.file_name = ''
        self.file_name_prefix = ''
        self.output_config = {}
        self.biz_map = {}
        self.resolvers = []
        self.default_set_map = {}


    # 加载输入配置文件
    def load_config(self, config_name: str) -> dict:
        with open(config_name) as f:
            data = json.load(f)

        self.header = data[FieldName_Header]
        self.columns = data[FieldName_Columns]
        self.sheet_name = data[FieldName_Sheet_Name]
        self.file_name_prefix = data[FieldName_File_Name_Prefix]
        self.biz_map = data[FieldName_Biz_Map]

        print(f'load config success')
        return data
    
    # 加载输出配置文件
    def load_output_config(self, output_config_name: str) -> dict:
        with open(output_config_name) as f:
            data = json.load(f)

        self.output_config = data
        self.default_set_map = self.output_config[FieldName_Default_Set_Map]

        print(f'load output config success')
        return self.output_config

    def load_data(self, file_name: str):
        assert file_name != "", "文件名不能为空"
        assert self.columns != [], "请提前加载配置项"
        
        self.df = pd.read_excel(
            file_name,
            header=self.header,
            sheet_name=self.sheet_name
        )[self.columns]

        # print(self.df)

    def resolver_column(self, value):
        ret = value
        for resolver in self.resolvers:
            ret = resolver(ret)
        
        return ret

    def to_bo(self) -> pd.DataFrame:
        pass

# 加班表
class OverWorkTable(Table):

    def __init__(self, file_prefix: str) -> None:
        super().__init__()
        self.tran = {}
        self.file_prefix = file_prefix
        self.resolvers = [
            NameResolver,
        ]

    def load_config(self) -> dict:
        config = super().load_config(Config_File_Dir_Name + Input_File_Dir_Name + self.file_prefix + Input_Config_File_Name_Json)
        self.tran = config['tran']  # 业务转换map

    def load_output_config(self) -> dict:
        return super().load_output_config(Config_File_Dir_Name + Output_File_Dir_Name + Over_Work_File_Prefix + Output_Config_File_Name_Json)

    def to_bo(self) -> pd.DataFrame:
        bo = pd.DataFrame(columns=self.output_config[FieldName_Column])
        for idx, row in self.df.iterrows():
            newRow = {}
            for k, v in self.tran[Tran_Value_To_Value].items():
                if pd.isna(row[k]):
                    continue
                newRow[v] = self.resolver_column(row[k])

            typ = row[self.biz_map[OverWork_Type]]
            if typ in self.tran[Tran_Value_To_Number]:
                newRow[self.tran[Tran_Value_To_Number][typ]] = row[self.biz_map[OverWork_Count]]

            if len(newRow) == 0:
                continue
            
            bo = bo._append(newRow, ignore_index=True)
            # print(idx, row)
        default_set(bo, self.default_set_map)
        
        return bo
    
# 请假表
class AttendanceTable(Table):
    
    def __init__(self, file_prefix: str) -> None:
        super().__init__()
        self.file_prefix = file_prefix

    def load_config(self) -> dict:
        config = super().load_config(Config_File_Dir_Name + Input_File_Dir_Name + self.file_prefix + Input_Config_File_Name_Json)
        self.tran = config['tran']  # 业务转换map

    def load_output_config(self) -> dict:
        return super().load_output_config(Config_File_Dir_Name + Output_File_Dir_Name + Attendance_File_Prefix + Output_Config_File_Name_Json)
    
    def to_bo(self) -> pd.DataFrame:
        bo = pd.DataFrame(columns=self.output_config[FieldName_Column])
        for idx, row in self.df.iterrows():
            newRow = {}
            for k, v in self.tran[Tran_Value_To_Value].items():
                if pd.isna(row[k]):
                    continue
                newRow[v] = self.resolver_column(row[k])

            typ = row[self.biz_map[OverWork_Type]]
            if typ in self.tran[Tran_Value_To_Number]:
                v2n = self.tran[Tran_Value_To_Number][typ]

                newRow[v2n[Attendance_Holiday_Count]] = row[self.biz_map[Attendance_Count]]
                newRow[v2n[Attendance_Holiday_Detail]] = GetTime10Before(row[self.biz_map[Attendance_StartTime]]) + "-" + \
                GetTime10Before(row[self.biz_map[Attendance_EndTime]]) + ", " + f'{row[self.biz_map[Attendance_Count]]}' + "天"
            else:
                continue

            if len(newRow) == 0:
                continue
            
            bo = bo._append(newRow, ignore_index=True)
            # print(idx, row)
        default_set(bo, self.default_set_map)
        
        return bo


# 工厂模式，创建对应表的对象
def TableFactory(file_prefix: str) -> Table:
    if Attendance_File_Prefix in file_prefix:
        return AttendanceTable(file_prefix)
    elif Over_Work_File_Prefix in file_prefix:
        return OverWorkTable(file_prefix)
    else:
        assert False, "未知文件前缀"