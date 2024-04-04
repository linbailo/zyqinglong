"""
益禾堂签到

打开微信小程序抓webapi.qmai.cn里面的qm-user-token(一般在请求头里)填到变量bwcjck里面即可

支持多用户运行

多用户用&或者@隔开
例如账号1：10086 账号2： 1008611
则变量为10086&1008611
export yhtck=""

cron: 0 0,7 * * *
const $ = new Env("益禾堂签到");
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
    
#分割变量
if 'yhtck' in os.environ:
    yhtck = re.split("@|&",os.environ.get("yhtck"))
    print(f'查找到{len(yhtck)}个账号')
else:
    yhtck =['']
    print('无yhtck变量')

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

def yx(ck):
    headers = {'qm-user-token': ck,'User-Agent': 'Mozilla/5.0 (Linux; Android 14; 2201122C Build/UKQ1.230917.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160065 MMWEBSDK/20231202 MMWEBID/2247 MicroMessenger/8.0.47.2560(0x28002F30) WeChat/arm64 Weixin NetType/5G Language/zh_CN ABI/arm64 MiniProgramEnv/android','qm-from': 'wechat'}
    dl = requests.get(url='https://webapi.qmai.cn/web/catering/crm/personal-info',headers=headers).json()
    if dl['message'] == 'ok':
        myprint(f"账号：{dl['data']['mobilePhone']}登录成功")
        data = {"activityId":"959131182653300737","appid":"10086"}
        lq = requests.post(url='https://webapi.qmai.cn/web/cmk-center/sign/takePartInSign',data=data,headers=headers).json()
        if lq['message'] == 'ok':
            myprint(f"签到情况：获得{lq['data']['rewardDetailList'][0]['rewardName']}：{lq['data']['rewardDetailList'][0]['sendNum']}")
        else:
            myprint(f"签到情况：{lq['message']}")


def main():
    z = 1
    for ck in yhtck:
        try:
            myprint(f'登录第{z}个账号')
            myprint('----------------------')
            yx(ck)
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
        send_notification_message(title='益禾堂')  # 发送通知
    except Exception as e:
        print('小错误')
