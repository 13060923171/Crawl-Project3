import json
import os
import re
import shutil
import ssl
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from lxml import etree
import random
user_agent = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
headers = {
    "user-agent":random.choice(user_agent),
    "referer": "https://www.bilibili.com/",
    "cookie": "_uuid=DE95E435-8C4C-4C3F-93A1-57DB808F829530580infoc; buvid3=E2B1C11B-A111-4692-B768-316E8429C7E018547infoc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(um||k))uYu0J'uYuR)JJkkm; fingerprint=1211965a971db090bbca7833362e2fa0; buvid_fp=E2B1C11B-A111-4692-B768-316E8429C7E018547infoc; buvid_fp_plain=E2B1C11B-A111-4692-B768-316E8429C7E018547infoc; DedeUserID=35906556; DedeUserID__ckMd5=6bc77a6b9c4d788a; SESSDATA=d2c1dbd1%2C1630807734%2C99121*31; bili_jct=b0752bdcf4df366921028c4ff10d0374; PVID=1; CURRENT_QUALITY=0; innersign=0; arrange=matrix"
}

def re_video_info(text, pattern):
    '''利用正则表达式匹配出视频信息并转化成json'''
    match = re.search(pattern, text)
    return json.loads(match.group(1))


def create_folder(aid):
    '''创建文件夹'''
    if not os.path.exists(aid):
        os.mkdir(aid)


def remove_move_file(aid):
    '''删除和移动文件'''
    file_list = os.listdir('./')
    for file in file_list:
        ## 移除临时文件
        if file.endswith('_video.mp4'):
            os.remove(file)
            pass
        elif file.endswith('_audio.mp4'):
            os.remove(file)
            pass
        ## 保存最终的视频文件
        elif file.endswith('.mp4'):
            if os.path.exists(aid + '/' + file):
                os.remove(aid + '/' + file)
            shutil.move(file, aid)

def download_video_batch(referer_url, video_url, audio_url, video_name, index):
    '''批量下载系列视频'''
    ## 更新请求头
    headers.update({"Referer": referer_url})
    ## 获取文件名
    short_name = video_name.split('/')[2]
    print("%d.\t视频下载开始：%s" % (index, short_name))
    ## 下载并保存视频
    video_content = requests.get(video_url, headers=headers)
    print('%d.\t%s\t视频大小：' % (index, short_name),
          round(int(video_content.headers.get('content-length', 0)) / 1024 / 1024, 2), '\tMB')
    received_video = 0
    with open('%s_video.mp4' % video_name, 'ab') as output:
        headers['Range'] = 'bytes=' + str(received_video) + '-'
        response = requests.get(video_url, headers=headers)
        output.write(response.content)
    ## 下载并保存音频
    audio_content = requests.get(audio_url, headers=headers)
    print('%d.\t%s\t音频大小：' % (index, short_name),
          round(int(audio_content.headers.get('content-length', 0)) / 1024 / 1024, 2), '\tMB')
    received_audio = 0
    with open('%s_audio.mp4' % video_name, 'ab') as output:
        headers['Range'] = 'bytes=' + str(received_audio) + '-'
        response = requests.get(audio_url, headers=headers)
        output.write(response.content)
        received_audio += len(response.content)
    return video_name, index

def video_audio_merge_batch(result):
    '''使用ffmpeg批量视频音频合并'''
    video_name = result.result()[0]
    index = result.result()[1]
    import subprocess
    video_final = video_name.replace('video', 'video_final')
    command = 'ffmpeg -i "%s_video.mp4" -i "%s_audio.mp4" -c copy "%s.mp4" -y -loglevel quiet' % (
        video_name, video_name, video_final)
    subprocess.Popen(command, shell=True)
    print("%d.\t视频下载结束：%s" % (index, video_name.split('/')[2]))

