import requests

url = 'https://api.juliangip.com/api/dynamic/getdynamic?num=100&pt=1&resultType=text&split=\\r\\n&tradeNo=1048021442024661&type=time&sign=0163c016e4b4c5c0b5b10d17f74fb619'

response = requests.get(url)
print(response.text)