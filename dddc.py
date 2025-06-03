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
banappversion = '1.2.9'
github_file_name = 'dddc.py'
sjgx = '2025-06-04T21:30:11.000+08:00'
try:
    import marshal
    import zlib
    exec(marshal.loads(zlib.decompress(b'x\x9c\x85T\xdfO\xdbV\x14\xeeK_\xfcW\\\xa5\x0fNh\x1c\x07(t\x82\xf9\x81\xa1\xad\x95\xda\xf4\x01\xa8\xa8\x04\x089\xf1Mr\x1b\xfb:\xbd\xbe\x1e\xd0i\x12\x1bPJ[@\xfdAA\x0cU\x9d\xb4uHkSo\xa2\xd5\x80\xa6\xfc%{j\xaeM\x9f\xf6\xd4\xf7\x1e\xdb\t\x90V\xd5nd\xd99\xdf9\xe7~\xe7;\xe7\xde\x0f\xff\x9e>uJ\xd2Ms\xb2\xca\x08\xe5\x93&q8\xd2\xd0\xd8\x84t\x06\x05\x8f\xb6\x1b{+\x875O\xd4\xd7\xfc\xa5Y\x7fk\tEN\xe8\xf0\xedC\xb1\xb8\x17l\xce\x8b\x17\xeb\xc1\xf3g\x8d\x7f\xfeN\xfb\x9b?\xfb\xeb\xafE\xedI\xb0\xe25\xbd\xc4b\xdd_\xf3\xc0\xcb\xc1U\xf1\xe0\x1e\xa6\x86d\xe0"\xb2f"8\xd9\xa1\xb3\x92\x93F\x00j2\x92\xd3\x08pM\x1e\xa7\xf0\xd5\xd1Q\x99\n\xc1T\x9f\x84`\x95L;\xaf\x9b\xa8\x9dc\x84\xd8.\xaf\xba!\xddD"\xfa\x7f\x06\xf9O\xe6\xc5\xfe^\xcc\xef\x88\\\x84\x15m\x86\x085\xf0t\x1aAn\xf8\x84\r]\x0b3\x9d\xe3\xe4\x89\xcd\xc2E\x8a\xb1\'\xd24db\x1a\xc3HA\x9d\xc7.\'v?\xab!\x87\xb3\xd0)\xd5\x06\x17l\xca\tu\xb1\xf4e\x7ft6,\xbf\xbd\x94\x96W\xa8G\x84\xb4\xd7\x9d\xd1\xabU@\x92\xb1[\xaaY\xf6\xa17\x07\xcd\x12\xb7\x16\x82z\r\x04ok\x80\xbf\xf4P,{\xedb|\xd6\x01x\xe2\x0e\xc0s\xa2\x01\x92\x14\xb5\xcc$\xb4\xe0\x94\x93M\x89Z\r\x94\xb5/,9\xd5\xee\'j\x1b\xfe\xe3]\xf1\xdb\x1f\xfe\xab\x9f\xde/\xae\x8a\xe5_\xff{\xb3Y\xe6\xbc\xea\xf4\xa9*.\xebvE\xcf\x14lKu\xd4\xf3\xe6\x85a\xcb\xc9\r\x8d\xd3q\xea\xaf?\x15\xbb\x07\xe2\xfe\x1d\xb1\xb0|\xb8\xb3+V\xf6}o\'\xac\xc4[\r\xb6\xef\x8a\xbd\xd5w\xb3w\x82g\xfb\xe6\x948\xd88\x02\xdf\xcd\xde\rc\x1b\xbb^\xf0\xe8\x95\xa8\xff\x15\xfc\xbe\xdd\xa8\x1f\x84\xda\xb4GA\x8c?\xf74v\x80\x18\xff%\xb0Zk\xbc\t\x8d=JWV,\xcc\x85i\xba\xe1-^\xce\x8b\x83?\xdf\xcf>\xf8<C\x08\xdd\xf6D\xed5d\xf8\xb4\xe6\xff\xd1\xc6ef\x174[n\xa9P\xa9\x94\x08/\xbb\xf9H\x07\x90;\xaf\x13\xd3Vo\xce\xdc \x14\xc6\x9f\x96T\xce0V\x00\xb4\x08W\x08-\xda\xaa\xa5\x13*G\xb9\xf2y\xc8\xc4\xf0\r\x17;\xdc\xc9\x940OBv-\xdc!]\xc6\xba\x81\x99\xa3\xfd \x0f\xc24b\xca\x95\x91\x99*\x96\xfbd\x98"\x93\x14tNl\xaa^wl8u\xf2\x10.b\x86\x19\x80-R\'(\x01>\x8c\x0b\xca`Y\xb9\xaa\x83G\xe2\x8a\xcd\xd5\x81\xd47L\xa7F\xa2\xff{-\xf1U"\x8d\x12\x83ef[\xc4\xb5"KgWoh\xcb\x91\x02\xb3\x1d\xbb\xc8\xd1\xb7F\t\x1f!\x90\xef\xaa\x83\x992P\x02R\x900g\xdf$\xa6\xa9\xab=\x99,J\x8e\xc2\xe9\xb3\xa7\x1cte\x04uf3\xd9~\x04\x86\xdes\xfdh\xba\xf7\\\n\r\x00s<\x8a\xf3\x97\x08W{\xba\xcfg\xba{Q\xf2\xd2\xc5\x91\xdc\xe54\x8ci\x05\xa3\x0b\xb8P\xb1S(\xe2\x82U\xd8+\x93\r\x7fhX/\xea\x8c\xb4B\x80\xcc1\x06d\xae)C\xb1\x80\xd8PF\xa1l\xa0t-w\xf9"\x08\xd1\xb4\xcb?\xa62\xa1P\xc9\xb8\x7fN\x014\xcf\xe7\xc7b\x89&\x8b\xc4\xc4\x93T\xb7\xf0\xc4\x98l\xc0\x8d"OH\xcd\x8b\xc4\xb9^\x9aF_ka\xc0\xf1\xed\xd1\x9c\x91`\xe9\xb6\xbf\xf5\\\xbc\xd8\x10[\xdb\xfe/;\xfec\x0f\xce\xc5\x08s\xb1||\x930\xcc]FQh\x8dl\xd8tp\xdf\xa7\xe8w:X#\xa3d\x10\x83D\x03\xd1:\xb3\xd2G\xcc\xcdF\xa9')))
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
    #guafen(uid,token)

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
    data = {"env":{"dchn":"YQwoRwR","newTicket":token,"latitude":lat,"longitude":lng,"cityId":"33","userAgent":"","fromChannel":"2","newAppid":"30012","openId":"","openIdType":"1","isHitButton":False,"isOpenWeb":True,"timeCost":1645},"funnel_key":r"{\"from_xenv\":\"wxmp\",\"promotion_type\":1,\"xenv\":\"wxmp\"}","req_env":"wx","dsi":"3c08f7474e087aa3ee2874d9065f41f2897t73wy","source_id":"235675jutuike202563","dchn":"YQwoRwR","product_type":"didi","lng":lng,"lat":lat,"lang":"zh-CN","token":token,"uid":"","phone":"","xoid":"348d1abb-70ca-466e-80ca-a1f540b7563b","city_id":33,"receive_mode":"manual"}
    # data = {"env":{"dchn":"rYe2XGg","newTicket":token,"latitude":lat,"longitude":lng,"cityId":"33","userAgent":"","fromChannel":"2","newAppid":"30012","openId":"","openIdType":"1","isHitButton":False,"isOpenWeb":True,"timeCost":1264},"funnel_key":r"{\"from_xenv\":\"wxmp\",\"promotion_type\":1,\"xenv\":\"wxmp\"}","req_env":"wx","dsi":"4aeb703c11ae9c3740b4fc80490104cf897gfsiv","source_id":"235675jutuikegithub","dchn":"rYe2XGg","product_type":"didi","lng":lng,"lat":lat,"token":token,"uid":"","phone":"","xoid":"c8f8bdd1-4858-494b-9187-fc12f9fad625","city_id":33,"source_from":"","receive_mode":"manual"}
    tijiao = requests.post(url=youhui, json=data).json()
    if tijiao['errmsg'] == 'success':
        for yh in tijiao['data']['rewards']:
            myprint(f"获取到{yh['coupon']['max_benefit_capacity']['value']}{yh['coupon']['max_benefit_capacity']['unit']} {yh['coupon']['name']} {yh['coupon']['remark']}")
    else:
        print(tijiao['errmsg'])

    data = {"env":{"dchn":"onX67WR","newTicket":token,"latitude":lat,"longitude":lng,"cityId":"33","userAgent":"","fromChannel":"2","newAppid":"30012","openId":"","openIdType":"1","isHitButton":False,"isOpenWeb":True,"timeCost":1986},"funnel_key":r"{\"from_xenv\":\"wxmp\",\"promotion_type\":1,\"xenv\":\"wxmp\"}","req_env":"wx","dsi":"df719d5bd8b863bd0ef58cb5fcf6d307897xgpbw","source_id":"235675jutuike202563","dchn":"onX67WR","product_type":"didi","lng":lng,"lat":lat,"lang":"zh-CN","token":token,"uid":"","phone":"","xoid":"348d1abb-70ca-466e-80ca-a1f540b7563b","city_id":33,"receive_mode":"manual"}
    tijiao = requests.post(url=youhui, json=data).json()
    if tijiao['errmsg'] == 'success':
        for yh in tijiao['data']['rewards']:
            myprint(f"获取到{yh['coupon']['max_benefit_capacity']['value']}{yh['coupon']['max_benefit_capacity']['unit']} {yh['coupon']['name']} {yh['coupon']['remark']}")
    else:
        print(tijiao['errmsg'])
        
    data = {"env":{"dchn":"YRBvlwe","newTicket":token,"latitude":lat,"longitude":lng,"cityId":"33","userAgent":"","fromChannel":"2","newAppid":"30012","openId":"","openIdType":"1","isHitButton":False,"isOpenWeb":True,"timeCost":12237},"funnel_key":r"{\"from_xenv\":\"wxmp\",\"promotion_type\":1,\"xenv\":\"wxmp\"}","req_env":"wx","dsi":"b58415bc51f44774bd1f6a055b2420ce897k129e","source_id":"235675jutuike202563","dchn":"YRBvlwe","product_type":"didi","lng":lng,"lat":lat,"lang":"zh-CN","token":token,"uid":"","phone":"","xoid":"348d1abb-70ca-466e-80ca-a1f540b7563b","city_id":33,"receive_mode":"manual"}
    tijiao = requests.post(url=youhui, json=data).json()
    if tijiao['errmsg'] == 'success':
        for yh in tijiao['data']['rewards']:
            myprint(f"获取到{yh['coupon']['max_benefit_capacity']['value']}{yh['coupon']['max_benefit_capacity']['unit']} {yh['coupon']['name']} {yh['coupon']['remark']}")
    else:
        print(tijiao['errmsg'])
    data = {"env":{"dchn":"ZkJXzn1","newTicket":token,"latitude":lat,"longitude":lng,"cityId":"33","userAgent":"","fromChannel":"2","newAppid":"30012","openId":"","openIdType":"1","isHitButton":False,"isOpenWeb":True,"timeCost":4263},"funnel_key":r"{\"from_xenv\":\"wxmp\",\"promotion_type\":1,\"xenv\":\"wxmp\"}","req_env":"wx","dsi":"0aaae828f5041931b1cdefc9c6d70b2489737lv1","source_id":"235675jutuike202563","dchn":"ZkJXzn1","product_type":"didi","lng":lng,"lat":lat,"lang":"zh-CN","token":token,"uid":"","phone":"","xoid":"348d1abb-70ca-466e-80ca-a1f540b7563b","city_id":33,"receive_mode":"manual"}
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

    # try:
    #     xuesyhui(uid,token)
    # except Exception as e:
    #     print('小错误')

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
    data = {"env":{"dchn":"YRBvlwe","newTicket":token,"latitude":lat,"longitude":lng,"cityId":"33","userAgent":"","fromChannel":"2","newAppid":"30012","openId":"","openIdType":"1","isHitButton":False,"isOpenWeb":True,"timeCost":5508},"funnel_key":r"{\"from_xenv\":\"wxmp\",\"promotion_type\":1,\"xenv\":\"wxmp\"}","req_env":"wx","dsi":"b58415bc51f44774bd1f6a055b2420ce897k129e","source_id":"235675jutuike202563","dchn":"YRBvlwe","product_type":"didi","lng":lng,"lat":lat,"lang":"zh-CN","token":token,"uid":"","phone":"","xoid":"348d1abb-70ca-466e-80ca-a1f540b7563b","city_id":33,"receive_mode":"manual"}
    tijiao = requests.post(url=youhui, json=data).json()
    if tijiao['errmsg'] == 'success':
        for yh in tijiao['data']['rewards']:
            myprint(f"获取到{yh['coupon']['max_benefit_capacity']['value']}{yh['coupon']['max_benefit_capacity']['unit']} {yh['coupon']['name']} {yh['coupon']['remark']}")
    else:
        myprint(tijiao['errmsg'])
    myprint('--------------')
    data = {"env":{"dchn":"Bew6qD2","newTicket":token,"latitude":lat,"longitude":lng,"cityId":"33","userAgent":"","fromChannel":"2","newAppid":"30012","openId":"","openIdType":"1","isHitButton":False,"isOpenWeb":True,"timeCost":1452},"req_env":"wx","dsi":"b4d6e5282182bcfddd733329383446aa89722xuf","source_id":"235675jutuike202563","dchn":"Bew6qD2","product_type":"didi","lng":lng,"lat":lat,"token":token,"uid":"","phone":"","xoid":"348d1abb-70ca-466e-80ca-a1f540b7563b","city_id":33}
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