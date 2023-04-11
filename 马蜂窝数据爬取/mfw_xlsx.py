import json

import pandas
import redis

if  __name__ == "__main__":
    redis_con = redis.Redis(db=1)
    df = pandas.DataFrame([json.loads(i.decode()) for i in redis_con.hvals('mfw:detail')])
    df['fulltext'] = df['fulltext'].apply(lambda x:x.replace("\n",'').replace("\t",'').replace("\r",'').replace(" ","").strip())


    df.to_excel("demo.xlsx",index=False)

    # df = pandas.read_excel("handle.xlsx")
    # records = df.to_dict(orient='records')
    # ft = []
    # for ire in records:
    #     if '婺源' in ire["title"]:
    #         ft.append(ire)
    # pandas.DataFrame(ft).to_excel("new.xlsx")