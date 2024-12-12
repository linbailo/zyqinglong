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

#初始化
print('============📣初始化📣============')
#版本
banappversion = '1.2.8'
github_file_name = 'dddc.py'
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
        from notify import send

        send(title, ''.join(all_print_list))
    except Exception as e:
        if e:
            print('发送通知消息失败！')

try:
    if didibb == True:
        print('📣📣📣📣📣📣📣📣📣📣📣📣📣')
        print('📣📣📣请更新版本：📣📣📣📣📣📣')
        print('📣https://raw.githubusercontent.com/linbailo/zyqinglong/main/dddc.py📣')
        print('📣📣📣📣📣📣📣📣📣📣📣📣📣')
    else:
        print(f"无版本更新：{banappversion}")
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
    token = ""
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