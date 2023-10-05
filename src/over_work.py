import pandas as pd
from util import *

typeMap = {
    "日常加班": "平时加班",
    "周未加班": "休息日加班",
    "法定假加班": "节假日加班",
}

class OW_sys():

    def __init__(self, file_name: str) -> None:
        self.header = 0
        self.filter_columns = ['加班员工', '加班类别', '复核加班小时数']
        self.sheet_name = 'Sheet0'
        self.df = None
        self.file_name = file_name

    def FilterDestColumns(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.loc[:, self.filter_columns]
        df['复核加班小时数'] = df['复核加班小时数'].astype(float)
        return df

    def CountOverWorkDay(self, output):

        df = self.FilterDestColumns(df)

        agg = df.groupby(by=['姓名', '加班类别']).agg({'复核加班小时数': 'sum'})
        dic = agg.to_dict()

        temp = {}

        for k, v in dic['复核加班小时数'].items():

            if k[0] not in temp:
                temp[k[0]] = {
                    '员工姓名': DeleteNameSurfix(k[0]),
                    '平时加班': 0, 
                    '休息日加班': 0,
                    '节假日加班': 0
                }

            cur = temp[k[0]]
            cur[typeMap[k[1]]] = v

        for k, v in temp.items():
            output = output._append(v, ignore_index=True)  