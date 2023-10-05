# 配置文件
Config_File_Dir_Name = "config/"
Input_File_Dir_Name = "input/"
Output_File_Dir_Name = "output/"


# 文件前缀
Over_Work_File_Prefix = "over_work_"
Attendance_File_Prefix = "attendance_"
Trans_File_Prefix = "trans_"
Sys_File_Prefix = "sys_"

# 任务文件配置
Over_Work_Mission_File_Prefix = [
    Trans_File_Prefix + Over_Work_File_Prefix,
    Sys_File_Prefix + Over_Work_File_Prefix
]

# 请假任务文件配置
Attendance_Mission_File_Prefix = [
    Trans_File_Prefix + Attendance_File_Prefix,
    Sys_File_Prefix + Attendance_File_Prefix
]

# 运输部门加班表
Trans_OverWork_Config_File_Name = "trans_over_work_config.json"
# 系统导出加班表
Sys_OverWork_Config_File_Name = "sys_over_work_config.json"


# 目标表配置
Default_Sheet = "Sheet0"

# 加班映射
overWorkMap = {
    "日常加班": "平时加班",
    "法定假加班": "节假日加班",
    "班前班后加班": "平时加班",
    "班后加班": "平时加班",
    "周未加班": "休息日加班",
    "平时加班": "平时加班",
}
