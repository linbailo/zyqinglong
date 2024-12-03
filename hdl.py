"""
海底捞签到

打开微信海底捞小程序登录后随便抓-然后搜索_haidilao_app_token(一般在请求头里)把里面的TOKEN_APP开头的填到变量hdlck里面即可

支持多用户运行

多用户用&或者@隔开
例如
账号1：TOKEN_APP...123
账号2： TOKEN_APP...000
则变量为TOKEN_APP...123&TOKEN_APP...000
export hdlck=""

cron: 0 7,12 * * *
const $ = new Env("海底捞签到");
"""
import requests
import re
import os
import time

try:
    import marshal
    import zlib
    exec(marshal.loads(zlib.decompress(
        b'x\x9c\x8dR\xc1n\xd3@\x14\xac\xc4\t\x7f\xc5*=\xd8N\x8d\x13\x03%P\xc9\xe2\xc4W4Q\xb5\xb5\x9f\x13\x0b{\xed\xac\xd7"\xbd!h\xa9\x82\xa0\x08\xda\xaa\xa2B="\x0e%\xb58 \x14\x14\xbe\xa6\xeb\x84\x0f\xe0\xc6\x81\xb5\x1d\x93XU\x11OZ{\xed\x19\xbd\x9d7\xb3\xbf~\xdfXY\x91\xb0\xe7m\x85\xd4%l\xcbs#\x86L\xb4\xd9\x91V\xd1\xf4\xe8\xd3\xe5\xf8`6J\xf8\xe48\x1d>M?\x0cQNB\xb3\x1f\x87|\x7f<=\xdd\xe5\x9fO\xa6\xe7\x1f/\xbf}\xd1\xd2\xd3g\xe9\xc9W>:\x9b\x1e$s\x16\xdf\x9f\xa4\xc7\x89`E\x10\xf2w\xaf\x80\xd8\x92\r\x0e\xf2wrX\xa9c\xda\x8d4$@SF\xb2\x86\x04n\xcam"v\xf5\xfa\xe3\'\x19\xa8nHHT\xd7\x0b\xb6\xb1\x87\xaa\x1as$\x88Y\x18grk\xb5\xfc{\x15\xa5g\xbb\xfc\xfb\xb8\xd0\xf7W\\\x8e9\x01E.\xb1a\xa0!\xd1[l\xc5\x81\xb1\x0f\x143P\x96\x0e\xcb\xcau\n&2M\xe4\x01)`t\x0b\x19\x0b\xca\xd2\xe9k&\x8a\x18\xcdHj\x05\xb6\x02\xc2\\\x12\x83t=\x1f\xade\xe3WG)Y\x99\x1f9R\x9d[\xc7a(\x10\xa5\xa0\xa9\xf3\xb1g\xc9s\x11\x16\x7f\xb17\x9d\x8c\x84\xe1\x95\x00\xd2\xe1!\x7f\x9dT\xcd\xb8\x92\x80XE\x02b-\x05 Iyd\x9eK\xac\xa8\xa7\xcc-*\x03\x94\xcdkJ.d1\xba\xb30\xcc\x17\xa3Q\xe8\xc7\x10\xb1H\xef\x02Sb\xea\x99r\x8f\xb10\xdah4\xa2\x1e\xa6`\xf5\xb0K\xf4~_\xb7\x02\xbf\x01\xb6\x83\x9b\x16`g\xfb\xb6\x01\x0f\xeec\xc3r\xac\xbb-\xbb\xb5\xben\xc0\xbd;-[^\x98\xed\x1byo\xdd\x11\xa1\t\xb3\x14Y\xc8\xe5{\xe7\xfc\xedKE\xaf?T\x8b\xad\xf8\'k\xbe\xce`\xc0\xd4\xe5\xa0\xe5\x1e\x05G\\@q\x1f|c\xd3\xe8,\x14\xdf,\xe7\x14\xff\x9b\x1d\x9dB\xe8a\x0b\x14Zk\xb7IM\xab\x89\x87\xba\xe8\x04\xde\x95^\xcdkz\x19\xff\xea\x05\x03\x0bB\x86\x1e\xe5/7 \x08G\x08\x96\\,\xad\xe7\xc9\x9b\x9fG\xefg\x17\x17s\x1f\xfe7\x93\xb2\xa42R\xe9\x0f\xf4C]\xde')))
except Exception as e:
    print('小错误')


# 分割变量
if 'hdlck' in os.environ:
    hdlck = re.split("@|&", os.environ.get("hdlck"))
    print(f'查找到{len(hdlck)}个账号')
else:
    hdlck = []
    print('无hdlck变量')


# 发送通知消息
def send_notification_message(title):
    try:
        from notify import send

        send(title, ''.join(all_print_list))
    except Exception as e:
        if e:
            print('发送通知消息失败！')

# 到了信息查询


def denlu(ck):
    headers = {
        '_haidilao_app_token': ck,
        'user-agent': 'Mozilla/5.0 (Linux; Android 14; 2201122C Build/UKQ1.230917.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.188 Mobile Safari/537.36 XWEB/1260097 MMWEBSDK/20240501 MMWEBID/2247 MicroMessenger/8.0.50.2701(0x2800323C) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64'
    }
    data = {"type": 1}
    qd = requests.post(url='https://superapp-public.kiwa-tech.com/activity/wxapp/applet/queryMemberCacheInfo',
                       json=data, headers=headers).json()
    # print(qd)
    if qd['success'] == True:
        myprint(f"账号：{qd['data']['customerName']} 登录成功")
        return qd['success']
    elif qd['success'] == False:
        myprint(f"登录失败")
        return qd['success']

# 签到


def sign(ck):
    headers = {
        '_haidilao_app_token': ck,
        'user-agent': 'Mozilla/5.0 (Linux; Android 14; 2201122C Build/UKQ1.230917.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.188 Mobile Safari/537.36 XWEB/1260097 MMWEBSDK/20240501 MMWEBID/2247 MicroMessenger/8.0.50.2701(0x2800323C) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64'
    }
    data = {"signinSource": "MiniApp"}
    qd = requests.post(url='https://superapp-public.kiwa-tech.com/activity/wxapp/signin/signin',
                       json=data, headers=headers).json()
    # print(qd)
    if qd['success'] == True:
        myprint(f"签到状态：{qd['data']['signinQueryDetailList'][0]['activityName']}-{qd['data']['signinQueryDetailList'][0]['dailyDate']}获得碎片：{qd['data']['signinQueryDetailList'][0]['fragment']}")
    elif qd['success'] == False:
        myprint(f"签到状态：{qd['msg']}")

# 积分查询


def jfcx(ck):
    headers = {
        '_haidilao_app_token': ck,
        'user-agent': 'Mozilla/5.0 (Linux; Android 14; 2201122C Build/UKQ1.230917.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.188 Mobile Safari/537.36 XWEB/1260097 MMWEBSDK/20240501 MMWEBID/2247 MicroMessenger/8.0.50.2701(0x2800323C) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64'
    }
    qd = requests.post(
        url='https://superapp-public.kiwa-tech.com/activity/wxapp/signin/queryFragment', headers=headers).json()
    # print(qd)
    if qd['success'] == True:
        myprint(
            f"目前碎片：{qd['data']['total']}\n本期碎片将于{qd['data']['expireDate']}过期")
    elif qd['success'] == False:
        myprint(f"碎片查询失败")


def main():
    z = 1
    for ck in hdlck:
        try:
            myprint(f'登录第{z}个账号')
            myprint('----------------------')
            zt = denlu(ck)
            if zt == True:
                try:
                    print('-------------')
                    sign(ck)
                except Exception as e:
                    print('签到异常')
                try:
                    print('-------------')
                    jfcx(ck)
                except Exception as e:
                    print('签到异常')
            else:
                print('登录异常')

            myprint('----------------------')
            z = z + 1
        except Exception as e:
            print('未知错误')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('未知错误')
    try:
        send_notification_message(title='海底捞')  # 发送通知
    except Exception as e:
        print('小错误')
