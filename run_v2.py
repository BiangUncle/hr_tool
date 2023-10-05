from src.table import *
from src.config import *
from src.constant import *
import os


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


RunAttendance("./files/")