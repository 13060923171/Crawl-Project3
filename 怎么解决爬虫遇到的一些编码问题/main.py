import chardet
import requests

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
response = requests.get('https://www.baidu.com',headers=headers)

# 注意下面这行代码，是怎么写的？
# response.encoding = chardet.detect(response.content)['encoding']
# print(response.text)

#或者这个也行，让它的编码等于它自身的编码
response.encoding = response.apparent_encoding
print(response.text)