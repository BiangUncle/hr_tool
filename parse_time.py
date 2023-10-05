from datetime import datetime
from datetime import timedelta
from chinese_calendar import is_workday

start = '2023-07-20 08:30:00'
end = '2023-07-20 17:30:00'

work_time_start = '08:30:00'
work_time_end = '17:30:00'

relax_time_start = '2023-07-20 12:00:00'
relax_time_end = '2023-07-20 13:00:00'

# 计算工作了多少个小时
def CountWorkHour(start, end):
    during = end - start
    work_hour = during.seconds / 60 / 60
    return work_hour


def MintusRelaxTime(start, end):

    rs = datetime.strptime(relax_time_start, '%Y-%m-%d %H:%M:%S')
    re = datetime.strptime(relax_time_end, '%Y-%m-%d %H:%M:%S')
    if start <= rs and end >= re:
        return 1.0
    
    return 0.0


def GetWorkDay(start, end):

    start_time = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')

    cur = start_time

    days = [cur]

    while cur.day != end_time.day:
        cur = cur + timedelta(days=1)
        # print(cur)
        if is_workday(cur):
            days.append(cur)
    # print(days)

    return days

def ConnetWordDay(days):
    if len(days) == 0:
        return []

    if len(days) == 1:
        return [days[0].strftime('%m.%d')]


    ret = []

    left = days[0].strftime('%m.%d')
    right = ''
    idx = 1
    while idx < len(days):
        if days[idx - 1].day + 1 == days[idx].day:
            right = days[idx].strftime('%m.%d')
            idx += 1
            continue
        else:
            if right == '':
                ret.append(left)
            else:
                ret.append(f'{left}-{right}')

            left = days[idx].strftime('%m.%d')
            right = ''
            idx += 1
            continue
    
    if right == '':
        ret.append(left)
    else:
        ret.append(f'{left}-{right}')
    
    return ret

def CountHoliday(start, end):
    days = GetWorkDay(start, end)
    print(days)
    ret = ConnetWordDay(days)
    print(ret)

    
    return ', '.join(ret) + f', {len(days)}天'

s = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
e = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')

work_hour = CountWorkHour(s, e)
relax_hour = MintusRelaxTime(s, e)
print(work_hour)
print(relax_hour)
print(work_hour - relax_hour)