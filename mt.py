"""
mt论坛自动签到

支持多用户运行
添加变量mtluntan
账号密码用&隔开
多用户用@隔开
例如账号1：10086 密码：1001 
账号1：1234 密码：1234
则变量为10086&1001@1234&1234
export mtluntan=""

cron: 0 0,7 * * *
const $ = new Env("mt论坛");
"""
import requests
import re
import os
import time

#qq:1628708538

#设置ua
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
session = requests.session()

#获取ip
ipdi = requests.get('http://ifconfig.me/ip', timeout=6).text.strip()
print('============📣初始化📣============')
print(ipdi)


#判断国内外地址
dizhi = f'http://ip-api.com/json/{ipdi}?lang=zh-CN'
pdip = requests.get(url=dizhi, timeout=6).json()
country = pdip['country']
if '中国' == country:
    print(country)
else:
    print(f'{country}无法访问论坛')
    exit()
print('==================================')

def main(username,password):
    headers={'User-Agent': ua}
    session.get('https://bbs.binmt.cc/member.php?mod=logging&action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login',headers=headers)
    chusihua = session.get('https://bbs.binmt.cc/member.php?mod=logging&action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login',headers=headers)
    #print(re.findall('loginhash=(.*?)">', chusihua.text))
    loginhash = re.findall('loginhash=(.*?)">', chusihua.text)[0]
    formhash = re.findall('formhash" value="(.*?)".*? />', chusihua.text)[0]
    denurl = f'https://bbs.binmt.cc/member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash={loginhash}&inajax=1'
    data = {'formhash': formhash,'referer': 'https://bbs.binmt.cc/forum.php','loginfield': 'username','username': username,'password': password,'questionid': '0','answer': '',}
    denlu = session.post(headers=headers, url=denurl, data=data).text
    #print(denlu)
    if '欢迎您回来' in denlu:
        #获取分组、名字
        fzmz = re.findall('欢迎您回来，(.*?)，现在', denlu)[0]
        print(f'{fzmz}：登录成功')
        #获取formhash
        zbqd = session.get('https://bbs.binmt.cc/k_misign-sign.html', headers=headers).text
        formhash = re.findall('formhash" value="(.*?)".*? />', zbqd)[0]
        #签到
        qdurl=f'https://bbs.binmt.cc/plugin.php?id=k_misign:sign&operation=qiandao&format=text&formhash={formhash}'
        qd = session.get(url=qdurl, headers=headers).text
        qdyz = re.findall('<root><(.*?)</root>', qd)[0]
        print(f'签到状态：{qdyz}')
        if '已签' in qd:
            huoqu(formhash)
    else:
        print('登录失败')




def huoqu(formhash):
    headers = {'User-Agent': ua}
    huo = session.get('https://bbs.binmt.cc/k_misign-sign.html', headers=headers).text
    pai = re.findall('您的签到排名：(.*?)</div>', huo)[0]
    jiang = re.findall('id="lxreward" value="(.*?)">', huo)[0]
    print(f'签到排名{pai}，奖励{jiang}金币')
    #退出登录，想要多用户必须，执行退出
    tuic = f'https://bbs.binmt.cc/member.php?mod=logging&action=logout&formhash={formhash}'
    session.get(url=tuic, headers=headers)


if __name__ == '__main__':
    #账号
    username = ''
    #username.encode("utf-8")
    #密码
    password = ''
    if 'mtluntan' in os.environ:
        fen = os.environ.get("mtluntan").split("@")
        print(f'查找到{len(fen)}个账号')
        print('==================================')
        for duo in fen:
            username,password = duo.split("&")
            try:
                main(username,password)
                print('============📣结束📣============')
            except Exception as e:
                raise e
    else:
        print('不存在青龙、github变量')
        if username == '' or password == '':
            print('本地账号密码为空')
            exit()
        else:
            try:
                main(username,password)
            except Exception as e:
                raise e
