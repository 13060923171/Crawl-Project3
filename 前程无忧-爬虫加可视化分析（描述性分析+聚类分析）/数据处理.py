import json
import random

import pandas

def __initdata__():
    with open("funnc.txt", 'r', encoding='utf-8') as fc:
        fcs = [i.strip() for i in fc.readlines()]
        l_ = []
        for ic in fcs:
            try:
                l_.append(json.loads(ic))
            except Exception as e:
                print(f"异常：{e}")
    data = pandas.DataFrame(l_)
    data.to_excel(f"51_{random.randint(1, 99)}.xlsx")


def handle_min(text):
    if type(text) == float:
        return '-'
    if text.strip().endswith("千/月"):
        salary = text.replace("千/月",'').split("-")[0]
        return float(salary)*1000
    elif text.strip().endswith("万/月"):
        salary = text.replace("万/月",'').split("-")[0]
        return float(salary) * 10000
    elif text.strip().endswith("万/年"):
        salary = text.replace("万/年",'').split("-")[0]
        return float(salary) * 10000 / 12
    elif text.strip().endswith("元/天"):
        salary = text.replace("元/天",'').split("-")[0]
        return float(salary) * 30
    elif text.strip().endswith("万以上/年"):
        salary = text.replace("万以上/年",'').split("-")[0]
        return float(salary) * 10000/12

def handle_max(text):
    if type(text) == float:
        return '-'
    if text.strip().endswith("千/月"):
        salary = text.replace("千/月",'').split("-")[-1]
        return float(salary)*1000
    elif text.strip().endswith("万/月"):
        salary = text.replace("万/月",'').split("-")[-1]
        return float(salary) * 10000
    elif text.strip().endswith("万/年"):
        salary = text.replace("万/年",'').split("-")[-1]
        return float(salary) * 10000 / 12
    elif text.strip().endswith("元/天"):
        salary = text.replace("元/天",'').split("-")[-1]
        return float(salary) * 30
    elif text.strip().endswith("万以上/年"):
        salary = text.replace("万以上/年",'').split("-")[-1]
        return float(salary) * 10000/12
def __clear__():
    pd_ = pandas.read_excel("link.xlsx")
    print(pd_.head(5))
    pd_["min_salary"] = pd_["providesalary_text"].apply(handle_min)
    pd_["max_salary"] = pd_["providesalary_text"].apply(handle_max)
    print(pd_["min_salary"],pd_["max_salary"])
    print(f"==>")
    pd_.to_excel(f'处理后总数据.xlsx')
    pddd_data = pd_.to_dict(orient='records')
    city_data = list(set([i.get("city") for i in pddd_data]))
    for icity in city_data:
        filter_data = [i for  i in pddd_data if i.get("city") == icity]
        pd_datas = pandas.DataFrame(filter_data)
        pd_datas.to_excel(f"{icity}.xlsx")

    # pd_data = pd_.to_dict(orient='records')


if  __name__ == '__main__':
    __initdata__()
