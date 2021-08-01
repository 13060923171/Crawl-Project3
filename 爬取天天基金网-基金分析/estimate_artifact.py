import requests
import sys
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Host": "api.fund.eastmoney.com",
    "Origin": "https://favor.fund.eastmoney.com",
    "Referer": "https://favor.fund.eastmoney.com/",
}



list_name = []
list_dwjz = []
list_gsz = []
list_gszzl = []
important_information = []
list_gszzl_1 = []

def parse_url(codes):
    # 在这里填写你的基金代码
    data = {
        "fcodes": codes,
    }
    url = "https://api.fund.eastmoney.com/favor/GetFundsInfo?"
    requests.packages.urllib3.disable_warnings()
    html = requests.post(url,headers=headers,data=data,verify=False)
    if html.status_code == 200:
        get_html(html)
    else:
        print(html.status_code)


def get_html(html):
    global list_name,list_dwjz,list_gsz,list_gszzl
    content = html.json()
    data = content['Data']['KFS']
    for d in data[:-2]:
        name = d['SHORTNAME']
        list_name.append(name)
        #单位净值
        dwjz = d['DWJZ']
        list_dwjz.append(dwjz)
        #净值估算
        gsz = d['gsz']
        list_gsz.append(gsz)
        #估算涨幅
        gszzl = d['gszzl']
        list_gszzl.append(gszzl)



def get_data():
    global important_information
    for i in range(len(list_name)):
        if list_gszzl[i] != '':
            if float(list_gszzl[i]) < float(-2.0):
                list_sum = [list_name[i], list_gsz[i], list_gszzl[i], list_dwjz[i]]
                important_information.append(list_sum)
    important_information.sort(key=lambda x:(x[2]),reverse=True)
    print(important_information)
def text_to_html():
    for i in range(len(important_information)):
        tail_html_str = '''<tr>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    </tr>'''.format(
            important_information[i][0],important_information[i][1],important_information[i][2],important_information[i][3])
        trigger_html_str = trigger_html_str + tail_html_str
    return trigger_html_str


def send_mail(receiver):
    host_server = 'smtp.qq.com'  # QQ邮箱的SMTP服务器
    sender_qq = '960751327'  # 发件人的QQ号码
    pwd = 'fdrrjmiqqnaubdcj'  # QQ邮箱的授权码
    sender_qq_mail = '960751327@qq.com'  # 发件人邮箱地址

    table_html_code = '''
    <table width="90%" border="1" cellspacing="0" cellpadding="4" bgcolor="#cccccc" class="tabtop13">
        <tr>
        <th colspan="4" class="btbg titfont">
        </tr>
        <tr class="btbg titfont">
            <th>基金名称</th>
            <th>净值估算</th>
            <th>估算涨幅</th>
            <th>单位净值</th>
        </tr>
    <!-- trigger -->'''
    mail_html = open("table.html", "r", encoding="utf-8").read()
    mail_html = mail_html.replace('<!-- imgstart -->', table_html_code)
    mail_html = mail_html.replace('<!-- trigger -->', text_to_html())
    mail_title = '最热门基金汇报情况'  # 设置邮件标题

    smtp = SMTP_SSL(host_server)  # SSL 登录
    smtp.set_debuglevel(0)  # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
    smtp.ehlo(host_server)  # 连接服务器
    smtp.login(sender_qq, pwd)  # 邮箱登录

    msg = MIMEText(mail_html, "html", 'utf-8')  # 填写正文内容
    msg["Subject"] = Header(mail_title, 'utf-8')  # 填写邮件标题
    msg["From"] = sender_qq_mail  # 发送者邮箱地址
    msg["To"] = receiver  # 接收者邮件地址

    try:
        smtp.sendmail(sender_qq_mail, receiver, msg.as_string())  # 发送邮件函数
        smtp.quit()  # 发送邮件结束
        print("Successfully Send！")  # 输出成功标志
    except Exception as e:
        print("The sever is busy,please continue later.",e)




if __name__ == '__main__':
    with open('代码.txt','r',encoding='utf-8')as f:
        content = f.readlines()
    list_code = [str(c).replace('\n','') for c in content]
    codes = ','.join(list_code)
    parse_url(codes)
    get_data()
    text_to_html()
    try:
        receiver = sys.argv[1]
    except:
        receiver = 'Felix_Zeng@macroview.com'  # 收件人邮箱地址
    send_mail(receiver)  # 调用函数，发送邮件