'''
Function:
	美团小爬虫主程序

python交流群:
	976191019
'''
import os
import re
import time
import random
import pickle
import argparse
import requests
from utils import *
from urllib.parse import urlencode


'''程序初始化'''
def initialProgram(cityname):
	cur_path = os.path.abspath(os.path.dirname(__file__))
	citynamesfilepath = os.path.join(cur_path, 'data\\cities.json')
	uafilepath = os.path.join(cur_path, 'data\\useragents.data')
	uuidfilepath = os.path.join(cur_path, 'data\\uuid.data')
	brfilepath = os.path.join(cur_path, 'data/br.json')
	savedatapath = os.path.join(cur_path, '%s_data.json' % cityname)
	# cities
	if not os.path.isfile(citynamesfilepath):
		downCitynamesfile(citynamesfilepath)
	# uuid
	url = 'https://{}.meituan.com/meishi/c54/'.format(cityname2CODE(cityname, citynamesfilepath))
	headers = {'User-Agent': getRandomUA(uafilepath)}
	res = requests.get(url, headers=headers)
	with open(uuidfilepath, 'w') as f:
		uuid = '467ca50fcf8c4c2f9ca8.1619840960.1.0.0'
		f.write(uuid)
	# return
	return citynamesfilepath, uafilepath, uuidfilepath, brfilepath, savedatapath


'''主函数'''
def MTSpider(cityname, maxpages=50):
	data_pages = {}
	citynamesfilepath, uafilepath, uuidfilepath, brfilepath, savedatapath = initialProgram(cityname)
	base_url = 'https://{}.meituan.com/meishi/api/poi/getPoiList?'.format(cityname2CODE(cityname, citynamesfilepath))
	try:
		for page in range(1, maxpages+1):
			print('[INFO]: Getting the data of page<%s>...' % page)
			data_page = None
			while data_page is None:
				params = getGETPARAMS(cityname, page, citynamesfilepath, uuidfilepath, brfilepath)
				url = base_url + urlencode(params)
				headers = {
							'Accept': 'application/json',
							'Accept-Encoding': 'gzip, deflate, br',
							'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
							'User-Agent': getRandomUA(uafilepath),
							'Connection': 'keep-alive',
							'Host': 'bj.meituan.com',
							"Cookie": "_lxsdk_cuid=176cc938bb490-0040463f3d68d8-c791039-e1000-176cc938bb5c8; iuuid=25A31E7553EB400F96942D62BCA7FFBAE7732C1D202A34A2546AD68C9161CB68; _lxsdk=25A31E7553EB400F96942D62BCA7FFBAE7732C1D202A34A2546AD68C9161CB68; Hm_lvt_f66b37722f586a240d4621318a5a6ebe=1609852138; cityname=%E6%97%A0%E9%94%A1; mtcdn=K; lsu=; _hc.v=6fea36cf-6c02-d091-81e6-5ab379b908b1.1619617992; uuid=467ca50fcf8c4c2f9ca8.1619840960.1.0.0; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; lat=23.135345; lng=113.328989; userTicket=MJIYeuHUYMFdwqxbVbpsjiSzxRxipJnNzorMuGXc; u=229598129; n=%E4%BD%A0%E5%A5%8B%E6%96%97%E7%9A%84%E6%A0%B7%E5%AD%90%E7%9C%9F%E7%BE%8E; lt=3KGjWo9w0A2H2OcA5tQci717hAYAAAAAZg0AAA3FQTuxg448C3pkvgRcDonrp7jM6uYVuYj8rmGtE4hyHrk_6dykwdr4ijgHchZeTA; mt_c_token=3KGjWo9w0A2H2OcA5tQci717hAYAAAAAZg0AAA3FQTuxg448C3pkvgRcDonrp7jM6uYVuYj8rmGtE4hyHrk_6dykwdr4ijgHchZeTA; token=3KGjWo9w0A2H2OcA5tQci717hAYAAAAAZg0AAA3FQTuxg448C3pkvgRcDonrp7jM6uYVuYj8rmGtE4hyHrk_6dykwdr4ijgHchZeTA; token2=3KGjWo9w0A2H2OcA5tQci717hAYAAAAAZg0AAA3FQTuxg448C3pkvgRcDonrp7jM6uYVuYj8rmGtE4hyHrk_6dykwdr4ijgHchZeTA; unc=%E4%BD%A0%E5%A5%8B%E6%96%97%E7%9A%84%E6%A0%B7%E5%AD%90%E7%9C%9F%E7%BE%8E; ci=50; rvct=50%2C238%2C20%2C52%2C1; __mta=209509933.1619883183110.1619883183110.1619883183110.1; client-id=366007ed-0a00-40a9-8026-e4ed9feb2bbc; firstTime=1619886833017; _lxsdk_s=17928894873-e8-958-49c%7C%7C137",
							'Referer': 'https://{}.meituan.com/'.format(cityname2CODE(cityname, citynamesfilepath))
						}
				res = requests.get(url, headers=headers)
				data_page = parsePage(json.loads(res.text))
				print(data_page)
				if data_page is None:
					time.sleep(random.random()+random.randint(3, 6))
					initialProgram(cityname)
			data_pages.update(data_page)
			if page != maxpages:
				time.sleep(random.random()+random.randint(3, 6))
	except:
		print('[Warning]: Something wrong...')
	with open(savedatapath, 'wb',encoding='utf-8') as f:
		pickle.dump(data_pages, f)


'''run'''
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Spider for gourmet shops in meituan.")
	parser.add_argument('-c', dest='cityname', help='The city you choose to crawl.', default='杭州')
	parser.add_argument('-p', dest='maxpages', help='Max pages to crawl.', default=50, type=int)
	args = parser.parse_args()
	cityname = args.cityname
	maxpages = args.maxpages
	MTSpider(cityname, maxpages)