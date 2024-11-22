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

cron: 0 0,7,12,17,21 * * *
const $ = new Env("T3打车");
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


# 发送通知消息
def send_notification_message(title):
    try:
        from sendNotify import send

        send(title, ''.join(all_print_list))
    except Exception as e:
        if e:
            print('发送通知消息失败！')


#初始化
print('============📣初始化📣============')
#版本

grayversion = 'P_i_2.0.4'

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
    data = {"cityCode":"450110","lat":lat,"lng":lng,"source":"4"}
    headers = {'token':token,'grayversion':grayversion,'riskdevicetoken':'67407d08R46xTQ9IvnfdLyB3WcsxNN7UWMJhYBW1'}
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
            myprint(f"任务：{taskName}-{lrw['data']['tips']}")
            data = {"eventType":taskSubType,"eventTime":int(time.time() * 1000),"taskUuid":taskUuid}
            ljl = requests.post(url='https://passenger.t3go.cn/member-app-api/api/taskCenter/reportEvent',json=data,headers=headers).json()
            if ljl['success'] == True:
                myprint(f"任务：{taskName}-已完成")





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