import pandas as pd
from chinese_calendar import *
from parse_time import *
from table import Table

attendance_filter_columns = ['申请人', '休假类别', '休假时长', '开始时间', '结束时间', '休假说明']


# output = pd.DataFrame(columns=['公司','姓名', '社会工龄', '年假', '年假天数', '调休（时）', '调休（时）天数', '其他'])
output = pd.DataFrame(columns=['公司','姓名', '社会工龄', '扣薪病假', '病假天数', '事假', '事假天数', '其他', '婚假天数', '丧假天数', '产假天数', '备注'])

def CreateOutputDataFrame() -> pd.DataFrame:
    output = pd.DataFrame(columns=['公司','姓名', '社会工龄', '扣薪病假', '病假天数', '事假', '事假天数', '其他', '婚假天数', '丧假天数', '产假天数', '备注'])
    return output


def FilterDestColumns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.loc[:, ['申请人', '休假类别', '休假时长', '开始时间', '结束时间', '休假说明']]
    return df

# 提取需要的数据列
df = pd.read_excel('attendance record.xlsx')
df = df.loc[:, ['申请人', '休假类别', '休假时长', '开始时间', '结束时间', '休假说明']]

count = {}

holiday_map = {
    '年假': '年假',
    '病假': '病假',
    '事假': '事假',
    '调休（时）': '调休',
}

def CountYearHoliday():
    for index, row in df.iterrows():

        if row['申请人'] not in count:
            count[row['申请人']] = {
                '年假时间': 0,
                '调休时间': 0,
            }
        
        cur_people = count[row['申请人']]

        if row['休假类别'] not in cur_people:
            cur_people[row['休假类别']] = []

        days = GetWorkDay(row['开始时间'], row['结束时间'])    
        cur_people[row['休假类别']] += days

        if row['休假类别'] == '年假':
            cur_people['年假时间'] += row['休假时长']
        elif row['休假类别'] == '调休（时）':
            cur_people['调休时间'] += row['休假时长']
        


    for name, holidays in count.items():
        newRows = {
            '公司': 'CHSZ',
            '姓名': name, 
            '社会工龄': '',
            '年假': '',
            '年假天数': holidays['年假时间'],
            '调休（时）': '',
            '调休（时）天数': holidays['调休时间'],
            '其他': '',
        }

        if '年假' in holidays:
            ret = ConnetWordDay(holidays['年假'])
            count = len(holidays['年假'])
            newRows['年假'] = ', '.join(ret) + f', {holidays["年假时间"]}天'
            # newRows['年假天数'] += count
        
        if '调休（时）' in holidays:
            ret = ConnetWordDay(holidays['调休（时）'])
            count = len(holidays['调休（时）'])
            newRows['调休（时）'] = ', '.join(ret) + f', {holidays["调休时间"]}时'
            # newRows['调休（时）天数'] += count

        output = output._append(newRows, ignore_index=True)

    print(output)

def CountUnPayHoliday():

    for index, row in df.iterrows():

        if row['休假类别'] != '病假' and row['休假类别'] != '事假':
            continue


        if row['申请人'] not in count:
            count[row['申请人']] = {
                '事假时间': 0,
                '病假时间': 0,
                '产检假时间': 0,
            }
        
        cur_people = count[row['申请人']]
        
        
        if row['休假类别'] not in cur_people:
            cur_people[row['休假类别']] = []

        days = GetWorkDay(row['开始时间'], row['结束时间'])    
        cur_people[row['休假类别']] += days

        if row['休假类别'] == '病假':
            cur_people['病假时间'] += row['休假时长']
        elif row['休假类别'] == '事假':
            cur_people['事假时间'] += row['休假时长']
        elif row['产检假']:
            cur_people['产检假时间'] += row['休假时长']
        

    for name, holidays in count.items():
        newRows = {
            '公司': 'CHSZ',
            '姓名': name, 
            '社会工龄': '',
            '扣薪病假': '',
            '病假天数': holidays['病假时间'],
            '事假': '',
            '事假天数': holidays['事假时间'],
            '其他': '',
            '婚假天数': '',
            '丧假天数': '', 
            '产假天数': '',
            '备注': '', 
        }

        if '病假' in holidays:
            ret = ConnetWordDay(holidays['病假'])
            print(ret)
            count = len(holidays['病假'])
            newRows['扣薪病假'] = ', '.join(ret) + f', {holidays["病假时间"]}天'
            # newRows['病假'] += count
        
        if '事假' in holidays:
            ret = ConnetWordDay(holidays['事假'])
            count = len(holidays['事假'])
            newRows['事假'] = ', '.join(ret) + f', {holidays["事假时间"]}天'
            # newRows['调休（时）天数'] += count

        if newRows['病假天数'] == 0 and newRows['事假天数'] == 0:
            continue

        output = output._append(newRows, ignore_index=True)


    output.to_excel('attendance_output.xlsx')

def CreateTable(file_name):
    xlsx = pd.ExcelFile(file_name)
    table = Table(file_name, attendance_filter_columns)
    table.df = pd.read_excel(xlsx, table.sheet_name, header=table.header)
    return table


def Run():
    tbl = CreateTable('attendance record.xlsx')
    CountUnPayHoliday(tbl.df)

Run()