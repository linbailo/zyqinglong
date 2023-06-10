"""
变量：
ddgyToken: 必填，账号token，多账号换行或者@隔开，格式uid&token。uid可随便填，主要是方便区分账号用

青龙：捉任意game.xiaojukeji.com的包，把body里的uid和token用&连起来填到变量ddgyToken
uid其实不重要，只是用来区分token所属的账号，方便重写。手动捉包的话uid随便填都可以
多账号换行或者@隔开，重写多账号直接换号捉就行
export ddgyToken='uid&token'

cron: 0 0,7,17 * * *
const $ = new Env("滴滴打车");
"""
import requests
import re
import os
import time


#初始化
print('============📣初始化📣============')
appversion = '6.6.20'
print(f'小程序版本：{appversion}')
lat = '39.852399823026097'  #纬度
lng = '116.32055410011579'   #经度
print(f'经纬度默认设置：{lat},{lng}')


print('==================================')
#设置api
fuli ='https://ut.xiaojukeji.com/ut/welfare/api/action/dailySign'
youhui = 'https://union.didi.cn/api/v1.0/reward/receive'
guafen1 = 'https://ut.xiaojukeji.com/ut/welfare/api/home/divideData'
guafen2 = 'https://ut.xiaojukeji.com/ut/welfare/api/action/joinDivide'
guafen3 = 'https://ut.xiaojukeji.com/ut/welfare/api/action/event/report'
ttfuli = 'https://ut.xiaojukeji.com/ut/janitor/api/home/sign/index'
ttfuli1 = 'https://ut.xiaojukeji.com/ut/janitor/api/action/sign/do'
yao = 'https://api.didi.cn/webx/chapter/product/init'

def main(uid,token):
    print(f'正在执行账号：{uid}')
    chaxun(uid,token)
    try:
        diyi(uid,token)
    except Exception as e:
        print(e)
    guafen(uid,token)
    

def diyi(uid,token):
    print('--------领取优惠券--------')
    yq(uid,token)
    data = {"lang":"zh-CN","token":token,"access_key_id":9,"appversion":appversion,"channel":1100000009,"_ds":"","xpsid":"d04ccc4ce0c844e38c164ecc30711458","xpsid_root":"d04ccc4ce0c844e38c164ecc30711458","dsi":"877e066d7ce22ef07762fa42992227567393hvn1","source_id":"31806556232355840DT124787708487929856DT","product_type":"didi","city_id":33,"lng":"","lat":"","source_.from":"","env":{"dchn":"r2mda3z","newTicket":token,"latitude":"","longitude":"","model":"2201122C","fromChannel":"2","newAppid":"35009","openId":"","openIdType":"1","sceneId":"1037","isHitButton":True,"isOpenWeb":False,"timeCost":19908,"cityId":"33","xAxes":"167.60003662109375","yAxes":"480.0857849121094"},"req_env":"wx","dunion_callback":""}
    tijiao = requests.post(url=youhui, json=data).json()
    if tijiao['errmsg'] == 'success':
        for yh in tijiao['data']['rewards']:
            print(f"获取到{yh['coupon']['max_benefit_capacity']['value']}{yh['coupon']['max_benefit_capacity']['unit']} {yh['coupon']['name']} {yh['coupon']['remark']}")
    else:
        print(tijiao['errmsg'])
    print('--------福利中心签到------')
    data = {
    'lang' : 'zh-CN',
    'token' : token,
    'access_key_id' : 9,
    'appversion' : appversion,
    'channel' : 1100000002,
    '_ds' : '',
    'lat' : lat,
    'lng' : lng,
    'platform' : 'mp',
    'env' : r'{\"cityId\":\"33\",\"token\":\"\",\"longitude\":\"\",\"latitude\":\"\",\"appid\":\"30012\",\"fromChannel\":\"2\",\"wxScene\":1089,\"sceneId\":1089,\"openId\":\"\"}',
    'dchn' : 'W0dzOxO'
    }
    #print(data)
    tijiao = requests.post(url=fuli, json=data).json()
    if tijiao['errmsg'] == 'success':
        print(f"签到成功：获得 {tijiao['data']['subsidy_state']['subsidy_amount']} 福利金")
    else:
        print(tijiao['errmsg'])
        
    print('--------天天领券签到------')
    headers = {'didi-ticket': token,'content-type':'application/json'}
    data = {
    'lang' : 'zh-CN',
    'token' : token,
    'access_key_id' : 9,
    'appversion' : appversion,
    'channel' : 1100000002,
    '_ds' : '',
    'xpsid': '',
    'xpsid_root': '',
    'city_id': 33,
    'env': {'isHitButton': True,'newAppid': 35009,'userAgent': '','openId': '','model': '2201122C','wifi': 2,'timeCost': 222318}
    }
    #print(data)
    tijiao = requests.post(url=ttfuli, json=data, headers=headers).json()
    if tijiao['errmsg'] == 'success':
        print(f"获取id成功：{tijiao['data']['activity_id']}，{tijiao['data']['instance_id']}")
    else:
        print(tijiao['errmsg'])
    
    #print(tijiao)
    data = {
    'lang' : 'zh-CN',
    'token' : token,
    'access_key_id' : 9,
    'appversion' : appversion,
    'channel' : 1100000002,
    '_ds' : '',
    'xpsid': '0b3283547ec94f74ab4c8bdfbe61594a',
    'xpsid_root': 'a14839465b384932b8b548e19c9f6737',
    'activity_id': tijiao['data']['activity_id'],
    'instance_id': tijiao['data']['instance_id'],
    'city_id': 33,
    'env': {'isHitButton': True,'newAppid': 35009,'userAgent': '','openId': '','model': '2201122C','wifi': 2}
    }
    #print(data)
    tijiao = requests.post(url=ttfuli1, json=data, headers=headers).json()
    if tijiao['errmsg'] == 'success':
        print(f"天天领券签到：{tijiao['errmsg']}")
    else:
        print(tijiao['errmsg'])
        
   #天天领券限时抢
    print('----领点券使使----')
    data = {"lang":"zh-CN","access_key_id":9,"appversion":appversion,"channel":1100000002,"_ds":"","xpsid":"28a361bf9f2e456f9867be3cad4877e4","xpsid_root":"0fa1ac9f38d24e43a4a2616319942c88","root_xpsid":"0fa1ac9f38d24e43a4a2616319942c88","f_xpsid":"41345c97bc744b27a30c0dda8fbdfcba","xbiz":"240000","prod_key":"ut-coupon-center","dchn":"wE7poOA","xoid":"26243a0a-b1b9-44d3-b2ed-046016031b38","xenv":"wxmp","xpsid_from":"2e5ded46d7114ac4b0cf490619f5592d","xpsid_share":"","xspm_from":"ut-aggre-homepage.none.c460.none","xpos_from":{"pk":"ut-aggre-homepage"},"args":[{"dchn":"kkXgpzO","prod_key":"ut-limited-seckill","runtime_args":{"token":token,"lat":lat,"lng":lng,"env":{"dchn":"wE7poOA","newTicket":token,"model":"2201122C","fromChannel":"2","newAppid":"35009","openId":"","openIdType":"1","sceneId":"1089","isHitButton":False,"isOpenWeb":False,"timeCost":70665,"latitude":lat,"longitude":lng,"cityId":"","fromPage":"ut-coupon-center/views/index/index","xAxes":"","yAxes":""},"content-type":"application/json","Didi-Ticket":token,"ptf":"mp","city_id":33,"platform":"mp","x_test_user":{"key":281475120025923}}},{"dchn":"gL3E8qZ","prod_key":"ut-support-coupon","runtime_args":{"token":token,"lat":lat,"lng":lng,"env":{"dchn":"wE7poOA","newTicket":token,"model":"2201122C","fromChannel":"2","newAppid":"35009","openId":"","openIdType":"1","sceneId":"1089","isHitButton":False,"isOpenWeb":False,"timeCost":70666,"latitude":lat,"longitude":lng,"cityId":"","fromPage":"ut-coupon-center/views/index/index","xAxes":"","yAxes":""},"content-type":"application/json","Didi-Ticket":token,"ptf":"mp","city_id":33,"platform":"mp","x_test_user":{"key": 281475120025923}}}]}
    tijiao = requests.post(url="https://api.didi.cn/webx/chapter/page/batch/config", json=data, headers=headers).json()
    if tijiao['errmsg'] == 'success':
        for xuju in tijiao['data']['conf'][0]['strategy_data']['data']['seckill']:
            for xu in xuju['coupons']:
                activity_id = xu['activity_id']
                group_id = xu['group_id']
                group_date = xu['group_date']
                coupon_conf_id = xu['coupon_conf_id']
                data = {"lang":"zh-CN","token":token,"access_key_id":9,"appversion":appversion,"channel":1100000002,"_ds":"","xpsid":"d51af08a62ef4b43b1eb41deaae30379","xpsid_root":"0fa1ac9f38d24e43a4a2616319942c88","activity_id":activity_id,"group_id":group_id,"group_date":group_date,"coupon_conf_id":coupon_conf_id,"dchn":"wE7poOA","platform":"mp","city_id":33,"env":{"isHitButton":True,"newAppid":35009,"userAgent":"","openId":"","model":"2201122C","wifi":2,"timeCost":""}}
                ju = requests.post(url="https://ut.xiaojukeji.com/ut/janitor/api/action/coupon/bind", json=data, headers=headers).json()
                print(f"{xu['name']}（{xu['threshold_desc']}）：{ju['errmsg']}")
                time.sleep(1)
    print('------------------')
    
def guafen(uid,token):
    print('--------瓜瓜乐打卡--------')
    headers = {'didi-ticket': token,'content-type':'application/json'}
    """
    #没用的
    data = {
    'lang' : 'zh-CN',
    'token' : token,
    'access_key_id' : 9,
    'appversion' : appversion,
    'channel' : 1100000002,
    '_ds' : '',
    'lat' : lat,
    'lng' : lng,
    'platform' : 'mp',
    'env' : r'{\"cityId\":\"33\",\"token\":\"\",\"longitude\":\"\",\"latitude\":\"\",\"appid\":\"30012\",\"fromChannel\":\"2\",\"wxScene\":1089,\"sceneId\":1089,\"openId\":\"\"}',
    'type': 'navigation_click',
    'data': {'navigation_type': 'divide'}
    }
    tijiao = requests.post(url=guafen3, json=data,headers=headers).json()
    """
    #获取数据
    data = {
    'lang' : 'zh-CN',
    'token' : token,
    'access_key_id' : 9,
    'appversion' : appversion,
    'channel' : 1100000002,
    '_ds' : '',
    'lat' : lat,
    'lng' : lng,
    'platform' : 'mp',
    'env' : r'{\"cityId\":\"33\",\"token\":\"\",\"longitude\":\"\",\"latitude\":\"\",\"appid\":\"30012\",\"fromChannel\":\"2\",\"wxScene\":1089,\"sceneId\":1089,\"openId\":\"\"}'
    }
    shuju = requests.post(url=guafen1, json=data).json()
    #print(shuju)
    rqi = list(shuju['data']['divide_data']['divide'])
    zs = len(rqi) - 1
    activity_id = shuju['data']['divide_data']['divide'][rqi[zs]]['activity_id']
    task_id = shuju['data']['divide_data']['divide'][rqi[zs]]['task_id']
    print(f'获取到日期数据：{rqi}\n需要的日期：{rqi[zs]}\n报名瓜分activity_id数据：{activity_id}')
    #报名瓜分
    data = {
    'lang' : 'zh-CN',
    'token' : token,
    'access_key_id' : 9,
    'appversion' : appversion,
    'channel' : 1100000002,
    '_ds' : '',
    'lat' : lat,
    'lng' : lng,
    'platform' : 'mp',
    'env' : r'{\"cityId\":\"33\",\"token\":\"\",\"longitude\":\"\",\"latitude\":\"\",\"appid\":\"30012\",\"fromChannel\":\"2\",\"wxScene\":1089,\"sceneId\":1089,\"openId\":\"\"}',
    'activity_id' : activity_id,
    'count' : 1,
    'type' : 'ut_bonus'
    }
    tijiao = requests.post(url=guafen2, json=data).json()
    if tijiao['errmsg'] == 'success':
        print(f"报名瓜分：{tijiao['errmsg']}")
    else:
        print(tijiao['errmsg'])
    #参加瓜分
    
    activity_id = shuju['data']['divide_data']['divide'][rqi[0]]['activity_id']
    task_id = shuju['data']['divide_data']['divide'][rqi[0]]['task_id']
    print(f'获取到日期数据：{rqi}\n需要的日期：{rqi[0]}\n参加瓜分activity_id数据：{activity_id}')
    data = {
    'lang' : 'zh-CN',
    'token' : token,
    'access_key_id' : 9,
    'appversion' : appversion,
    'channel' : 1100000002,
    '_ds' : '',
    'lat' : lat,
    'lng' : lng,
    'platform' : 'mp',
    'env' : r'{\"cityId\":\"33\",\"token\":\"\",\"longitude\":\"\",\"latitude\":\"\",\"appid\":\"30012\",\"fromChannel\":\"2\",\"wxScene\":1089,\"sceneId\":1089,\"openId\":\"\"}',
    'activity_id' : activity_id,
    'task_id' : task_id
    }
    tijiao = requests.post(url='https://ut.xiaojukeji.com/ut/welfare/api/action/divideReward', json=data).json()
    if tijiao['errmsg'] == 'success':
        print(f"参加瓜分：{tijiao['errmsg']}")
    else:
        print(tijiao['errmsg'])
    #print(tijiao)
    #获取数据
    data = {
    'lang' : 'zh-CN',
    'token' : token,
    'access_key_id' : 9,
    'appversion' : appversion,
    'channel' : 1100000002,
    '_ds' : '',
    'lat' : lat,
    'lng' : lng,
    'platform' : 'mp',
    'env' : r'{\"cityId\":\"33\",\"token\":\"\",\"longitude\":\"\",\"latitude\":\"\",\"appid\":\"30012\",\"fromChannel\":\"2\",\"wxScene\":1089,\"sceneId\":1089,\"openId\":\"\"}'
    }
    shuju = requests.post(url=guafen1, json=data).json()
    #print(shuju)
    print('------')
    if '14点自动开奖' == shuju['data']['divide_data']['divide'][rqi[0]]['button']['text']:
        print(f"参加今日瓜分状态：成功-{shuju['data']['divide_data']['divide'][rqi[0]]['button']['text']}")
    elif '发奖了' == shuju['data']['divide_data']['divide'][rqi[0]]['button']['text']:
        print(f"参加今日瓜分状态：成功-{shuju['data']['divide_data']['divide'][rqi[0]]['button']['text']}")
    else:
        print(f"参加今日瓜分状态：失败")

    if '明天14点前访问' == shuju['data']['divide_data']['divide'][rqi[zs]]['button']['text']:
        print(f"参加今日瓜分状态：成功-{shuju['data']['divide_data']['divide'][rqi[zs]]['button']['text']}")
    else:
        print(f"参加明日瓜分状态：失败")
    print('------')
    
    
def chaxun(uid,token):
    print('--------福利金查询--------')
    cx = requests.get(url=f'https://rewards.xiaojukeji.com/loyalty_credit/bonus/getWelfareUsage4Wallet?token={token}&city_id=0').json()
    if 'ok' == cx['errmsg']:
        print(f"账号{uid}现在有福利金：{cx['data']['worth']}（可抵扣{cx['data']['worth']/100}元）\n{cx['data']['recent_expire_time']}过期福利金：{cx['data']['recent_expire_amount']}")
    else:
        print('查询失败')

def yq(uid,token):
    headers = {'content-type':'application/json'}
    data = {"lang": "zh-CN","access_key_id": 9,"appversion": appversion,"channel": 1100000005,"_ds": "","xpsid": "","xpsid_root": "","root_xpsid": "","f_xpsid": "","xbiz": "110105","prod_key": "wyc-cpc-v-three","dchn": "kaxm7er","xoid": "ddaf1498-d170-4f3b-bcc7-541d12ee782f","xenv": "wxmp","xpsid_share": "","xspm_from": "none.none.none.none","args": {"invoke_key": "default","key": 299073592885446,"runtime_args": {"scene": 1037,"token": token,"lat": lat,"lng": lng,"env": {"dchn": "kaxm7er","newTicket": token,"model": "2201122C","fromChannel": "2","newAppid": "35009","openId": "","openIdType": "1","sceneId": "1007","isHitButton": False,"isOpenWeb": False,"timeCost": 199,"latitude": lat,"longitude": lng,"cityId": "","fromPage": "wyc-cpc-v-three/views/index/index","xAxes": "","yAxes": ""},"dsi": "fb98de6169fea3440a3cd5208f899286923sekiu","ncc": True,"x_test_user": {"key": 299073592885446}}},"need_page_config": True,"need_share_config": True,"xpsid_from": ""}
    yy = requests.post(url=yao, json=data, headers=headers).json()

if __name__ == '__main__':
    uid = 1
    token = ""
    
    if 'ddgyToken' in os.environ:
        fen = os.environ.get("ddgyToken").split("@")
        print(f'查找到{len(fen)}个账号')
        print('==================================')
        for duo in fen:
            uid,token = duo.split("&")
            try:
                main(uid,token)
                print('============📣结束📣============')
            except Exception as e:
                raise e
    else:
        print('不存在青龙变量，本地运行')
        if uid == '' or token == '':
            print('本地账号密码为空')
            exit()
        else:
            try:
                main(uid,token)
            except Exception as e:
                raise e