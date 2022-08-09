# coding=utf-8
# by spenly

import copy


# 获取分配任务后任务数量的平均值
def avgOfList(taskNumList, dis_taskNum):
    _sum = dis_taskNum
    for num in taskNumList:
        _sum = _sum + num
    if (len(taskNumList) > 0):
        return _sum / len(taskNumList)
    else:
        return 0


def getMinLine(taskNumList, desc_taskNumList, avg, dis_taskNum):  # 计算分配后的最小数量
    if (len(taskNumList) == 0 or dis_taskNum == 0):  # 参数检查
        return 0
    print('###############')
    print(taskNumList)
    print("avg", avg)
    print(desc_taskNumList)
    print('---------------')

    flag = True  # 是否已经得到了MinLine
    for num in desc_taskNumList:  # check是否已经得到了目标数值MinLine
        if (num >= avg):
            flag = False
            break
    if (flag):  # 如果得到了就返回
        return avg
    else:  # 否则重新计算avg
        _sum = dis_taskNum  # 任务数和
        _count = 0  # 符合要求的机器数
        c_stn = copy.copy(desc_taskNumList)  # 建立副本
        for item in c_stn:
            if item < avg:
                _sum = _sum + item
                _count = _count + 1
            else:
                desc_taskNumList.remove(item)
        print("sum", _sum, "count", _count)

        if (_count > 0):
            avg = _sum / _count
        else:
            return avg
        print("avg", avg)
        return getMinLine(taskNumList, desc_taskNumList, avg, dis_taskNum)


# 获得分配后的任务数
def getAvgNumAfDstb(taskNum, disNum):
    d_tn = sorted(taskNum, reverse=True)  # 降序排序后的 list
    avg = avgOfList(taskNum, disNum)
    return getMinLine(taskNum, d_tn, avg, disNum)
