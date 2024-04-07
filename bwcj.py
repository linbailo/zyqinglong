"""
霸王茶姬签到

打开微信小程序抓webapi.qmai.cn里面的qm-user-token(一般在请求头里)填到变量bwcjck里面即可

支持多用户运行

多用户用&或者@隔开
例如账号1：10086 账号2： 1008611
则变量为10086&1008611
export bwcjck=""

cron: 0 0,7 * * *
const $ = new Env("霸王茶姬签到");
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

#分割变量
if 'bwcjck' in os.environ:
    bwcjck = re.split("@|&",os.environ.get("bwcjck"))
    print(f'查找到{len(bwcjck)}个账号')
else:
    bwcjck = ''
    print('无bwcjck变量')



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
        data = {"activityId":"947079313798000641","appid":"10086"}
        lq = requests.post(url='https://webapi.qmai.cn/web/cmk-center/sign/takePartInSign',data=data,headers=headers).json()
        if lq['message'] == 'ok':
            myprint(f"签到情况：获得{lq['data']['rewardDetailList'][0]['rewardName']}：{lq['data']['rewardDetailList'][0]['sendNum']}")
        else:
            myprint(f"签到情况：{lq['message']}")


def main():
    z = 1
    for ck in bwcjck:
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
        send_notification_message(title='霸王茶姬')  # 发送通知
    except Exception as e:
        print('小错误')
