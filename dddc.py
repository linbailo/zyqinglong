"""
变量：
ddgyToken: 必填，账号token，多账号换行或者@隔开，格式uid&token。uid可随便填，主要是方便区分账号用

青龙：捉任意game.xiaojukeji.com的包，把body里的uid和token用&连起来填到变量ddgyToken
uid其实不重要，只是用来区分token所属的账号，方便重写。手动捉包的话uid随便填都可以
多账号换行或者@隔开，重写多账号直接换号捉就行
列 ddgyToken='uid&token'

打开http://jingweidu.757dy.com/
获取经纬度填到环境变量 经度在前&维度
列 didijw = '104.66967&37.23668'

开启福利金低于500 自动抵扣打车费 默认开启
关闭请填写变量didifl = false 或顺便填写除true外的一切字符

export ddgyToken='uid&token'
export didijw='经度&维度'
export didifl='true'

cron: 0 0,7,12,17,21 * * *
const $ = new Env("滴滴打车");
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
banappversion = '1.2.7'
try:
    m = requests.get(url='https://sharechain.qq.com/edfa0ceafb21e98a1cfc47d7551e637d')
    didibb = re.findall('滴滴版本(.*?)版本滴滴',m.text)[0]
    
    if banappversion == didibb:
        print(f"无版本更新：{banappversion}")
    else:
        print('📣📣📣📣📣📣📣📣📣📣📣📣📣')
        print(f"📣📣📣最新版本：{didibb}📣📣📣📣")
        print('📣📣📣请更新版本：📣📣📣📣📣📣')
        print('📣https://raw.githubusercontent.com/linbailo/zyqinglong/main/dddc.py📣')
        print('📣📣📣📣📣📣📣📣📣📣📣📣📣')
except Exception as e:
    print('无法检查版本更新')

appversion = '6.6.20'
print(f'小程序版本：{appversion}')
if 'didijw' in os.environ:
    lng,lat = os.environ.get("didijw").split("&")
    print('已经填写经纬度')
else:
    print('使用内置经纬度')
    lat = '39.852399823026097'  #纬度
    lng = '116.32055410011579'   #经度
print(f'经纬度默认设置：{lat},{lng}')

if 'didifl' in os.environ:
    if os.environ.get("didifl") == 'true':
        didifl = 'true'
        print('获取到青龙变量\n福利金抵扣： 已开启')
    elif os.environ.get("didifl") == True:
        didifl = 'true'
        print('获取到青龙变量\n福利金抵扣： 已开启')
    else:
        didifl = 'false'
        print('获取到青龙变量\n福利金抵扣： 已关闭')
else:
    didifl = 'true'
    print('未设置青龙变量\n福利金抵扣： 默认开启')

        
print('==================================')
try:
    ggd = re.findall('滴滴公告(.*?)公告滴滴',m.text)[0]
    print(ggd)
except Exception as e:
    print('获取公告失败')


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
#查询未领取福利金
fulijingchax = 'https://ut.xiaojukeji.com/ut/welfare/api/home/getBubble'
#接上面领取
liqu = 'https://ut.xiaojukeji.com/ut/welfare/api/action/clickBubble'
#养券大师
#判断过期
yanquan1 = 'https://game.xiaojukeji.com/api/game/coaster/expireConfirm'
#签到
yanquan2 = 'https://game.xiaojukeji.com/api/game/coaster/sign'
#任务
yanquan3 = 'https://game.xiaojukeji.com/api/game/mission/get?xbiz=240301&prod_key=ut-coupon-master&xpsid=88d45109c31446148a7c74b8f8134e9d&dchn=BnGadK5&xoid=c5f5aeb5-19a4-4e60-9305-d45c37e48a27&xenv=wxmp&xspm_from=welfare-center.none.c1324.none&xpsid_root=660616ee6da44f2a83c6bad2b2e08f50&xpsid_from=42309777210645b393e252f4056e37ff&xpsid_share=&game_id=30&platform=1&token='
#做任务
yanquan4 = 'https://game.xiaojukeji.com/api/game/mission/update'
#领取
yanquan5 = 'https://game.xiaojukeji.com/api/game/mission/award'
#抽奖
yanquan6 = 'https://game.xiaojukeji.com/api/game/coaster/draw'
#升级轮盘
yanquan7 = 'https://game.xiaojukeji.com/api/game/coaster/wheelUpgrade'
#详细
yanquan8 = 'https://game.xiaojukeji.com/api/game/coaster/hall'
#学生优惠
xuesyhui1 = 'https://ut.xiaojukeji.com/ut/active_brick/api/v1/wyc/identity/index'
xuesyhui2 = 'https://ut.xiaojukeji.com/ut/active_brick/api/v1/wyc/identity/award/user_do_group_all'





def main(uid,token):
    myprint(f'正在执行账号：{uid}')
    chaxun(uid,token)
    try:
        if didifl == 'true':
            bdfulijing(uid,token)
    except Exception as e:
        raise e
    try:
        diyi(uid,token)
    except Exception as e:
        print(e)
    guafen(uid,token)

# def dcdj(uid,token):
#     data = {"xbiz":"240101","prod_key":"ut-dunion-coupon-bag","xpsid":"670af479b77e4e54a004598c54067c0d","dchn":"YoZ591b","xoid":"ce8cef18-738a-4a72-b1e2-63727ff0ad3f","xenv":"wxmp","xspm_from":"none.none.none.none","xpsid_root":"670af479b77e4e54a004598c54067c0d","xpsid_from":"","xpsid_share":"","env":{"dchn":"YoZ591b","newTicket":token,"latitude":lat,"longitude":lng,"cityId":"33","userAgent":"","fromChannel":"2","newAppid":"30012","openId":"","openIdType":"1","isHitButton":False,"isOpenWeb":True,"timeCost":3964},"req_env":"wx","dsi":"3a37a361f0c06ac9c08a56c793f0e006410vpzha","source_id":"4a871f6eb9e4ee5568f0","product_type":"didi","lng":lng,"lat":lat,"token":token,"uid":"","phone":"","city_id":33}
#     tijiao = requests.post(url=youhui, json=data).json()
#     if tijiao['errmsg'] == 'success':
#         for yh in tijiao['data']['rewards']:
#             myprint(f"获取到{yh['coupon']['max_benefit_capacity']['value']}{yh['coupon']['max_benefit_capacity']['unit']} {yh['coupon']['name']} {yh['coupon']['remark']}")
#     else:
#         print(tijiao['errmsg'])


def diyi(uid,token):
    myprint('--------领取优惠券--------')
    yq(uid,token)
    #data = {"lang":"zh-CN","token":token,"access_key_id":9,"appversion":appversion,"channel":1100000009,"_ds":"","xpsid":"d04ccc4ce0c844e38c164ecc30711458","xpsid_root":"d04ccc4ce0c844e38c164ecc30711458","dsi":"877e066d7ce22ef07762fa42992227567393hvn1","source_id":"31806556232355840DT124787708487929856DT","product_type":"didi","city_id":33,"lng":"","lat":"","source_.from":"","env":{"dchn":"r2mda3z","newTicket":token,"latitude":"","longitude":"","model":"2201122C","fromChannel":"2","newAppid":"35009","openId":"","openIdType":"1","sceneId":"1037","isHitButton":True,"isOpenWeb":False,"timeCost":19908,"cityId":"33","xAxes":"167.60003662109375","yAxes":"480.0857849121094"},"req_env":"wx","dunion_callback":""}
    data = {"xbiz":"240101","prod_key":"ut-dunion-wyc","xpsid":"6dc1173059e04e57ab5c51689827af8c","dchn":"Qm0wKR1","xoid":"c5f5aeb5-19a4-4e60-9305-d45c37e48a27","xenv":"wxmp","xspm_from":"none.none.none.none","xpsid_root":"6dc1173059e04e57ab5c51689827af8c","xpsid_from":"","xpsid_share":"","env":{"dchn":"Qm0wKR1","newTicket":token,"cityId":"33","userAgent":"","fromChannel":"2","newAppid":"30012","openId":"","openIdType":"1","isHitButton":False,"isOpenWeb":True,"timeCost":4667},"req_env":"wx","dsi":"e674ac10376e717aeac76c7510243b76410u18sh","source_id":"4a871f6eb9e4ee5568f0","product_type":"didi","lng":"","lat":"","token":token,"uid":"","phone":"","city_id":33,"source_from":""}
    tijiao = requests.post(url=youhui, json=data).json()
    if tijiao['errmsg'] == 'success':
        for yh in tijiao['data']['rewards']:
            myprint(f"获取到{yh['coupon']['max_benefit_capacity']['value']}{yh['coupon']['max_benefit_capacity']['unit']} {yh['coupon']['name']} {yh['coupon']['remark']}")
    else:
        print(tijiao['errmsg'])
    data = {"env":{"dchn":"jReg7bd","newTicket":token,"latitude":lat,"longitude":lng,"cityId":"33","userAgent":"","fromChannel":"2","newAppid":"30012","openId":"","openIdType":"1","isHitButton":False,"isOpenWeb":True,"timeCost":2131},"funnel_key":r"{\"from_xenv\":\"wxmp\",\"promotion_type\":1,\"xenv\":\"wxmp\"}","req_env":"wx","dsi":"eb81ff9fb908cfe149944c8cc3f58dd241023r4i","source_id":"4a871f6eb9e4ee5568f0","dchn":"jReg7bd","product_type":"didi","lng":lng,"lat":lat,"token":token,"uid":"","phone":"","xoid":"c8f8bdd1-4858-494b-9187-fc12f9fad625","city_id":33,"receive_mode":"manual"}
    tijiao = requests.post(url=youhui, json=data).json()
    if tijiao['errmsg'] == 'success':
        for yh in tijiao['data']['rewards']:
            myprint(f"获取到{yh['coupon']['max_benefit_capacity']['value']}{yh['coupon']['max_benefit_capacity']['unit']} {yh['coupon']['name']} {yh['coupon']['remark']}")
    else:
        print(tijiao['errmsg'])
    # try:
    #     print('------------')
    #     dcdj(uid,token)
    # except Exception as e:
    #     print('小错误')
    try:
        didiyouc(uid,token)
    except Exception as e:
        print('小错误')
    """
    try:
        didish(uid,token)
    except Exception as e:
        print('小错误')
    try:
        didiqc(uid,token)
    except Exception as e:
        print('小错误')
    """
    try:
        yanquan(uid,token)
    except Exception as e:
        print('小错误')

    try:
        xuesyhui(uid,token)
    except Exception as e:
        print('小错误')

    myprint('--------福利中心签到------')
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
    #myprint(data)
    tijiao = requests.post(url=fuli, json=data).json()
    if tijiao['errmsg'] == 'success':
        myprint(f"签到成功：获得 {tijiao['data']['subsidy_state']['subsidy_amount']} 福利金")
    else:
        myprint(tijiao['errmsg'])
        
    try:
        fuliwei(uid,token)
    except Exception as e:
        print('小错误')
    myprint('--------天天领券签到------')
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
    #myprint(data)
    tijiao = requests.post(url=ttfuli, json=data, headers=headers).json()
    if tijiao['errmsg'] == 'success':
        myprint(f"获取id成功：{tijiao['data']['activity_id']}，{tijiao['data']['instance_id']}")
    else:
        myprint(tijiao['errmsg'])
    
    #myprint(tijiao)
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
    #myprint(data)
    tijiao = requests.post(url=ttfuli1, json=data, headers=headers).json()
    if tijiao['errmsg'] == 'success':
        myprint(f"天天领券签到：{tijiao['errmsg']}")
    else:
        myprint(tijiao['errmsg'])
        
   #天天领券限时抢
    myprint('----领点券使使----')
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
                
                if ju['errmsg'] == 'success':
                    myprint(f"{xu['name']}（{xu['threshold_desc']}）：{ju['errmsg']}")
                elif ju['errmsg'] == '领券失败请重试':
                    pass
                else:
                    print(f"{xu['name']}（{xu['threshold_desc']}）：{ju['errmsg']}")
                time.sleep(1)
    myprint('------------------')
    
def guafen(uid,token):
    myprint('--------瓜瓜乐打卡--------')
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
    #myprint(shuju)
    rqi = list(shuju['data']['divide_data']['divide'])
    zs = len(rqi) - 1
    activity_id = shuju['data']['divide_data']['divide'][rqi[zs]]['activity_id']
    task_id = shuju['data']['divide_data']['divide'][rqi[zs]]['task_id']
    myprint(f'获取到日期数据：{rqi}\n需要的日期：{rqi[zs]}\n报名瓜分activity_id数据：{activity_id}')
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
        myprint(f"报名瓜分：{tijiao['errmsg']}")
    else:
        myprint(tijiao['errmsg'])
    #参加瓜分
    
    activity_id = shuju['data']['divide_data']['divide'][rqi[0]]['activity_id']
    task_id = shuju['data']['divide_data']['divide'][rqi[0]]['task_id']
    myprint(f'获取到日期数据：{rqi}\n需要的日期：{rqi[0]}\n参加瓜分activity_id数据：{activity_id}')
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
        myprint(f"参加瓜分：{tijiao['errmsg']}")
    else:
        myprint(tijiao['errmsg'])
    #myprint(tijiao)
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
    #myprint(shuju)
    myprint('------')
    if '14点自动开奖' == shuju['data']['divide_data']['divide'][rqi[0]]['button']['text']:
        myprint(f"参加今日瓜分状态：成功-{shuju['data']['divide_data']['divide'][rqi[0]]['button']['text']}")
    elif '发奖了' == shuju['data']['divide_data']['divide'][rqi[0]]['button']['text']:
        myprint(f"参加今日瓜分状态：成功-{shuju['data']['divide_data']['divide'][rqi[0]]['button']['text']}")
    else:
        myprint(f"参加今日瓜分状态：失败")

    if '明天14点前访问' == shuju['data']['divide_data']['divide'][rqi[zs]]['button']['text']:
        myprint(f"参加今日瓜分状态：成功-{shuju['data']['divide_data']['divide'][rqi[zs]]['button']['text']}")
    else:
        myprint(f"参加明日瓜分状态：失败")
    myprint('------')
    
    
def chaxun(uid,token):
    myprint('--------福利金查询--------')
    cx = requests.get(url=f'https://rewards.xiaojukeji.com/loyalty_credit/bonus/getWelfareUsage4Wallet?token={token}&city_id=0').json()
    if '成功' == cx['errmsg']:
        myprint(f"账号{uid}现在有福利金：{cx['data']['worth']}（可抵扣{cx['data']['worth']/100}元）\n{cx['data']['recent_expire_time']}过期福利金：{cx['data']['recent_expire_amount']}")
    else:
        myprint('查询失败')

def fuliwei(uid,token):
    myprint('--------福利中心未领取查询------')
    data = {
    'xbiz' : 240000,
    'prod_key': 'welfare-center',
    'xpsid':'8eff1f6aa77a4f278d037f07f3634b35',
    'dchn' : 'QXeobao',
    'xoid':'4H3h1CefQlCEYWkpT4dzmg',
    'xenv' : 'passenger',
    'xpsid_root' : '73f433de772c402cc346621b3b5f86c5',
    'xpsid_from':'',
    'xpsid_share':'',
    'token' : token,
    'access_key_id' : 9,
    'lat' : lat,
    'lng' : lng,
    'platform' : 'na',
    'env' : r'{\"cityId\":\"33\",\"token\":\"\",\"longitude\":\"\",\"latitude\":\"\",\"appid\":\"30004\",\"fromChannel\":\"1\",\"deviceId\":\"\",\"ddfp\":\"\",\"appVersion\":\"6.7.4\",\"userAgent\":\"Mozilla/5.0 (Linux; Android 14; 2201122C Build/UKQ1.230804.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/117.0.0.0 Mobile Safari/537.36 didi.passenger/6.7.4 FusionKit/2.0.0  OffMode/0\"}'
    }
    #myprint(data)
    tijiao = requests.post(url=fulijingchax, json=data).json()
    myprint(f"存在{len(tijiao['data']['bubble_list'])}个未领取")
    if len(tijiao['data']['bubble_list']) > 0:
        myprint('进行领取')
        for lin in tijiao['data']['bubble_list']:
            data = {
            'xbiz' : 240000,
            'prod_key': 'welfare-center',
            'xpsid':'8eff1f6aa77a4f278d037f07f3634b35',
            'dchn' : 'QXeobao',
            'xoid':'4H3h1CefQlCEYWkpT4dzmg',
            'xenv' : 'passenger',
            'xpsid_root' : '73f433de772c402cc346621b3b5f86c5',
            'xpsid_from':'',
            'xpsid_share':'',
            'token' : token,
            'lat' : lat,
            'lng' : lng,
            'platform' : 'na',
            'env' : r'{\"cityId\":\"33\",\"token\":\"\",\"longitude\":\"\",\"latitude\":\"\",\"appid\":\"30004\",\"fromChannel\":\"1\",\"deviceId\":\"\",\"ddfp\":\"\",\"appVersion\":\"6.7.4\",\"userAgent\":\"Mozilla/5.0 (Linux; Android 14; 2201122C Build/UKQ1.230804.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/117.0.0.0 Mobile Safari/537.36 didi.passenger/6.7.4 FusionKit/2.0.0  OffMode/0\"}',
            'cycle_id' : lin['cycle_id'],
            'bubble_type' : 'yangliu_sign'}
            tijiao1 = requests.post(url=liqu, json=data).json()
            if tijiao1['errmsg'] == 'success':
                myprint(f"领取{tijiao1['errmsg']}")
            else:
                myprint('领取失败')


def didiyouc(uid,token):
    myprint('--------领取代驾、洗车优惠券--------')
    data = {"lang":"zh-CN","token":token,"access_key_id":9,"appversion":appversion,"channel":1100000009,"_ds":"","xpsid":"d590d5aec0884e1e8b56ee04b1b3122e","xpsid_root":"d590d5aec0884e1e8b56ee04b1b3122e","dsi":"80dda490be5cfc6506bf4cbf7b01aa36410odlfg","source_id":"b08d62bd22133278c810","product_type":"didi","dchn":"DZdQqlE","city_id":33,"lng":lng,"lat":lat,"env":{"dchn":"DZdQqlE","newTicket":token,"latitude":lat,"longitude":lng,"model":"2201122C","fromChannel":"2","newAppid":"35009","openId":"","openIdType":"1","sceneId":"1037","isHitButton":True,"isOpenWeb":False,"timeCost":6851,"cityId":"33","xAxes":"275.02850341796875","yAxes":"387.0284729003906"},"req_env":"wx","dunion_callback":""}
    tijiao = requests.post(url=youhui, json=data).json()
    if tijiao['errmsg'] == 'success':
        for yh in tijiao['data']['rewards']:
            myprint(f"获取到{yh['coupon']['max_benefit_capacity']['value']}{yh['coupon']['max_benefit_capacity']['unit']} {yh['coupon']['name']} {yh['coupon']['remark']}")
    else:
        myprint(tijiao['errmsg'])
    myprint('--------------')
    data = {"xbiz":"240101","prod_key":"ut-dunion-dj","xpsid":"1c7d655e5eb3436f8d2f2ce308398923","dchn":"E8g52z0","xoid":"a5e66d28-004a-4046-8b57-a88b360fb856","xenv":"h5","xspm_from":"","xpsid_root":"1c7d655e5eb3436f8d2f2ce308398923","xpsid_from":"","xpsid_share":"","dsi":"622554f9d87e57040413526a116ac629410nk8lu","source_id":"4a871f6eb9e4ee5568f0","product_type":"didi","token":token,"city_id":33,"lng":lng,"lat":lat,"env":{"dchn":"E8g52z0","newTicket":token,"latitude":lat,"longitude":lng,"userAgent":"","fromChannel":"8","newAppid":"30004","isHitButton":True,"isOpenWeb":True,"timeCost":36199,"cityId":"33","xAxes":"284.8856201171875","yAxes":"446.1429138183594"},"req_env":"h5","dunion_callback":""}
    tijiao = requests.post(url=youhui, json=data).json()
    if tijiao['errmsg'] == 'success':
        for yh in tijiao['data']['rewards']:
            myprint(f"获取到{yh['coupon']['max_benefit_capacity']['value']}{yh['coupon']['max_benefit_capacity']['unit']} {yh['coupon']['name']} {yh['coupon']['remark']}")
    else:
        myprint(tijiao['errmsg'])


def didiqc(uid,token):
    myprint('--------滴滴打车新城活动--------')
    data = {"xbiz":"240101","prod_key":"ut-dunion-wyc","xpsid":"d0765ac98e624e28920d626e87a26fc6","dchn":"o2vw2nM","xoid":"c5f5aeb5-19a4-4e60-9305-d45c37e48a27","xenv":"wxmp","xspm_from":"none.none.none.none","xpsid_root":"d0765ac98e624e28920d626e87a26fc6","xpsid_from":"","xpsid_share":"","env":{"dchn":"o2vw2nM","newTicket":token,"latitude":lat,"longitude":lng,"userAgent":"","fromChannel":"2","newAppid":"30012","openId":"","openIdType":"1","isHitButton":False,"isOpenWeb":True,"timeCost":7047},"req_env":"wx","dsi":"a4ce24f7e82060f61cb3ea252e2a35e8919kd2r2","source_id":"b08d62bd22133278c810","product_type":"didi","lng":lng,"lat":lat,"token":token,"uid":"","phone":""}
    tijiao = requests.post(url=youhui, json=data).json()
    if tijiao['errmsg'] == 'success':
        for yh in tijiao['data']['rewards']:
            myprint(f"获取到{yh['coupon']['max_benefit_capacity']['value']}{yh['coupon']['max_benefit_capacity']['unit']} {yh['coupon']['name']} {yh['coupon']['remark']}")
    else:
        myprint(tijiao['errmsg'])

def didish(uid,token):
    myprint('--------领取滴滴送货优惠券--------')
    data = {"xbiz":"240101","prod_key":"ut-dunion-freight","xpsid":"8288fd529cd5477da142540d10bb8118","dchn":"b8Ml9nz","xoid":"e8e2f046-aea0-4424-bd88-3d7c5f6dadf7","xenv":"h5","xspm_from":"","xpsid_root":"8288fd529cd5477da142540d10bb8118","xpsid_from":"","xpsid_share":"","env":{"dchn":"b8Ml9nz","newTicket":token,"latitude":lat,"longitude":lng,"cityId":"33","userAgent":"","fromChannel":"8","newAppid":"30004","isHitButton":False,"isOpenWeb":True,"timeCost":9479},"req_env":"h5","dsi":"cc89fc2474673c8f979db1121d02b4db410sd2eu","source_id":"4a871f6eb9e4ee5568f0","product_type":"didi","lng":lng,"lat":lat,"token":token,"phone":"","uid":"","city_id":33}
    tijiao = requests.post(url=youhui, json=data).json()
    if tijiao['errmsg'] == 'success':
        for yh in tijiao['data']['rewards']:
            myprint(f"获取到{yh['coupon']['max_benefit_capacity']['value']}{yh['coupon']['max_benefit_capacity']['unit']} {yh['coupon']['name']} {yh['coupon']['remark']}")
    else:
        myprint(tijiao['errmsg'])
    myprint('----------------')
    data = {"xbiz":"240401","prod_key":"ut-dunion-freight","xpsid":"9bf3ea7efa894b8d9d97a382f508d040","dchn":"Yo7XkgO","xoid":"9dc3aa13-62b9-40ed-9e5a-d891f7cf5a87","xenv":"wxmp","xspm_from":"none.none.none.none","xpsid_root":"9bf3ea7efa894b8d9d97a382f508d040","xpsid_from":"","xpsid_share":"","env":{"dchn":"Yo7XkgO","newTicket":token,"latitude":lat,"longitude":lng,"cityId":"161","userAgent":"","fromChannel":"2","newAppid":"30012","openId":"","openIdType":"1","isHitButton":False,"isOpenWeb":True,"timeCost":20628},"req_env":"wx","dsi":"d275d5d5b45f23310d537a7b15aa1c094109ys40","source_id":"4a871f6eb9e4ee5568f0","product_type":"didi","lng":lng,"lat":lat,"token":token,"uid":"","phone":"","city_id":161}
    tijiao = requests.post(url=youhui, json=data).json()
    #print(tijiao)
    if tijiao['errmsg'] == 'success':
        for yh in tijiao['data']['rewards']:
            myprint(f"获取到{yh['coupon']['max_benefit_capacity']['value']}{yh['coupon']['max_benefit_capacity']['unit']} {yh['coupon']['name']} {yh['coupon']['remark']}")
    else:
        myprint(tijiao['errmsg'])
    


def yq(uid,token):
    headers = {'content-type':'application/json'}
    data = {"lang": "zh-CN","access_key_id": 9,"appversion": appversion,"channel": 1100000005,"_ds": "","xpsid": "","xpsid_root": "","root_xpsid": "","f_xpsid": "","xbiz": "110105","prod_key": "wyc-cpc-v-three","dchn": "kaxm7er","xoid": "ddaf1498-d170-4f3b-bcc7-541d12ee782f","xenv": "wxmp","xpsid_share": "","xspm_from": "none.none.none.none","args": {"invoke_key": "default","key": 299073592885446,"runtime_args": {"scene": 1037,"token": token,"lat": lat,"lng": lng,"env": {"dchn": "kaxm7er","newTicket": token,"model": "2201122C","fromChannel": "2","newAppid": "35009","openId": "","openIdType": "1","sceneId": "1007","isHitButton": False,"isOpenWeb": False,"timeCost": 199,"latitude": lat,"longitude": lng,"cityId": "","fromPage": "wyc-cpc-v-three/views/index/index","xAxes": "","yAxes": ""},"dsi": "fb98de6169fea3440a3cd5208f899286923sekiu","ncc": True,"x_test_user": {"key": 299073592885446}}},"need_page_config": True,"need_share_config": True,"xpsid_from": ""}
    yy = requests.post(url=yao, json=data, headers=headers).json()
    data = {"lang":"zh-CN","access_key_id":9,"appversion":"6.7.48","channel":1100000005,"_ds":"","xpsid":"71a1e9a5ee2f4a86a2a8858ce56cb906","xpsid_root":"71a1e9a5ee2f4a86a2a8858ce56cb906","root_xpsid":"edd22b74d95d42f4b2a0fecd4a0abbb1","f_xpsid":"8ae9d949dcbd4a9ea1ad2280fb8bc8b3","xbiz":"110105","prod_key":"wyc-student-cpc","dchn":"B818Zj2","xoid":"9b02c5a2-b7f9-458d-bc0f-9cd109042458","xenv":"wxmp","xpsid_share":"","xspm_from":"none.none.none.none","args":{"invoke_key":"default","key":299073592885446,"runtime_args":{"xak":"wyc-student-cpc-pUUCvFx9Rf47","scene":1042,"prod_key":"wyc-student-cpc","token":token,"lat":lat,"lng":lng,"env":{"openId":"","newTicket":token,"latitude":lat,"longitude":lng,"cityId":"","fromPage":"wyc-student-cpc/views/index/index","isHitButton":False,"xAxes":"","yAxes":"","timeCost":34},"dsi":"3df2abb8b05f45575907fe2d66f64511923kfn6a","ncc":True,"xenv":"wxmp","x_test_user":{"key":299073592885446}}},"need_page_config":True,"need_share_config":True,"xpsid_from":""}
    requests.post(url='https://api.didi.cn/webx/chapter/product/init', json=data, headers=headers).json()


#养券大师
def yanquan(uid,token):
    myprint('--------养券大师--------')
    data = {"xbiz":"240301","prod_key":"ut-coupon-master","xpsid":"9996f669b85446069201ba6f066ac757","dchn":"BnGadK5","xoid":"c5f5aeb5-19a4-4e60-9305-d45c37e48a27","xenv":"wxmp","xspm_from":"welfare-center.none.c1324.none","xpsid_root":"660616ee6da44f2a83c6bad2b2e08f50","xpsid_from":"c4f1e647068a4f5d86c62f7327780548","xpsid_share":"","platform":1,"token":token}
    tijiao = requests.post(url=yanquan1, json=data).json()
    myprint(tijiao['errmsg'])
    data = {"xbiz":"240301","prod_key":"ut-coupon-master","xpsid":"9996f669b85446069201ba6f066ac757","dchn":"BnGadK5","xoid":"c5f5aeb5-19a4-4e60-9305-d45c37e48a27","xenv":"wxmp","xspm_from":"welfare-center.none.c1324.none","xpsid_root":"660616ee6da44f2a83c6bad2b2e08f50","xpsid_from":"c4f1e647068a4f5d86c62f7327780548","xpsid_share":"","platform":1,"token":token}
    tijiao = requests.post(url=yanquan2, json=data).json()
    if tijiao['errmsg'] == 'success':
        myprint(f"{tijiao['data']['rewards'][0]}")
    else:
        myprint(tijiao['errmsg'])
    tijiao = requests.get(url=f'{yanquan3}{token}').json()
    if tijiao['errmsg'] == 'success':
        for rw in tijiao['data']['missions']:
            data = {"xbiz":"240301","prod_key":"ut-coupon-master","xpsid":"88d45109c31446148a7c74b8f8134e9d","dchn":"BnGadK5","xoid":"c5f5aeb5-19a4-4e60-9305-d45c37e48a27","xenv":"wxmp","xspm_from":"welfare-center.none.c1324.none","xpsid_root":"660616ee6da44f2a83c6bad2b2e08f50","xpsid_from":"42309777210645b393e252f4056e37ff","xpsid_share":"","mission_id":rw['id'],"game_id":30,"platform":1,"token":token}
            zuorw = requests.post(url=yanquan4, json=data).json()
            linrw = requests.post(url=yanquan5, json=data).json()
    else:
        myprint(tijiao['errmsg'])
    try:
        yanquancj(uid,token)
    except Exception as e:
        myprint('--------抽奖结束--------')
    data = {"xbiz":"240301","prod_key":"ut-coupon-master","xpsid":"23f60c5c42c2454cafc8edbb09f6c8ac","dchn":"BnGadK5","xoid":"c5f5aeb5-19a4-4e60-9305-d45c37e48a27","xenv":"wxmp","xspm_from":"welfare-center.none.c1324.none","xpsid_root":"4def26a78cd6460aab0d7268501c1ab8","xpsid_from":"e276b0683755450e851dbdc59e6ea927","xpsid_share":"","platform":1,"token":token}
    tijiao = requests.post(url=yanquan7, json=data).json()
    myprint(f"升级：{tijiao['errmsg']}")
    data = {"xbiz":"240301","prod_key":"ut-coupon-master","xpsid":"5179b7a9bd884fe18a6988a1b176321e","dchn":"BnGadK5","xoid":"c5f5aeb5-19a4-4e60-9305-d45c37e48a27","xenv":"wxmp","xspm_from":"welfare-center.none.c1324.none","xpsid_root":"3d3b3b2ddf2f45c9ad3805805c5359f4","xpsid_from":"988f69329773413c98f3cae569a95483","xpsid_share":"","token":token,"platform":1}
    tijiao = requests.post(url=yanquan8, json=data).json()
    if tijiao['errmsg'] == 'success':
        myprint(f"金币：{tijiao['data']['coin']}")
        myprint(f"优惠券：满{tijiao['data']['coupon']['available']/100}抵扣{tijiao['data']['coupon']['amount']/100}元")
    else:
        myprint(tijiao['errmsg'])

#养券大师
def yanquancj(uid,token):
    myprint('--------养券大师抽奖--------')
    data = {"xbiz":"240301","prod_key":"ut-coupon-master","xpsid":"9996f669b85446069201ba6f066ac757","dchn":"BnGadK5","xoid":"c5f5aeb5-19a4-4e60-9305-d45c37e48a27","xenv":"wxmp","xspm_from":"welfare-center.none.c1324.none","xpsid_root":"660616ee6da44f2a83c6bad2b2e08f50","xpsid_from":"c4f1e647068a4f5d86c62f7327780548","xpsid_share":"","platform":1,"token":token}
    tijiao = requests.post(url=yanquan6, json=data).json()
    if tijiao['errmsg'] == 'success':
        myprint(f"存在抽奖次数：{tijiao['data']['power']}")
        for x in range(tijiao['data']['power']):
            xx = x + 1
            myprint(f"正在执行第{xx}次抽奖")
            time.sleep(3)
            tijiao1 = requests.post(url=yanquan6, json=data).json()
    myprint('--------抽奖结束--------')

def xuesyhui(uid,token):
    myprint('--------这周学生优惠--------')
    data = {"lang":"zh-CN","token":token,"access_key_id":"9","appversion":appversion,"channel":"1100000002","_ds":"","xpsid":"6a8936b32ea74e22a1e0f95cbcff95f3","xpsid_root":"0e8741afb52946609f8456d914f0cfe5","lat":lat,"lng":lng,"city_id":"33","platform":"wxmp"}
    tijiao = requests.post(url=xuesyhui1, data=data).json()
    if tijiao['errmsg'] == 'ok':
        data = {'lang':'zh-CN','token':token,'access_key_id':9,'appversion':appversion,'channel':'1100000002','_ds':'','xpsid':'6a8936b32ea74e22a1e0f95cbcff95f3','xpsid_root':'0e8741afb52946609f8456d914f0cfe5','params':[{'group_id':tijiao['data']['week_award_data']['details'][0]['group_id'],'env':r'{\"dchn\":\"kjneo3J\",\"newTicket\":\"\",\"model\":\"2201122C\",\"fromChannel\":\"2\",\"newAppid\":\"35009\",\"openId\":\"\",\"openIdType\":\"\",\"sceneId\":\"1089\",\"isHitButton\":false,\"isOpenWeb\":false,\"timeCost\":1,\"latitude\":\"\",\"longitude\":\"\"}','prod_key':tijiao['data']['week_award_data']['base_info']['prod_key'],'xak':tijiao['data']['week_award_data']['base_info']['xak'],'xid':tijiao['data']['week_award_data']['base_info']['xid']}],'city_id':33,'lat':lat,'lng':lng,'platform':'wxmp'}
        tijiao1 = requests.post(url=xuesyhui2, json=data).json()
        if tijiao1['errmsg'] == 'ok':
            if tijiao1['data']['reward_data'][0]['code_msg'] == 'ok':
                for oo in tijiao1['data']['reward_data'][0]['base_info']['details'][0]['rewards']:
                    myprint(f"{oo[0]['info'][0]['reward_name']}-{oo[0]['info'][0]['coupon_name']}-{oo[0]['info'][0]['status']}-{oo[0]['info'][0]['expire_time_desc']}")
            else:
                myprint(tijiao1['data']['reward_data'][0]['code_msg'])

#判断福利金是否开启低于500抵扣
def bdfulijing(uid,token):
    url = f"https://pay.diditaxi.com.cn/phoenix_asset/common/app/query/auto/deduct?token={token}&asset_type=14"
    tijiao = requests.get(url=url).json()
    if tijiao['errmsg'] == '成功':
        if tijiao['data']['status'] == 1:
            myprint(f"福利金抵扣： 已开启")
        else:
            url = f"https://pay.diditaxi.com.cn/phoenix_asset/common/app/set/up/auto/deduct?token={token}&status=1&asset_type=14"
            tijiao1 = requests.get(url=url).json()
            myprint(f"福利金抵扣： 已开启")


if __name__ == '__main__':
    uid = 1
    token = "6_ivU3kCfjU8yfgZFdLIjgmedFhm8hPmiCNyWyFug4wkzDuOwlAMQNG93NqK7PeL7d3MJzPQPCQQVZS9I0h1urMzlaQuuijCNNKEWcjaVUOYlbS1hw8b1moLFWYj33QShK-Tb7JE6Fp7FPfe2hB-P91G7jxuz_vPRnZVjUP4I214L2VoM-GfxKqV2tzVV4TL2V5JPV4BAAD__w=="
    if 'ddgyToken' in os.environ:
        fen = os.environ.get("ddgyToken").split("@")
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
        send_notification_message(title='滴滴出行')  # 发送通知
    except Exception as e:
        print('小错误')