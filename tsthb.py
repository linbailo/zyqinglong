"""
塔斯汀汉堡签到

打开微信小程序抓sss-web.tastientech.com里面的user-token(一般在headers里)填到变量tsthbck里面即可

支持多用户运行

多用户用&或者@隔开
例如账号1：10086 账号2： 1008611
则变量为10086&1008611
export tsthbck=""

cron: 55 1,9,16 * * *
const $ = new Env("塔斯汀汉堡");
"""
import requests
import re
import os
import time
#初始化
print('============📣初始化📣============')
#版本
github_file_name = 'tsthb.py'
sjgx = '2025-02-17T21:30:11.000+08:00'
version = '1.46.8'

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
        print(f'📣https://raw.githubusercontent.com/linbailo/zyqinglong/main/{github_file_name}📣')
        print('📣📣📣📣📣📣📣📣📣📣📣📣📣')
    else:
        print(f"无版本更新")
except Exception as e:
    print('无法检查版本更新')


#分割变量
if 'tsthbck' in os.environ:
    tsthbck = re.split("@|&",os.environ.get("tsthbck"))
    print(f'查找到{len(tsthbck)}个账号')
else:
    tsthbck =['']
    print('无tsthbck变量')



def yx(ck):
    
    headers = {'user-token':ck,'version':version,'channel':'1'}
    dl = requests.get(url='https://sss-web.tastientech.com/api/intelligence/member/getMemberDetail',headers=headers).json()
    if dl['code'] == 200:
        myprint(f"账号：{dl['result']['phone']}登录成功")
        phone = dl['result']['phone']
        data = {"activityId":56,"memberName":"","memberPhone":phone}
        lq = requests.post(url='https://sss-web.tastientech.com/api/sign/member/signV2',json=data,headers=headers).json()
        if lq['code'] == 200:
            if lq['result']['rewardInfoList'][0]['rewardName'] == None:
                myprint(f"签到情况：获得 {lq['result']['rewardInfoList'][0]['point']} 积分")
            else:
                myprint(f"签到情况：获得 {lq['result']['rewardInfoList'][0]['rewardName']}")
        else:
            myprint(f"签到情况：{lq['msg']}")



def main():
    z = 1
    for ck in tsthbck:
        try:
            myprint(f'登录第{z}个账号')
            myprint('----------------------')
            yx(ck)
            myprint('----------------------')
            z = z + 1
        except Exception as e:
            print(e)
            print('未知错误')

if __name__ == '__main__':
    print('====================')
    try:
        main()
    except Exception as e:
        print('未知错误')
    print('====================')
    try:
        send_notification_message(title='塔斯汀汉堡')  # 发送通知
    except Exception as e:
        print('小错误')
    
