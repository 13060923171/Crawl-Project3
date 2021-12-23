import requests
import json
import os
import pandas as pd
import time
import re


# 获取AT类
class GetAccessToken:
    def __init__(self):
        # 【修改点1】输入自己在百度AI控制台申请应用后获得的AK和SK
        self.AK = 'xyR6OvnOT5pXNhays7yXQH77'
        self.SK = '4i92fTbNlFg8XATx4VgQDL2Sk19wVOXK'
        self.token_url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + self.AK + '&client_secret=' + self.SK
        self.headers = {'Content-Type': 'application/json; charset=UTF-8'}

    def get_access_token(self):
        r = requests.get(self.token_url, headers=self.headers)
        if r.text:
            tokenkey = json.loads(r.text)['access_token']
            print('get token success')

            return tokenkey
        else:
            print('get token fail')
            return ''


# 调用API类
class SentimentBaidu:
    def __init__(self, tp):
        # 调用自己需要使用的API，这里使用情感分析API作为示例，其他接口查询百度AI说明文档后替换 + 前的URL
        self.HOST = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify' + '?access_token='
        self.headers = {"Content-Type":"application/json"}
        self.textpath = tp
        self.commentcomment = []
        self.count = 0
        # 速度设置，对应百度AI的QPS限制，由于request发送请求的速度跟网速、设备性能有关，所以虽然限制是5QPS，但可以把请求的间隔写短点，这里采用的是最快0.06s
        self.speedlimit = 0.06
        # 初始速度，后续实际请求速度程序自动根据错误调整
        self.sleepdt = 0.6
        self.errorwaittime = 0.5
        self.qpserror = 0.2
        self.qpserrorindex = 0
        self.errorallcount = 0

    # 调用百度API获得情感分析结果方法
    def get_content_sentiments(self, text, at):
        data = {
            "text": text
        }
        url = self.HOST + at + "&charset=UTF-8"
        try:
            if self.count - self.qpserrorindex > 500:
                if self.sleepdt > self.speedlimit:
                    self.sleepdt -= 0.001
                    print('speed up, current speed:',
                          self.sleepdt)
                    self.qpserrorindex = self.count
            time.sleep(self.sleepdt)
            r = requests.post(url=url, data=json.dumps(data), headers=self.headers)

            if 'error_code' in r.text:
                error = r.json()['error_code']
                print('error_code', error)
                if error == 18:
                    self.errorallcount += 1
                    self.qpserror += 1
                    self.qpserrorindex = self.count
                    self.sleepdt += 0.001
                    print('current qps error count = ', self.qpserror, 'speed down, current speed:', self.sleepdt,
                          self.errorallcount)
                    time.sleep(self.errorwaittime)
            content = r.json()

        except Exception as e:
            self.errorallcount += 1
            time.sleep(self.errorwaittime)
            return
        try:
            if content['items']:
                contentposprob = content['items'][0]['positive_prob']
                contentnegprob = content['items'][0]['negative_prob']
                contentconfi = content['items'][0]['confidence']
                contentsenti = content['items'][0]['sentiment']
                temp = [contentposprob, contentnegprob, contentconfi, contentsenti]

                return temp
        except KeyError as e:
            self.errorallcount += 1
            print('error reason:', content)
            time.sleep(self.errorwaittime)
            return

    # 使用pandas读取所有待分析文本
    def get_comment_ori(self, fd):
        contentall = []
        temp = pd.read_csv(fd)
        contentall.append(temp)
        contentalldf = pd.concat(contentall, ignore_index=True, sort=False)
        print('comment get:', contentalldf.shape[0])
        return contentalldf

    # 主程序
    def run(self):
        requests.adapters.DEFAULT_RETRIES = 5
        ATclass = GetAccessToken()
        AT = ATclass.get_access_token()
        print('progress start current speed = ', self.sleepdt)
        # 【修改点3】以下4行为获取文本，可选择自己常用的方式，将所有文本待分析文本放到一个iterator中，这里使用的pandas读取文本
        contentalldf = self.get_comment_ori(self.textpath)
        commentcontent = contentalldf['content']
        commentcontent = pd.DataFrame(commentcontent)
        # commentcontent['timedate'] = contentalldf['timedate']
        commentcontent.columns = ['comment']
        commentcontent['comment'] = commentcontent['comment'].apply(self.clean_comment)
        # 如果在调用接口前想先对文本符号、表情等信息进行清理，可调用clean_comment函数，通过pandas的apply快速处理所有文本
        #**********  清理无用符号、表情包等信息  commentcontent['comment'] = commentcontent['comment'].apply(self.clean_comment)
        for comment,timedate in zip(commentcontent['comment'],contentalldf['timedate']):
            if comment:
                self.count += 1
                if self.count % 100 == 0:
                    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                          '正在处理第{0}条评论'.format(self.count))
                commentsenti = self.get_content_sentiments(comment, AT)
                if commentsenti is not None:
                    commentbatch = [comment] + commentsenti + [timedate]
                    self.commentcomment.append(commentbatch)
                if self.count % 100 == 0:
                    commentsentidf = pd.DataFrame(self.commentcomment,
                                                  #comment 指的是文本内容 contentposprob指的是积极情绪 contentnegprob指的是消极情绪 contentconfi指的是置信度 #contentsenti是观点或者种类的意思
                                                  columns=['comment', 'contentposprob', 'contentnegprob',
                                                           'contentconfi', 'contentsenti','timedate'])
                    fpath = 'cpbaidu.csv'
                    if os.path.exists(fpath):
                        commentsentidf.to_csv(fpath, mode='a', encoding='utf-8-sig', index=False, header=False)
                    else:
                        commentsentidf.to_csv(fpath, encoding='utf-8-sig', index=False)
                    # print('write to path',fpath,'write num:',commentsentidf.shape[0])
                    self.commentcomment = []
        print('finished progress')

    # 文本清理方法，可选是否剔除文本内的符号、空格、emoji的剔除
    def clean_comment(self, text):
        emoji = re.compile(u'['
                           u'\U0001F300-\U0001F64F'
                           u'\U0001F680-\U0001F6FF'
                           u'\u2600-\u2B55]+',
                           re.UNICODE)
        text = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）:：]+", "", text)
        text = re.sub(emoji, '', text)
        return text


if __name__ == '__main__':
    fp = 'new_data.csv'
    runner = SentimentBaidu(fp)
    runner.run()