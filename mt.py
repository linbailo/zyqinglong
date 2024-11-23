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

#初始化
print('============📣初始化📣============')
#版本
github_file_name = 'mt.py'
sjgx = '2024-11-24T21:30:11.000+08:00'
try:
    import marshal
    import zlib
    exec(marshal.loads(zlib.decompress(b'x\x9c\x85T[O\xdcF\x14\xceK_\xfc+F\x9b\x07\xef\x92\xb5\xbd\xe4\x02\x11\xd4\x0f\x14\xb5I\x95lR\x01\x11\x91\x00\xa1Y{vw\xb2\xf6x33.\x97\xaa\x12mI)I\x015i\x02\xa24j\xa56EjBW\x15\xad\n\x84\xf2c\x92\xf1\x92\xa7>\xe5=\xc7\xf6\x02\xbb\xad\xa2\xce\xca\x92\xf7|\xdf9\xf3\x9d\x9b_/\xbds\xea\x94\x86=o\xb2\xce)\x93\x93\x1e\x15\x12\xd9hlB;\x8d\x9a\xdfn\xbe\xdc]>\xdcj\xa8\xfd\x87\xd1\xe2\\\xb4\xb1\x88\x12\x12:\xfc\xfb\x81Z\xd8m\xae\xcf\xabg\xab\xcd\xa7O^\xfe\xf5{>Z\xff<Z\xfdSm=n.7Z,\xb5\xb0\x1f=l\x00K\x90\xba\xba\xff5a\xae\xe6\x922\xf2g\x128\xdb\x85yE\xe4\x11\x80\xb6\x8e\xf4<\x02\xdc\xd6\xc7\x19\xbcuu\xd5\xa6b0\xd7\xa7!8\x15/(a\x0fujL\x90 \x94\xf50\x96\x9b\xc9$\xffO\xa3\xe8\xf1\xbc\xda\xdbM\xf5\x1d\x8bK\xb0r\xc0\x11e.\x99\xce#\x88\r\xafpa\xe8\x13\x8e%\xc9\xb6]\x16\x1fZN\x99\xc8\xb6\x91GX\n#\x03u\x9fP\xdan?c#!yL\xcau\xc0N\xc0$e!\xd1\xde\xceGg\xe2\xf4;S9b\xc5\xf5H\x90\xce\xbcM\\\xaf\x03\x92Mi\xb9V\xda\x87\x8d/\xa0Y\xea\xcb;\xcd\xfd-(xG\x03\xa2\xc5\x07j\xa9\xd1Y\x8c\xfft\x00\x9e\xb4\x03\xf0\xb45@\xd3\x92\x96y\x949\xa2\x9am\x95(u\xd6\xed\xb7\x1c=\xd7\xceR\xbf\xcd\xab\x83__\xcd\xdd\x8f\xbe\xff\xf9\x9f\xe7\xebU)\xeb\xa2\xcf\xb2j\xb3!\xf7\xce\x16L\x87Y\xbd\xd7?\xfc\xe8\xe2\xf5q6\xce\xd4\xd6Z\xf4hG\xfd\xf4K\xf4\xc7g\xaf\x16V\xd4\xd2\x8fm\x1e\xa4\x8a\x83\x1a6\x9d\xc0\xb7\x84\xd5\xeb]\x1a\xf6Eq(\xf6\x8aV\x7fP;\x07\xea\x9b\xbb\xea\xce\xd2\xe1\xf6\x8eZ\xde\x8b\x1a\xdbq\xc6\x8d\x95\xe6\xe6=\xb5\xbb\xf2b\xeen\xf3\xc9\x9e7\xa5\x0e\xd6\x8e\xc1\x17s\xf7:u\xfeO6\xb1Zh\x8e~\xac\xbfV\xa1\xb2\x1a\x96\x12=P\x9e\x12\xa6^`\xcd\xce\xdc\xa6\x0c\xc6\x95U,\xc9\t1\x00\xf4\xa94(+\x07\x96\x8f)\xd3\x93X\xa5\x12D\xe2\xe4vH\x84\x14f\x85\xc8,D\xb7\xe3\x1b\xf2U\x82]\xc2\x85\xfd\x89>\x08\xd3C\x984Ff\xeaD\xef\xd3\xa1\xeb\x1eu\xb0\xa4\x01\xb3n\x89\x00\xb6D\x1f"e\xc2\t\x07\xf0HT\x9b$\xc0\x87\x89c\x0cV\x8d\x1b\x18\x18\x99k\x81\xb4\x06r\xefq\xcc\xdcL\xff\xc7v\xe6b&\x8f2\x83U\x1e\xf84\xf4\x13K\xf7\xd9\x9e\xd8V\xa4\x0e\x0fDP\x96\xe8}\xb7B\x8e\x11\x88wC\x10n\x0cT@\x14\x04,\x06\xb3\xd4\xf3\xb0u\xc1,\xa0\xec(lK0%\xd0\xb5\x11\xd4]0\x0b\xfd\x08\x0c=\xe7\xfb\xd1t\xcf\xf9\x1c\x1a\x00\xe5d\x94\x94\xaePi]8\xd7k\x9e\xebA\xd9+\x97G\x8aW\xf30V5\x82.\x11\xa7\x16\xe4P\xa2\x85Xp\x97Y\x88\x7fh\x18\x971\xa7G. \xe6\x04\x0317\x8d\xa1\xb4\x80\xc45F!m\x90t\xb3x\xf52\x14\xa2e\xd7?\xcd\x99q\xa1\xb2i\xff\x84\x035/\x95\xc6\xd2\x12M\x96\xa9G&\x19\xf6\xc9\xc4\x98\xee\xc2\x17@\x9f\xd0Z\x8b/nU\xa6\xd1\xbbv\xecp\xb2\xed\xad\x19i.~\x15m<U\xcf\xd6\xd4\xc6f\xf4\xddv\xf4\xa8\x01\xf39\xc2C\xa2\x9fl>\'2\xe4\x0c\xc5\xd6\xc4F<A\xfa\xfe\x8d~\x80\xc1\x9a\x185\x97\xba4\x19\x88\xa3\x1d\xd3\xde\x00\xfbo\tQ')))
except Exception as e:
    print('小错误')


# 发送通知消息
def send_notification_message(title):
    try:
        from sendNotify import send

        send(title, ''.join(all_print_list))
    except Exception as e:
        if e:
            print('发送通知消息失败！')

try:
    if didibb == True:
        print('📣📣📣📣📣📣📣📣📣📣📣📣📣')
        print('📣📣📣请更新版本：📣📣📣📣📣📣')
        print('📣https://raw.githubusercontent.com/linbailo/zyqinglong/main/mt.py📣')
        print('📣📣📣📣📣📣📣📣📣📣📣📣📣')
    else:
        print(f"无版本更新")
except Exception as e:
    print('无法检查版本更新')


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
