
"""
本模块用于计算公司员工薪水
"""

company = '北京尚学堂'


def yearSalary(monthSalary):
    """根据传入的月薪的值，计算出年薪：monthSalary*12"""
    return monthSalary * 12


def daySalary(monthSalary):
    """根据传入的月薪，计算出一天的薪资，一个月按照22.5天来计算（国家规定工作日）"""
    pass


# 测试模块
if __name__ == "__main__":
    print(yearSalary(5000))









