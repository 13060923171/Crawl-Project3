import pandas as pd


df = pd.read_csv('李宇春-男.csv')
# 查看数据的重复值
df[df.duplicated()==True]
# 根据某列查看重复值
# df[df['行 ID'].duplicated()==True]
# 删除重复值（默认first）
df.drop_duplicates(keep='first',inplace=True)
# df.columns = ['标题','文章内容','时间']
df.columns = pd.MultiIndex.from_tuples(zip(['标题','文章内容','时间'], df.columns))
df.dropna(axis=0,how='any',inplace=True)
df.to_excel('李宇春-男.xlsx',encoding='gbk')