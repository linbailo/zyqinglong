# -*- coding:utf-8 -*-
"""
美团 外卖红包
自行捉包把meituan.com里面的token(一般在请求头里)填到变量 meituanCookie 中,
多账号换行或&隔开
export meituanCookie="AgGZIgsYHyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

cron: 2 0,6,10,16,20 * * *
const $ = new Env("美团辅助");
"""
import os
import requests
import json
import urllib
import re

#print(os.getenv('meituanCookie').split("&"))



ip = requests.post(url="https://mars.meituan.com/locate/v3/sdk/loc", json={"need_poi":-1,"need_openCity":1,"coord_type":"WGS84"}, headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 13; 2201122C Build/TKQ1.220807.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 XWEB/5223 MMWEBSDK/20230701 MMWEBID/2247 MicroMessenger/8.0.40.2420(0x28002837) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android"}).json()

if ip['code'] == 200 :
    actualLongitude = re.sub("\D","",str(ip['data']['location']['longitude']))
    actualLatitude = re.sub("\D","",str(ip['data']['location']['latitude']))
    print(actualLatitude,actualLongitude)
else:
    actualLongitude = 108306046
    actualLatitude = 22844505
    
    
for mt in os.getenv('meituanCookie').split("&"):
    print(mt)
    print('----------------------------------')
    cookie = f"token={mt};"
    headers ={"Content-Type": "application/json; charset=UTF-8","Connection": "Keep-Alive","Charset": "UTF-8","Accept-Encoding": "gzip","cookie":cookie,"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36","content-type":"application/json;charset=UTF-8"}
    data = {"gundamId":20625,"instanceId":"16807827427780.5322617288978357","actualLongitude":actualLongitude,"actualLatitude":actualLatitude,"needTj":True,"couponConfigIdOrderCommaString":"620969479,2189245219456,2237835510400,4298495230601,8540270559881,7782970229385,7783155696265,7783158907529,7283307184777,7285054243465,7285182431881,7281017291401,7349815083657,7458408104585,7457691927177,7282280694409,7956466762377,7955383321225,7955383386761,8368840966793,8524616172169,4987378139785,3458690974345,7904774587017,5513815065225,603844019,516213972,345822793,8026086900361","couponAllConfigIdOrderString":"620969479,2189245219456,2237835510400,4298495230601,8540270559881,7782970229385,7783155696265,7783158907529,7283307184777,7285054243465,7285182431881,7281017291401,7349815083657,7458408104585,7457691927177,7282280694409,7956466762377,7955383321225,7955383386761,8368840966793,8524616172169,4987378139785,3458690974345,7904774587017,5513815065225,603844019,516213972,345822793,8026086900361","rubikCouponKey":"PrizePool-200043026","platform":13,"app":-1,"h5Fingerprint":"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"}
    url = "https://mediacps.meituan.com/gundam/gundamGrabV4?yodaReady=h5&csecplatform=4&csecversion=2.1.0"
    b = requests.post(url=url,json=data,headers=headers).json()
    #print(b['data']['allCoupons']);
    for sj in b['data']['allCoupons']:
        print(f"{sj['couponName']}-{sj['amountLimit']}-{sj['couponAmount']}元-{sj['amountLimit']}-{sj['etime']}")
        
    data = {"gundamId":165001,"instanceId":"16454483836900.5080374137278387","actualLongitude":actualLongitude,"actualLatitude":actualLatitude,"needTj":True,"couponConfigIdOrderCommaString":"511616988,511516780","couponAllConfigIdOrderString":"","rubikCouponKey":""}
    b1 = requests.post(url="https://mediacps.meituan.com/gundam/gundamGrabV4",json=data,headers=headers).json()
    #print(b1['data']['allCoupons']);
    for sj in b1['data']['coupons']:
        print(f"{sj['couponName']}-{sj['amountLimit']}-{sj['couponAmount']}元-{sj['amountLimit']}-{sj['etime']}")
	
    print('----------------------------------')