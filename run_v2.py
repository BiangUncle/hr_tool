from src.table import *
from src.config import *
from src.constant import *
import os
import sys


def RunAttendance(root='./'):

    dirs = os.listdir(root)

    output = None

    for file in dirs:
        prefix = ContainFilePrefix(file, Attendance_Mission_File_Prefix)
        if prefix == '':
            continue

        t = TableFactory(prefix)
        t.load_config()
        t.load_output_config()
        t.load_data(root + file)
        bo = t.to_bo()

        if output is None:
            output = bo
        else:
            output = pd.concat([output, bo], axis=0)

    # output = output.groupby(Employee_Name).sum()
    output.to_excel("./output/attendance.xlsx")


def RunOverWork(root='./'):

    dirs = os.listdir(root)
    output = None

    for file in dirs:
        prefix = ContainFilePrefix(file, Over_Work_Mission_File_Prefix)
        if prefix == '':
            continue

        t = TableFactory(prefix)
        t.load_config()
        t.load_output_config()
        t.load_data(root + file)
        bo = t.to_bo()

        if output is None:
            output = bo
        else:
            output = pd.concat([output, bo], axis=0)

    # output = output.groupby(Employee_Name).sum()
    output.to_excel("./output/over_work.xlsx")



def Run():
    args = sys.argv
    if len(args) != 3 and len(args) != 2:
        assert False, "参数传递错误"

    mission = args[1]
    root = './'
    if len(args) == 3:
        root = args[2]

    if mission == "att":
        RunAttendance(root)
    elif mission == "ow":
        RunOverWork("./files/")
    else:
        assert False, "错误的参数"

Run()