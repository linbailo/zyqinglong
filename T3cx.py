"""
变量：
T3Token: 必填，账号token，多账号换行或者@隔开，格式uid&token。uid可随便填，主要是方便区分账号用

青龙：打开T3小程序捉任意passenger.t3go.cn的包，把headers里的uid和token用&连起来填到变量T3Token
uid其实不重要，只是用来区分token所属的账号，方便重写。手动捉包的话uid随便填都可以

多账号换行或者@隔开，重写多账号直接换号捉就行
列 T3Token='uid&token'

打开http://jingweidu.757dy.com/
获取经纬度填到环境变量 经度在前&维度
列 didijw = '104.66967&37.23668'


export T3Token='uid&token'
export didijw='经度&维度'

cron: 0 0,7,12 * * *
const $ = new Env("T3打车");
"""
import requests
import re
import os
import time

#初始化
print('============📣初始化📣============')
#版本
github_file_name = 'T3cx.py'
sjgx = '2024-11-24T21:30:11.000+08:00'
grayversion = 'P_i_2.0.4'
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
        print('📣https://raw.githubusercontent.com/linbailo/zyqinglong/main/T3cx.py.py📣')
        print('📣📣📣📣📣📣📣📣📣📣📣📣📣')
    else:
        print(f"无版本更新")
except Exception as e:
    print('无法检查版本更新')




if 'didijw' in os.environ:
    lng,lat = os.environ.get("didijw").split("&")
    print('已经填写经纬度')
else:
    print('使用内置经纬度')
    lat = '39.852399823026097'  #纬度
    lng = '116.32055410011579'   #经度
print(f'经纬度默认设置：{lat},{lng}')




def main(uid,token):
    myprint(f'正在执行账号：{uid}')
    
    try:
        qd(uid,token)
    except Exception as e:
        print(e)
    try:
        yhq(uid,token)
    except Exception as e:
        print(e)
    try:
        sqzx(uid,token)
    except Exception as e:
        print(e)

# def dcdj(uid,token):
#     data = {"xbiz":"240101","prod_key":"ut-dunion-coupon-bag","xpsid":"670af479b77e4e54a004598c54067c0d","dchn":"YoZ591b","xoid":"ce8cef18-738a-4a72-b1e2-63727ff0ad3f","xenv":"wxmp","xspm_from":"none.none.none.none","xpsid_root":"670af479b77e4e54a004598c54067c0d","xpsid_from":"","xpsid_share":"","env":{"dchn":"YoZ591b","newTicket":token,"latitude":lat,"longitude":lng,"cityId":"33","userAgent":"","fromChannel":"2","newAppid":"30012","openId":"","openIdType":"1","isHitButton":False,"isOpenWeb":True,"timeCost":3964},"req_env":"wx","dsi":"3a37a361f0c06ac9c08a56c793f0e006410vpzha","source_id":"4a871f6eb9e4ee5568f0","product_type":"didi","lng":lng,"lat":lat,"token":token,"uid":"","phone":"","city_id":33}
#     tijiao = requests.post(url=youhui, json=data).json()
#     if tijiao['errmsg'] == 'success':
#         for yh in tijiao['data']['rewards']:
#             myprint(f"获取到{yh['coupon']['max_benefit_capacity']['value']}{yh['coupon']['max_benefit_capacity']['unit']} {yh['coupon']['name']} {yh['coupon']['remark']}")
#     else:
#         print(tijiao['errmsg'])


#签到
def qd(uid,token):
    myprint('--------签到状态--------')
    n = requests.get(url='https://dingxiang.t3go.cn:8663/udid/c1',headers={'Param': 'j10086'}).json()
    riskdevicetoken = n['data']
    data = {"cityCode":"450110","lat":lat,"lng":lng,"source":"4"}
    headers = {'token':token,'grayversion':grayversion,'riskdevicetoken':riskdevicetoken}
    qd = requests.post(url='https://passenger.t3go.cn/member-app-api/api/v1/sign/signIn',json=data,headers=headers).json()
    if qd['success'] == True:
        myprint(f"{qd['data'][0]['signDate']}-签到成功获取到：{qd['data'][0]['rewardNum']}福气\n连续签到：{qd['data'][0]['signDays']}天")
    else:
        myprint(f"签到状态：{qd['msg']}")


#领优惠券
def yhq(uid,token):
    myprint('--------领取优惠券--------')
    data = {"activityId":"d75c7b77d3c642d9b084f1052347d2a3","originTerminal":"wx","landingPageType":"LM","extParam":{"participationWay":"RECALL","sourceId":"4a871f6eb9e4ee5568f0","originTerminal":"wx","cityCode":"450110","lat":lat,"lng":lng}}
    headers = {'token':token,'grayversion':grayversion}
    yq = requests.post(url='https://passenger.t3go.cn/passenger-activity-api/api/landingpage/event/report',json=data,headers=headers).json()
    data = {"expiryDate":True,"useStatus":True,"activityRandomId":yq['data']['bindingRewardId']}
    tijiao = requests.post(url='https://passenger.t3go.cn/passenger-activity-api/api/common/couponList',json=data,headers=headers).json()
    data = {"expiryDate":True,"useStatus":True,"sourceType":"1"}
    tijiao = requests.post(url='https://passenger.t3go.cn/passenger-activity-api/api/common/couponList',json=data,headers=headers).json()
    
    if tijiao['data'] != []:
        for i in tijiao['data']:
            myprint(f"获取到：{i['couponName']}-{i['discount']}折-最多抵扣{i['highestMoney']}元")
    else:
        myprint('今日已领取')
        print(tijiao['data'])

    

#省钱中心
def sqzx(uid,token):
    #查询任务
    myprint('--------做任务--------')
    data = {"areaCode":"450110"}
    headers = {'token':token,'grayversion':grayversion}
    tijiao = requests.post(url='https://passenger.t3go.cn/member-app-api/api/v1/sm/v3/pageCfg',data=data,headers=headers).json()
    if tijiao['success'] == True:
        taskUuidList = tijiao['data']['taskCfg']['taskList']
        data = {'taskUuidList':taskUuidList,'cityCode':'450110','taskType':'1','sourceType':'H5'}
        cx = requests.post(url='https://passenger.t3go.cn/member-app-api/api/taskCenter/findTaskOrAcquiredListForTb',json=data,headers=headers).json()
        for i in cx['data']:
            #名字
            taskName = i['taskName']
            taskSubType = i['subTaskList'][0]['taskSubType']
            taskUuid = i['taskUuid']
            #领任务
            data = {"receiveType":"TASK_PACKAGE","taskUuid":taskUuid,"cityCode":"450110"}
            lrw = requests.post(url='https://passenger.t3go.cn/member-app-api/api/taskCenter/receive',json=data,headers=headers).json()
            if lrw['data']['tips'] != '网络异常':
                myprint(f"任务：{taskName}-{lrw['data']['tips']}")
                data = {"eventType":taskSubType,"eventTime":int(time.time() * 1000),"taskUuid":taskUuid}
                ljl = requests.post(url='https://passenger.t3go.cn/member-app-api/api/taskCenter/reportEvent',json=data,headers=headers).json()
                if ljl['success'] == True:
                    myprint(f"任务：{taskName}-已完成")
        myprint(f"今日所有任务已完成")





if __name__ == '__main__':
    uid = 1
    token = ""
    if 'T3Token' in os.environ:
        fen = os.environ.get("T3Token").split("@")
        myprint(f'查找到{len(fen)}个账号')
        myprint('==================================')
        for duo in fen:
            time.sleep(6)
            uid,token = duo.split("&")
            try:
                main(uid,token)
                myprint('============📣结束📣============')
            except Exception as e:
                myprint('小错误')
    else:
        myprint('不存在青龙变量，本地运行')
        if uid == '' or token == '':
            myprint('本地账号密码为空')
            exit()
        else:
            try:
                main(uid,token)
            except Exception as e:
                myprint('小错误')
    try:
        print('==================================')
        send_notification_message(title='T3出行')  # 发送通知
    except Exception as e:
        print('小错误')