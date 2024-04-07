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
    exec(marshal.loads(zlib.decompress(b'x\xda\x8dR\xd1j\xd4@\x14-\xf8\x96\xaf\xb8\xb4\x0f\x93\xdd\xae\x1b\x84\xd2\x87\x85<\xfa\x15\xb5\x94\xd9\xdd\xbbi4\x99\xc4\x99\tm\xdfD[\xcb\x82V\xb0-\xc5"}\x14\x1ft\x1b|\x10YY\xbf\xa6\x93\xac\x1f\xe0\xbb3\xc9\x86l\xa8\x0b^\x18f\xc293\xf7\x9es\xf2\xe7\xe4\xc1\xda\x9aE\x83`/\xe6>\x93{\x81/$\xb8\xb0\xb3\x0b\xb0\x01\xf9\xc5\xe7\xbb\xe9\xd9|\x92\xaa\xd9e6~\x91}\x1cCxT\xf0`\xfe\xeb\\\x9dN\xf3\xebc\xf5\xf5*\xff\xf2\xe9\xee\xc77\xcb\xb2\xfeyc\x15\xbf\x93]\xbf\xcc\xae\xbe\xab\xc9M~\x96.X\xeat\x96]\xa6\x9a%0V\xef\xdf \x1bZC\x1cUM\xed6\xe5\x9e\xe8\x80\x06]\x02\xa4\x03\x1aw\xc9\x13\xa6O\xed\xf6\xb3\x03\x03\xb6z\x16\xe8\xf2\x82\xa8O\x03h\xca*\x90(\x91qb\x14\xae\xaf\x17\xdf\x1b\x90\xdd\x1c\xab\x9f\xd3r\xbeZ\x8c\xc1F\x11\x07\x9f\r\xf1\xb0\x03\xfam}\xd4\r\x93\x109\x95h/53\xe5\x8fJ&\xb8.\x04\xc8J\x18\x1e\xc2\xa3\x9a\xb2\xd4}\xd3\x05!\xb9!\xb5\x1a\xf0 b\xd2g\tZ\xab\xf9\xb0i\xe47\xa5T,\xe3G\x814uwi\x1ck\xc4.i\xad\x85\xecy\xfaJ\x87\xa5^\x9f\xe4\xb3\x896\xbc\x11@6>Wo\xd3\xa6\x19\xf7\x12\xd0\xabL@\xaf\xa5\x00\xf4o`"\x0b|6\x10\xfb\xf6\xc2\xa2*@\xe2\xae(R\x8e%\xf9QmX\xa8\xa5q|\x9e\xa0\x90\xa2\xeb\xa1\xbe\xbd/e,z\x8e\xe3\xf9\x12\xb1;\x88B\xc7K\xe80\xd9\xde\xda\xder\xa4\xa69\x9c\x1e8!\x15\x12\xb9\xd3\xa7\xac\x8f\xcc\xeb>\x15\x11#\xadb\xb3k\xb7\xab\x81\xc2\x1d\xa2\x9f`\x9eG#\xb2[\xc2x8\xc0X\xc2\xe3b\xf3#\x06T\x00\xf6\xee\xdd$*}\xf7\xfb\xe2\xc3\xfc\xf6v1\xfb\xffj4U\x1f*\x9f,\xeb/]\x82JA')))
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
