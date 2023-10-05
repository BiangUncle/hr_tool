import pandas as pd
from util import *
import os

sheet_name_map = {

}

typeMap = {
    "日常加班": "平时加班",
    "法定假加班": "节假日加班",
    "班前班后加班": "平时加班",
    "班后加班": "平时加班",
    "周未加班": "休息日加班",
    "周末加班": "休息日加班",
    "平时加班": "平时加班",
    "法定假加班": "节假日加班"
}

default_columns = ['姓名', '班后/周末/法定假加班', '时长：H']

class Table:

    def __init__(self, file_name) -> None:
        self.header = 0
        self.filter_columns = default_columns
        self.sheet_name = 'Sheet0'
        self.df = None
        self.file_name = file_name

def CreateOutputDataFrame() -> pd.DataFrame:
    output = pd.DataFrame(columns=['员工姓名','平时加班', '休息日加班', '节假日加班'])
    return output

def FilterDestColumns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.loc[:, ['姓名', '班后/周末/法定假加班', '时长：H']]
    df['时长：H'] = df['时长：H'].astype(float)
    return df

output = CreateOutputDataFrame()

def CountOverWorkDay(df):
    global output

    count = {}
    print(df)
    df = FilterDestColumns(df)

    agg = df.groupby(by=['姓名', '班后/周末/法定假加班']).agg({'时长：H': 'sum'})
    dic = agg.to_dict()

    temp = {}

    for k, v in dic['时长：H'].items():

        if k[0] not in temp:
            temp[k[0]] = {
                '员工姓名': DeleteNameSurfix(k[0]),
                '平时加班': 0, 
                '休息日加班': 0,
                '节假日加班': 0
            }

        cur = temp[k[0].replace(' ', '')]
        cur[typeMap[k[1].replace(' ', '')]] = v

    for k, v in temp.items():
        output = output._append(v, ignore_index=True)  

def Output():
    global output
    output.to_excel('output_overwork.xlsx')

def SheetName():
    xlsx = pd.ExcelFile('test2.xlsx')
    print(xlsx.sheet_names)

def SelectSheetName(sheet_names) -> str:
    if '合丹主体加班表' in sheet_names:
        return '合丹主体加班表'
    return 'Sheet0'

def CreateTable(file_name):

    xlsx = pd.ExcelFile(file_name)
    table = Table(file_name)
    print(xlsx.sheet_names)
    table.sheet_name = 'Sheet0'
    table.header = 0
    # if '合丹主体加班表' in xlsx.sheet_names:
    #     table.header = 1
    #     table.sheet_name = '合丹主体加班表'
        
    table.df = pd.read_excel(xlsx, table.sheet_name, header=table.header)
    if '班后/周末/法定假加班' in table.df.columns:
        table.filter_columns = ['加班员工', '班后/周末/法定假加班', '时长：H']

    return table

def LoadDestSheet():
    xlsx = pd.ExcelFile('test2.xlsx')
    sheet_name = SelectSheetName(xlsx.sheet_names)
    df = pd.read_excel(xlsx, sheet_name, header=1)
    return df

def Run():

    dirs = os.listdir('over_work_apply')

    for file in dirs:
        # if file == '2023.8.18-2023.9.18康德乐-加班转计薪.xlsx':
        #     continue
        table = CreateTable('over_work_apply/' + file)
        CountOverWorkDay(table.df)
    Output()

Run()