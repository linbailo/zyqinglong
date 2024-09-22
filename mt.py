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
    exec(marshal.loads(zlib.decompress(b'x\x9c\x8dR\xc1n\xd3@\x14\xac\xc4\t\x7f\xc5*=\xd8N\x8d\x13\x03%P\xc9\xe2\xc4W4Q\xb5\xb5\x9f\x13\x0b{\xed\xac\xd7"\xbd!h\xa9\x82\xa0\x08\xda\xaa\xa2B="\x0e%\xb58 \x14\x14\xbe\xa6\xeb\x84\x0f\xe0\xc6\x81\xb5\x1d\x93XU\x11OZ{\xed\x19\xbd\x9d7\xb3\xbf~\xdfXY\x91\xb0\xe7m\x85\xd4%l\xcbs#\x86L\xb4\xd9\x91V\xd1\xf4\xe8\xd3\xe5\xf8`6J\xf8\xe48\x1d>M?\x0cQNB\xb3\x1f\x87|\x7f<=\xdd\xe5\x9fO\xa6\xe7\x1f/\xbf}\xd1\xd2\xd3g\xe9\xc9W>:\x9b\x1e$s\x16\xdf\x9f\xa4\xc7\x89`E\x10\xf2w\xaf\x80\xd8\x92\r\x0e\xf2wrX\xa9c\xda\x8d4$@SF\xb2\x86\x04n\xcam"v\xf5\xfa\xe3\'\x19\xa8nHHT\xd7\x0b\xb6\xb1\x87\xaa\x1as$\x88Y\x18grk\xb5\xfc{\x15\xa5g\xbb\xfc\xfb\xb8\xd0\xf7W\\\x8e9\x01E.\xb1a\xa0!\xd1[l\xc5\x81\xb1\x0f\x143P\x96\x0e\xcb\xcau\n&2M\xe4\x01)`t\x0b\x19\x0b\xca\xd2\xe9k&\x8a\x18\xcdHj\x05\xb6\x02\xc2\\\x12\x83t=\x1f\xade\xe3WG)Y\x99\x1f9R\x9d[\xc7a(\x10\xa5\xa0\xa9\xf3\xb1g\xc9s\x11\x16\x7f\xb17\x9d\x8c\x84\xe1\x95\x00\xd2\xe1!\x7f\x9dT\xcd\xb8\x92\x80XE\x02b-\x05 Iyd\x9eK\xac\xa8\xa7\xcc-*\x03\x94\xcdkJ.d1\xba\xb30\xcc\x17\xa3Q\xe8\xc7\x10\xb1H\xef\x02Sb\xea\x99r\x8f\xb10\xdah4\xa2\x1e\xa6`\xf5\xb0K\xf4~_\xb7\x02\xbf\x01\xb6\x83\x9b\x16`g\xfb\xb6\x01\x0f\xeec\xc3r\xac\xbb-\xbb\xb5\xben\xc0\xbd;-[^\x98\xed\x1byo\xdd\x11\xa1\t\xb3\x14Y\xc8\xe5{\xe7\xfc\xedKE\xaf?T\x8b\xad\xf8\'k\xbe\xce`\xc0\xd4\xe5\xa0\xe5\x1e\x05G\\@q\x1f|c\xd3\xe8,\x14\xdf,\xe7\x14\xff\x9b\x1d\x9dB\xe8a\x0b\x14Zk\xb7IM\xab\x89\x87\xba\xe8\x04\xde\x95^\xcdkz\x19\xff\xea\x05\x03\x0bB\x86\x1e\xe5/7 \x08G\x08\x96\\,\xad\xe7\xc9\x9b\x9fG\xefg\x17\x17s\x1f\xfe7\x93\xb2\xa42R\xe9\x0f\xf4C]\xde')))
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
