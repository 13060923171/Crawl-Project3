import pandas as pd
import string
import numpy as np
df = pd.read_excel('../51_91.xlsx')
df1 = df.drop_duplicates(keep='first')


def chuli_city(x):
    x = str(x)
    x = x.split(',')
    x = x[0]
    x = x.replace("'","").replace("[","").replace("]","")
    return x

df1['place'] = df1['place'].apply(chuli_city)
df1 = df1.drop(['num','Unnamed: 0'],axis=1)


def chuli_fullcontent(x):
    def str_count(str):
        count_en = count_dg = count_sp = count_zh = count_pu = 0
        for s in str:
            if s in string.ascii_letters:
                count_en += 1
            elif s.isdigit():
                count_dg += 1
            elif s.isspace():
                count_sp += 1
            elif s.isalpha():
                count_zh += 1
            else:
                count_pu += 1
        return count_zh
    x = str(x)
    x1 = x.replace('_x000D_\n','').replace(' ','').strip(' ;')
    x1 = x1.replace(' ','')
    count = str_count(x1)
    if count >= 10:
        return x1
    else:
        return np.NAN


def city_type(x):
    if '北京' in x or '深圳' in x or '广州' in x or '上海' in x:
        return '一线城市'
    if '天津' in x or '成都' in x or '南京' in x or '西安' in x or '重庆' in x or '长沙' in x or '杭州' in x or '武汉' in x or '苏州' in x or '合肥' in x or '沈阳' in x or '青岛' in x or '郑州' in x or '东莞' in x or '佛山' in x:
        return '新一线城市'
    if '合肥' in x or '福州' in x or '泉州' in x or '厦门' in x or '兰州' in x or '贵阳' in x or '珠海' in x or '惠州' in x or '中山' in x or '南宁' in x or '石家庄' in x or '哈尔滨' in x or '长春' in x or '常州' in x or '南通' in x or '无锡' in x or '徐州' in x or '南昌' in x or '大连' in x or '潍坊' in x or '济南' in x or '临沂' in x or '烟台' in x:
        return '二线城市'
    if '太原' in x or '昆明' in x or '嘉兴' in x or '金华' in x or '绍兴' in x or '台州' in x or '温州' in x:
        return '二线城市'
    else:
        return '其他城市'

df1['fullcontent'] = df1['fullcontent'].apply(chuli_fullcontent)
df1['tell_c'] = df1['tell_c'].apply(chuli_fullcontent)
df1['com_info'] = df1['com_info'].apply(chuli_fullcontent)
df1['city_type'] = df1['place'].apply(city_type)
df2 = df1.dropna(how='any')
df2.to_excel('招聘数据.xlsx')