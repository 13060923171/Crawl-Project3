import pandas as pd

df = pd.read_csv('data.csv',parse_dates=['timedate'],index_col='timedate').loc[:,['content']]
df = df.sort_index()
df = df.dropna(how='all')
df = df.drop_duplicates(keep='first')
df.to_csv('new_data.csv')

#
# # 使用pandas读取所有待分析文本
# def get_comment_ori(fd):
#     contentall = []
#     temp = pd.read_csv(fd)
#     contentall.append(temp.content)
#     contentalldf = pd.concat(contentall, ignore_index=True, sort=False)
#     print('comment get:', contentalldf.shape[0])
#     return contentalldf
#
# if __name__ == '__main__':
#     fp = 'new_data.csv'
#     get_comment_ori(fp)




