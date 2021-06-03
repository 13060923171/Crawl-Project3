import pandas as pd
import numpy as np


df = pd.read_excel('刘雨昕-男.xls',sheet_name='final').loc[1:,['序号','内容','尾数','反驳男性气质和男化','与男性相比较','小麦肌肉男（性取向）','肯定男性气质','宝冢男役','男化','男粉','性取向的讨论','对性别无偏向','讨论性别刻板','不男不女','感情生活']]


def comment_1():
    list_1 = []
    for i in df['反驳男性气质和男化']:
        if np.isnan(i) == False:
            list_1.append(i)
    list_1.sort(key=lambda x:x,reverse=False)

    list_number = []
    for n in df['序号']:
        n = int(n)
        list_number.append(n)
    list_comment = []
    for c in df['内容']:
        c = str(c)
        list_comment.append(c)
    list_mantissa = []
    for m in df['尾数']:
        m = int(m)
        list_mantissa.append(m)

    array_1 = []
    array_2 = []
    array_3 = []
    for l in list_1:
        for k in range(len(list_comment)):
            if list_number[k] == l:
                array_1.append(list_number[k])
                array_2.append(list_comment[k])
                array_3.append(list_mantissa[k])
    df1 = pd.DataFrame()
    df1['序号'] = array_1
    df1['文字内容'] = array_2
    df1['数字'] = array_3
    return df1

def comment_2():
    list_1 = []
    for i in df['与男性相比较']:
        if np.isnan(i) == False:
            list_1.append(i)
    list_1.sort(key=lambda x:x,reverse=False)

    list_number = []
    for n in df['序号']:
        n = int(n)
        list_number.append(n)
    list_comment = []
    for c in df['内容']:
        c = str(c)
        list_comment.append(c)
    list_mantissa = []
    for m in df['尾数']:
        m = int(m)
        list_mantissa.append(m)

    array_1 = []
    array_2 = []
    array_3 = []
    for l in list_1:
        for k in range(len(list_comment)):
            if list_number[k] == l:
                array_1.append(list_number[k])
                array_2.append(list_comment[k])
                array_3.append(list_mantissa[k])
    df1 = pd.DataFrame()
    df1['序号'] = array_1
    df1['文字内容'] = array_2
    df1['数字'] = array_3
    return df1

def comment_3():
    list_1 = []
    for i in df['小麦肌肉男（性取向）']:
        if np.isnan(i) == False:
            list_1.append(i)
    list_1.sort(key=lambda x:x,reverse=False)

    list_number = []
    for n in df['序号']:
        n = int(n)
        list_number.append(n)
    list_comment = []
    for c in df['内容']:
        c = str(c)
        list_comment.append(c)
    list_mantissa = []
    for m in df['尾数']:
        m = int(m)
        list_mantissa.append(m)

    array_1 = []
    array_2 = []
    array_3 = []
    for l in list_1:
        for k in range(len(list_comment)):
            if list_number[k] == l:
                array_1.append(list_number[k])
                array_2.append(list_comment[k])
                array_3.append(list_mantissa[k])
    df1 = pd.DataFrame()
    df1['序号'] = array_1
    df1['文字内容'] = array_2
    df1['数字'] = array_3
    return df1

def comment_4():
    list_1 = []
    for i in df['肯定男性气质']:
        if np.isnan(i) == False:
            list_1.append(i)
    list_1.sort(key=lambda x:x,reverse=False)

    list_number = []
    for n in df['序号']:
        n = int(n)
        list_number.append(n)
    list_comment = []
    for c in df['内容']:
        c = str(c)
        list_comment.append(c)
    list_mantissa = []
    for m in df['尾数']:
        m = int(m)
        list_mantissa.append(m)

    array_1 = []
    array_2 = []
    array_3 = []
    for l in list_1:
        for k in range(len(list_comment)):
            if list_number[k] == l:
                array_1.append(list_number[k])
                array_2.append(list_comment[k])
                array_3.append(list_mantissa[k])
    df1 = pd.DataFrame()
    df1['序号'] = array_1
    df1['文字内容'] = array_2
    df1['数字'] = array_3
    return df1

def comment_5():
    list_1 = []
    for i in df['宝冢男役']:
        if np.isnan(i) == False:
            list_1.append(i)
    list_1.sort(key=lambda x:x,reverse=False)

    list_number = []
    for n in df['序号']:
        n = int(n)
        list_number.append(n)
    list_comment = []
    for c in df['内容']:
        c = str(c)
        list_comment.append(c)
    list_mantissa = []
    for m in df['尾数']:
        m = int(m)
        list_mantissa.append(m)

    array_1 = []
    array_2 = []
    array_3 = []
    for l in list_1:
        for k in range(len(list_comment)):
            if list_number[k] == l:
                array_1.append(list_number[k])
                array_2.append(list_comment[k])
                array_3.append(list_mantissa[k])
    df1 = pd.DataFrame()
    df1['序号'] = array_1
    df1['文字内容'] = array_2
    df1['数字'] = array_3
    return df1

def comment_6():
    list_1 = []
    for i in df['男化']:
        if np.isnan(i) == False:
            list_1.append(i)
    list_1.sort(key=lambda x:x,reverse=False)

    list_number = []
    for n in df['序号']:
        n = int(n)
        list_number.append(n)
    list_comment = []
    for c in df['内容']:
        c = str(c)
        list_comment.append(c)
    list_mantissa = []
    for m in df['尾数']:
        m = int(m)
        list_mantissa.append(m)

    array_1 = []
    array_2 = []
    array_3 = []
    for l in list_1:
        for k in range(len(list_comment)):
            if list_number[k] == l:
                array_1.append(list_number[k])
                array_2.append(list_comment[k])
                array_3.append(list_mantissa[k])
    df1 = pd.DataFrame()
    df1['序号'] = array_1
    df1['文字内容'] = array_2
    df1['数字'] = array_3
    return df1

def comment_7():
    list_1 = []
    for i in df['男粉']:
        if np.isnan(i) == False:
            list_1.append(i)
    list_1.sort(key=lambda x:x,reverse=False)

    list_number = []
    for n in df['序号']:
        n = int(n)
        list_number.append(n)
    list_comment = []
    for c in df['内容']:
        c = str(c)
        list_comment.append(c)
    list_mantissa = []
    for m in df['尾数']:
        m = int(m)
        list_mantissa.append(m)

    array_1 = []
    array_2 = []
    array_3 = []
    for l in list_1:
        for k in range(len(list_comment)):
            if list_number[k] == l:
                array_1.append(list_number[k])
                array_2.append(list_comment[k])
                array_3.append(list_mantissa[k])
    df1 = pd.DataFrame()
    df1['序号'] = array_1
    df1['文字内容'] = array_2
    df1['数字'] = array_3
    return df1

def comment_8():
    list_1 = []
    for i in df['性取向的讨论']:
        if np.isnan(i) == False:
            list_1.append(i)
    list_1.sort(key=lambda x:x,reverse=False)

    list_number = []
    for n in df['序号']:
        n = int(n)
        list_number.append(n)
    list_comment = []
    for c in df['内容']:
        c = str(c)
        list_comment.append(c)
    list_mantissa = []
    for m in df['尾数']:
        m = int(m)
        list_mantissa.append(m)

    array_1 = []
    array_2 = []
    array_3 = []
    for l in list_1:
        for k in range(len(list_comment)):
            if list_number[k] == l:
                array_1.append(list_number[k])
                array_2.append(list_comment[k])
                array_3.append(list_mantissa[k])
    df1 = pd.DataFrame()
    df1['序号'] = array_1
    df1['文字内容'] = array_2
    df1['数字'] = array_3
    return df1

def comment_9():
    list_1 = []
    for i in df['对性别无偏向']:
        if np.isnan(i) == False:
            list_1.append(i)
    list_1.sort(key=lambda x:x,reverse=False)

    list_number = []
    for n in df['序号']:
        n = int(n)
        list_number.append(n)
    list_comment = []
    for c in df['内容']:
        c = str(c)
        list_comment.append(c)
    list_mantissa = []
    for m in df['尾数']:
        m = int(m)
        list_mantissa.append(m)

    array_1 = []
    array_2 = []
    array_3 = []
    for l in list_1:
        for k in range(len(list_comment)):
            if list_number[k] == l:
                array_1.append(list_number[k])
                array_2.append(list_comment[k])
                array_3.append(list_mantissa[k])
    df1 = pd.DataFrame()
    df1['序号'] = array_1
    df1['文字内容'] = array_2
    df1['数字'] = array_3
    return df1

def comment_10():
    list_1 = []
    for i in df['讨论性别刻板']:
        if np.isnan(i) == False:
            list_1.append(i)
    list_1.sort(key=lambda x:x,reverse=False)

    list_number = []
    for n in df['序号']:
        n = int(n)
        list_number.append(n)
    list_comment = []
    for c in df['内容']:
        c = str(c)
        list_comment.append(c)
    list_mantissa = []
    for m in df['尾数']:
        m = int(m)
        list_mantissa.append(m)

    array_1 = []
    array_2 = []
    array_3 = []
    for l in list_1:
        for k in range(len(list_comment)):
            if list_number[k] == l:
                array_1.append(list_number[k])
                array_2.append(list_comment[k])
                array_3.append(list_mantissa[k])
    df1 = pd.DataFrame()
    df1['序号'] = array_1
    df1['文字内容'] = array_2
    df1['数字'] = array_3
    return df1

def comment_11():
    list_1 = []
    for i in df['不男不女']:
        if np.isnan(i) == False:
            list_1.append(i)
    list_1.sort(key=lambda x:x,reverse=False)

    list_number = []
    for n in df['序号']:
        n = int(n)
        list_number.append(n)
    list_comment = []
    for c in df['内容']:
        c = str(c)
        list_comment.append(c)
    list_mantissa = []
    for m in df['尾数']:
        m = int(m)
        list_mantissa.append(m)

    array_1 = []
    array_2 = []
    array_3 = []
    for l in list_1:
        for k in range(len(list_comment)):
            if list_number[k] == l:
                array_1.append(list_number[k])
                array_2.append(list_comment[k])
                array_3.append(list_mantissa[k])
    df1 = pd.DataFrame()
    df1['序号'] = array_1
    df1['文字内容'] = array_2
    df1['数字'] = array_3
    return df1

def comment_12():
    list_1 = []
    for i in df['感情生活']:
        if np.isnan(i) == False:
            list_1.append(i)
    list_1.sort(key=lambda x:x,reverse=False)

    list_number = []
    for n in df['序号']:
        n = int(n)
        list_number.append(n)
    list_comment = []
    for c in df['内容']:
        c = str(c)
        list_comment.append(c)
    list_mantissa = []
    for m in df['尾数']:
        m = int(m)
        list_mantissa.append(m)

    array_1 = []
    array_2 = []
    array_3 = []
    for l in list_1:
        for k in range(len(list_comment)):
            if list_number[k] == l:
                array_1.append(list_number[k])
                array_2.append(list_comment[k])
                array_3.append(list_mantissa[k])
    df1 = pd.DataFrame()
    df1['序号'] = array_1
    df1['文字内容'] = array_2
    df1['数字'] = array_3
    return df1



def sum_comment():
    df1 = comment_1()
    df2 = comment_2()
    df3 = comment_3()
    df4 = comment_4()
    df5 = comment_5()
    df6 = comment_6()
    df7 = comment_7()
    df8 = comment_8()
    df9 = comment_9()
    df10 = comment_10()
    df11 = comment_11()
    df12 = comment_12()


    name = ['反驳男性气质和男化','与男性相比较','小麦肌肉男（性取向）','肯定男性气质','宝冢男役','男化','男粉','性取向的讨论','对性别无偏向','讨论性别刻板','不男不女','感情生活']
    with pd.ExcelWriter('刘雨昕.xlsx') as xlsx:
        df1.to_excel(xlsx, sheet_name="反驳男性气质和男化", index=False)
        df2.to_excel(xlsx, sheet_name="与男性相比较", index=False)
        df3.to_excel(xlsx, sheet_name="小麦肌肉男（性取向）", index=False)
        df4.to_excel(xlsx, sheet_name="肯定男性气质", index=False)
        df5.to_excel(xlsx, sheet_name="宝冢男役", index=False)
        df6.to_excel(xlsx, sheet_name="男化", index=False)
        df7.to_excel(xlsx, sheet_name="男粉", index=False)
        df8.to_excel(xlsx, sheet_name="性取向的讨论", index=False)
        df9.to_excel(xlsx, sheet_name="对性别无偏向", index=False)
        df10.to_excel(xlsx, sheet_name="讨论性别刻板", index=False)
        df11.to_excel(xlsx, sheet_name="不男不女", index=False)
        df12.to_excel(xlsx, sheet_name="感情生活", index=False)


if __name__ == '__main__':
    sum_comment()
