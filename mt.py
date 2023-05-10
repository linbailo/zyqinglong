"""
mt论坛自动签到

暂不支持多个账号，我知道你们肯定没有这个需求

账号变量 mtusername 
密码变量 mtpassword
export mtusername=""
export mtpassword=""

cron: 0 0,7, * * *
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

def main(username,password):
    headers={'User-Agent': ua}
    session.get('https://bbs.binmt.cc/member.php?mod=logging&action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login',headers=headers)
    chusihua = session.get('https://bbs.binmt.cc/member.php?mod=logging&action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login',headers=headers)
    print(re.findall('loginhash=(.*?)">', chusihua.text))
    loginhash = re.findall('loginhash=(.*?)">', chusihua.text)[0]
    formhash = re.findall('formhash" value="(.*?)".*? />', chusihua.text)[0]
    denurl = f'https://bbs.binmt.cc/member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash={loginhash}&inajax=1'
    data = {'formhash': formhash,'referer': 'https://bbs.binmt.cc/forum.php','loginfield': 'username','username': username,'password': password,'questionid': '0','answer': '',}
    denlu = session.post(headers=headers, url=denurl, data=data).text
    print(denlu)
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
        qdyz = re.findall('<root><(.*?)</root>', qd)
        print(qd)
    else:
        print('登录失败')



if __name__ == '__main__':
    #账号
    username = ''
    #username.encode("utf-8")
    #密码
    password = ''
    if 'mtusername' in os.environ:
        username = os.environ.get("mtusername")
    else:
        print('不存在青龙、github变量')
    if 'mtpassword' in os.environ:
        password = os.environ.get("mtpassword")
    
    try:
        main(username,password)
    except Exception as e:
        raise e

