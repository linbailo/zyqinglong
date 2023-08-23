# -*- coding:utf-8 -*-
"""
美团 外卖红包
自行捉包把meituan.com里面的token(一般在请求头里)填到变量 meituanCookie 中,
多账号换行或&隔开
export meituanCookie="AgGZIgsYHyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

cron: 2,30 0,6,7,10,11,16,17,20,21 * * *
const $ = new Env("美团辅助");
"""
import os
import requests
import json
import urllib
import re

#print(os.getenv('meituanCookie').split("&"))


"""
ip = requests.post(url="https://mars.meituan.com/locate/v3/sdk/loc", json={"need_poi":-1,"need_openCity":1,"coord_type":"WGS84"}, headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 13; 2201122C Build/TKQ1.220807.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 XWEB/5223 MMWEBSDK/20230701 MMWEBID/2247 MicroMessenger/8.0.40.2420(0x28002837) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android"},verify = False).json()
if ip['code'] == 200 :
    actualLongitude = re.sub("\D","",str(ip['data']['location']['longitude']))
    actualLatitude = re.sub("\D","",str(ip['data']['location']['latitude']))
    print(actualLatitude,actualLongitude)
else:
    actualLongitude = 108306046
    actualLatitude = 22844505
    
"""    
for mt in os.getenv('meituanCookie').split("&"):
    print(mt)
    print('----------------------------------')
    cookie = f"token={mt};"
    headers = {"Cookie": cookie,"Content-Type":"application/json; charset=UTF-8","User-Agent":"Mozilla/5.0 (Linux; Android 6.0.1; OPPO R9s Plus Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36"}
    data = '{"gundamId":20625,"instanceId":"16807827427780.5322617288978357","actualLongitude":109445850,"actualLatitude":21598917,"needTj":true,"couponConfigIdOrderCommaString":"620969479,2189245219456,2237835510400,8818937234057,4298495230601,8540270559881,7782970229385,7783155696265,7783158907529,7283307184777,7285054243465,7285182431881,7281017291401,7349815083657,7458408104585,7457691927177,7282280694409,7956466762377,7955383321225,7955383386761,8368840966793,8524616172169,4987378139785,3458690974345,7904774587017,5513815065225,603844019,516213972,345822793,8026086900361","couponAllConfigIdOrderString":"620969479,2189245219456,2237835510400,8818937234057,4298495230601,8540270559881,7782970229385,7783155696265,7783158907529,7283307184777,7285054243465,7285182431881,7281017291401,7349815083657,7458408104585,7457691927177,7282280694409,7956466762377,7955383321225,7955383386761,8368840966793,8524616172169,4987378139785,3458690974345,7904774587017,5513815065225,603844019,516213972,345822793,8026086900361","rubikCouponKey":"PrizePool-200043026","platform":13,"app":-1,"h5Fingerprint":"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"}'
    #print(data)
    url = 'https://mediacps.meituan.com/gundam/gundamGrabV4?yodaReady=h5&csecplatform=4&csecversion=2.1.2&mtgsig=%7B%22a1%22%3A%221.1%22%2C%22a2%22%3A1692753460955%2C%22a3%22%3A%2235vu51434114550y078yyvv7zuvwvv9481z9w39v78x97958zywv5u71%22%2C%22a5%22%3A%22Za%2BQY648VDhGQNJbbdZT%2F%2BCflEuQEo1tKW%3D%3D%22%2C%22a6%22%3A%22hs1.4rMLnSSN7%2FTuDgTJbLhpKNOP7G6dUz8T2CCHjsw3G4Cm1GogYF2Pw6%2BWeYuXENVo9IJkBq%2BITu5MG7jo49mCQI%2Bbnf0QPtDeKTg2QQcrQAfI%3D%22%2C%22x0%22%3A4%2C%22d1%22%3A%22d8f6db0f9f33dc9a2e36191d47c50799%22%7D'
    b = requests.post(url=url,data=data,headers=headers,verify = False).json()
    #print(b['data']['allCoupons']);
    #print(b)
    for sj in b['data']['allCoupons']:
        print(f"{sj['couponName']}-{sj['amountLimit']}-{sj['couponAmount']}元-{sj['amountLimit']}-{sj['etime']}")
        
    print('----------')
    data = '{"gundamId":165001,"instanceId":"16926998783770.14811346236514056","actualLongitude":109445850,"actualLatitude":21598917,"needTj":true,"couponConfigIdOrderCommaString":"","couponAllConfigIdOrderString":"","rubikCouponKey":""}'
    b1 = requests.post(url="https://mediacps.meituan.com/gundam/gundamGrabV4?yodaReady=h5&csecplatform=4&csecversion=2.1.2&mtgsig=%7B%22a1%22%3A%221.1%22%2C%22a2%22%3A1692755483328%2C%22a3%22%3A%2235vu51434114550y078yyvv7zuvwvv9481z9w39v78x97958zywv5u71%22%2C%22a5%22%3A%22maGODW5rghjT3HUB%2Bm7wLWRXtsv5E1hL%22%2C%22a6%22%3A%22hs1.4rMLnSSN7%2FTuDgTJbLhpKNBcrC0AUmw7g0I9G2pDhxjhgYU7IQO8bMDHphX0D0dvqKC2D2NMNftU6YFJDSMky4t4g96IJaHl2pGxqs3dYDMc%3D%22%2C%22x0%22%3A4%2C%22d1%22%3A%228e737ffb9800b4da4216c3111673cb28%22%7D",data=data,headers=headers,verify = False).json()
    #print(b1['data']['allCoupons']);
    for sj in b1['data']['coupons']:
        print(f"{sj['couponName']}-{sj['amountLimit']}-{sj['couponAmount']}元-{sj['amountLimit']}-{sj['etime']}")
	
    print('----------------------------------')