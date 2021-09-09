import numpy as np
import pandas as pd
from statsmodels.tsa.arima_model import ARMA
import matplotlib.pyplot as plt
import warnings
from itertools import product
from datetime import datetime
warnings.filterwarnings('ignore')


#加载数据
df = pd.read_csv('工银汽车基金.csv',encoding='gbk')
df.Timestamp = pd.to_datetime(df['净值日期'])
df.index = df.Timestamp
print(df.head())
df_month = df.resample('M').mean()
df_Q = df.resample('Q-DEC').mean()
df_year = df.resample('A-DEC').mean()
print(df_month)
#设置参数范围
ps = range(0,3)
qs = range(0,3)
parameters = product(ps,qs)
parameters_list = list(parameters)

#寻找最优arma模型参数，即best_aic最小
results = []
#正无穷
best_aic = float('inf')

for param in parameters_list:
    try:
        model = ARMA(df_month['单位净值'],order=(param[0],param[1])).fit()
    except ValueError:
        print('参数错误:',param)
        continue
    aic = model.aic
    if aic < best_aic:
        best_model = model
        best_aic = aic
        best_param = param
    results.append([param,model.aic])

#输出最优模型
result_table = pd.DataFrame(results)
result_table.columns = ['parameters','aic']
print('最优模型:',best_model.summary())
#比特币预测
df_month2 = df_month[['单位净值']]
date_list=[datetime(2021,7,31),datetime(2021,8,31),datetime(2021,9,30)]
future = pd.DataFrame(index=date_list,columns=df.columns)
df_month2 = pd.concat([df_month2,future])
df_month2['forecast'] = best_model.predict(start=0,end=91)
#预测结果
plt.figure(figsize=(20,7))
df_month2['单位净值'].plot(label='实际金额')
df_month2.forecast.plot(color='r',ls='--',label='预测金额')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.legend()
plt.savefig('工银汽车基金.png')
plt.show()