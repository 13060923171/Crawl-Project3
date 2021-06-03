import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image


# 设置网页名称
st.set_page_config(page_title='调查结果')
# 设置网页标题
st.header('2020年调查问卷')
# 设置网页子标题
st.subheader('2020年各部门对生产部的评分情况')

# 读取数据
excel_file = '各部门对生产部的评分情况.xlsx'
sheet_name = 'DATA'

df = pd.read_excel(excel_file,
                   sheet_name=sheet_name,
                   usecols='B:D',
                   header=3)

# 此处为各部门参加问卷调查人数
df_participants = pd.read_excel(excel_file,
                                sheet_name=sheet_name,
                                usecols='F:G',
                                header=3)
df_participants.dropna(inplace=True)

# streamlit的多重选择(选项数据)
department = df['部门'].unique().tolist()
# streamlit的滑动条(年龄数据)
ages = df['年龄'].unique().tolist()

# 滑动条, 最大值、最小值、区间值
age_selection = st.slider('年龄:',
                          min_value=min(ages),
                          max_value=max(ages),
                          value=(min(ages), max(ages)))

# 多重选择, 默认全选
department_selection = st.multiselect('部门:',
                                      department,
                                      default=department)

# 根据选择过滤数据
mask = (df['年龄'].between(*age_selection)) & (df['部门'].isin(department_selection))
number_of_result = df[mask].shape[0]

# 根据筛选条件, 得到有效数据
st.markdown(f'*有效数据: {number_of_result}*')

# 根据选择分组数据
df_grouped = df[mask].groupby(by=['评分']).count()[['年龄']]
df_grouped = df_grouped.rename(columns={'年龄': '计数'})
df_grouped = df_grouped.reset_index()

# 绘制柱状图, 配置相关参数
bar_chart = px.bar(df_grouped,
                   x='评分',
                   y='计数',
                   text='计数',
                   color_discrete_sequence=['#F63366']*len(df_grouped),
                   template='plotly_white')
st.plotly_chart(bar_chart)

# 添加图片和交互式表格
col1, col2 = st.beta_columns(2)
image = Image.open('survey.jpg')
col1.image(image,
           caption='Designed by 小F / 法纳斯特',
           use_column_width=True)
col2.dataframe(df[mask], width=300)

# 绘制饼图
pie_chart = px.pie(df_participants,
                   title='总的参加人数',
                   values='人数',
                   names='公司部门')
st.plotly_chart(pie_chart)
