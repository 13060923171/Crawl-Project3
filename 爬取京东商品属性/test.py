from phone import Book,sess
import pandas as pd

df = pd.read_excel('商品属性.xls').loc[:,['价钱','评论','好评','差评','品牌']]

for i in range(len(df['价钱'])):
    try:
        book_data = Book(
            price=df['价钱'][i],
            comment=df['评论'][i],
            goodrate=df['好评'][i],
            poorrate=df['差评'][i],
            attribute=df['品牌'][i]
        )
        sess.add(book_data)
        sess.commit()
    except Exception as e:
        print(e)
        # 如果出错了就回滚到原来的地方
        sess.rollback()
