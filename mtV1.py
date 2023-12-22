# -*- coding:utf-8 -*-
"""
美团 外卖红包
自行捉包把meituan.com里面的token(一般在请求头里)填到变量 meituanCookie 中,
多账号换行或&隔开
export meituanCookie="AgGZIgsYHyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

cron: 0,30 * * * *
const $ = new Env("美团领杂券");
"""
import os
import requests
import json
import urllib
import re
from urllib import parse

def qid(mt):
    print('----------------------------------')
    try:
        waimai1(mt)
    except Exception as e:
        print(f'小错误')
    try:
        waimai2(mt)
    except Exception as e:
        print(f'小错误')
    try:
        chaos(mt)
    except Exception as e:
        print(f'小错误')
    try:
        zha(mt)
    except Exception as e:
        print(f'小错误')
    print('----------------------------------')

def waimai1(mt):
    cookie = f"token={mt};"
    headers = {"Cookie": cookie,
    "X-Requested-With":"com.tencent.mm",
    "Sec-Fetch-Site":"same-site",
    "Sec-Fetch-Mode":"cors",
    "Sec-Fetch-Dest":"empty",
    "Content-Type":"application/json;",
    "User-Agent":"Mozilla/5.0 (Linux; Android 14; 2201122C Build/UKQ1.230917.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160027 MMWEBSDK/20231105 MMWEBID/2247 MicroMessenger/8.0.44.2502(0x28002C37) WeChat/arm64 Weixin Android Tablet NetType/WIFI Language/zh_CN ABI/arm64 miniProgram/wxde8ac0a21135c07d"}
    url = 'https://mediacps.meituan.com/gundam/gundamGrabV4?yodaReady=h5&csecplatform=4&csecversion=2.3.1&mtgsig=%7B%22a1%22%3A%221.1%22%2C%22a2%22%3A1703249523466%2C%22a3%22%3A%22u436y57v4uv65y51y20yv956632wx5vu81x1w780y1297958vwuzvu5v%22%2C%22a5%22%3A%22lIYW1HgxopF98LvEVowp6h1I3207fr9g1W%3D%3D%22%2C%22a6%22%3A%22hs1.4D%2BodbiVB7g3xIIk%2BJcao4367F%2FHiHrYL9d5MvFu55TLFtZU%2Bc91Lo1vmfrGRD%2FUSliJhKOh6JFEZKxhfYgPoEzlYZZf1tx4iH3%2B2xrnnb68%3D%22%2C%22x0%22%3A4%2C%22d1%22%3A%22fc25f050f47d9367e537cb050858632f%22%7D'
    data = '{"gundamId":531693,"instanceId":"16970942475020.14201015290378827","actualLongitude":108196730,"actualLatitude":23159088,"needTj":true,"couponConfigIdOrderCommaString":"620969479,2189245219456,2237835510400,4298495230601,13612419842697,13612970082953,13612152259209,13612970345097,7390907925129,7622642631305,7606006907529,604064706,604064705,4987378139785,345822793","couponAllConfigIdOrderString":"620969479,2189245219456,2237835510400,4298495230601,13612419842697,13612970082953,13612152259209,13612970345097,7390907925129,7622642631305,7606006907529,604064706,604064705,4987378139785,345822793","platform":13,"app":-1,"h5Fingerprint":"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"}'
    requests.options(url)
    b = requests.post(url=url,data=data,headers=headers).json()
    print(f'[{z}]账号登录成功')
    for sj in b['data']['allCoupons']:
        print(f"{sj['couponName']}-{sj['amountLimit']}-{sj['couponAmount']}元-{sj['amountLimit']}-{sj['etime']}")
    print('----------')


def waimai2(mt):
    cookie = f"token={mt};"
    headers = {"Cookie": cookie,
    "X-Requested-With":"com.tencent.mm",
    "Sec-Fetch-Site":"same-site",
    "Sec-Fetch-Mode":"cors",
    "Sec-Fetch-Dest":"empty",
    "Content-Type":"application/json;",
    "User-Agent":"Mozilla/5.0 (Linux; Android 14; 2201122C Build/UKQ1.230917.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160027 MMWEBSDK/20231105 MMWEBID/2247 MicroMessenger/8.0.44.2502(0x28002C37) WeChat/arm64 Weixin Android Tablet NetType/WIFI Language/zh_CN ABI/arm64 miniProgram/wxde8ac0a21135c07d"}
    url = 'https://mediacps.meituan.com/gundam/gundamGrabV4?yodaReady=h5&csecplatform=4&csecversion=2.3.1&mtgsig=%7B%22a1%22%3A%221.1%22%2C%22a2%22%3A1703249931058%2C%22a3%22%3A%22u436y57v4uv65y51y20yv956632wx5vu81x1w780y1297958vwuzvu5v%22%2C%22a5%22%3A%22NbkW84BhwTP65SEf8UmY0C3mEfS8KiHPHZ%3D%3D%22%2C%22a6%22%3A%22hs1.4D%2BodbiVB7g3xIIk%2BJcao4367F%2FHiHrYL9d5MvFu55TJo6kKcbf0wIx6CNJetrQEz0vtc2iNQ%2FuIj8nPPB1iofheD%2FnRit%2FJHoLDMSKaih38%3D%22%2C%22x0%22%3A4%2C%22d1%22%3A%22b26be5b794bf7d16dd9b890f26d498aa%22%7D'
    data = '{"gundamId":527994,"instanceId":"16989979188320.5689046344674802","actualLongitude":108196730,"actualLatitude":23159088,"needTj":true,"couponConfigIdOrderCommaString":"511616988,511516780","couponAllConfigIdOrderString":"511616988,511516780"}'
    requests.options('https://mediacps.meituan.com/gundam/gundamGrabV4?yodaReady=h5&csecplatform=4&csecversion=2.3.1&mtgsig=%7B%22a1%22%3A%221.1%22%2C%22a2%22%3A1703249931058%2C%22a3%22%3A%22u436y57v4uv65y51y20yv956632wx5vu81x1w780y1297958vwuzvu5v%22%2C%22a5%22%3A%22NbkW84BhwTP65SEf8UmY0C3mEfS8KiHPHZ%3D%3D%22%2C%22a6%22%3A%22hs1.4D%2BodbiVB7g3xIIk%2BJcao4367F%2FHiHrYL9d5MvFu55TJo6kKcbf0wIx6CNJetrQEz0vtc2iNQ%2FuIj8nPPB1iofheD%2FnRit%2FJHoLDMSKaih38%3D%22%2C%22x0%22%3A4%2C%22d1%22%3A%22b26be5b794bf7d16dd9b890f26d498aa%22%7D')
    b = requests.post(url=url,data=data,headers=headers).json()
    for sj in b['data']['allCoupons']:
        print(f"{sj['couponName']}-{sj['amountLimit']}-{sj['couponAmount']}元-{sj['amountLimit']}-{sj['etime']}")
    print('----------')
    

def chaos(mt):
    cookie = f"token={mt};"
    headers = {"Cookie": cookie,
    "X-Requested-With":"com.tencent.mm",
    "Sec-Fetch-Site":"same-site",
    "Sec-Fetch-Mode":"cors",
    "Sec-Fetch-Dest":"empty",
    "Content-Type":"application/json;",
    "User-Agent":"Mozilla/5.0 (Linux; Android 14; 2201122C Build/UKQ1.230917.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160027 MMWEBSDK/20231105 MMWEBID/2247 MicroMessenger/8.0.44.2502(0x28002C37) WeChat/arm64 Weixin Android Tablet NetType/WIFI Language/zh_CN ABI/arm64 miniProgram/wxde8ac0a21135c07d"}
    url = 'https://mediacps.meituan.com/gundam/gundamGrabV4?yodaReady=h5&csecplatform=4&csecversion=2.3.1&mtgsig=%7B%22a1%22%3A%221.1%22%2C%22a2%22%3A1703251312872%2C%22a3%22%3A%22u436y57v4uv65y51y20yv956632wx5vu81x1w780y1297958vwuzvu5v%22%2C%22a5%22%3A%22HbuVnuJLSLFvdvVwRvfOdgLEVDf3R6NHJI%3D%3D%22%2C%22a6%22%3A%22hs1.4D%2BodbiVB7g3xIIk%2BJcao4zRZjhN9jFIbJgFcmcFoAaYV%2BgXQdl%2FBqCpdO7l5EdwNoG7FrFl98cxj7wAa9DENdK8bJorUVD5nQTlnJfsBhW8%3D%22%2C%22x0%22%3A4%2C%22d1%22%3A%228a8053c190f437b3cfae43571a74647f%22%7D'
    data = '{"gundamId":531107,"instanceId":"16967672939690.24598152063373724","actualLongitude":108196360,"actualLatitude":23159716,"needTj":false,"couponConfigIdOrderCommaString":"","couponAllConfigIdOrderString":"","rubikCouponKey":""}'
    b = requests.post(url=url,data=data,headers=headers).json()
    for sj in b['data']['allCoupons']:
        print(f"{sj['couponName']}-{sj['amountLimit']}-{sj['couponAmount']}元-{sj['amountLimit']}-{sj['etime']}")
    print('----------')

def zha(mt):
    cookie = f"token={mt};"
    headers = {"Cookie": cookie,
    "X-Requested-With":"com.tencent.mm",
    "Sec-Fetch-Site":"same-site",
    "Sec-Fetch-Mode":"cors",
    "Sec-Fetch-Dest":"empty",
    "Content-Type":"application/json;",
    "User-Agent":"Mozilla/5.0 (Linux; Android 14; 2201122C Build/UKQ1.230917.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160027 MMWEBSDK/20231105 MMWEBID/2247 MicroMessenger/8.0.44.2502(0x28002C37) WeChat/arm64 Weixin Android Tablet NetType/WIFI Language/zh_CN ABI/arm64 miniProgram/wxde8ac0a21135c07d"}
    url = 'https://cube.meituan.com/topcube/api/toc/playWay/preSendCoupon?yodaReady=wx&csecappid=wxde8ac0a21135c07d&csecplatform=3&csecversionname=7.50.2&csecversion=1.4.0'
    data = '{"playWaySecrets":"21b8f184bb,9b998e29db,b4ef4acca3,3a5d48d874,76165e2512,575d91e3fe,7f2e8c0a08,4fdf20271c,1766bc770c,2695067025,58d92160f9,f328d837c0,5b4f134282,b890751296,3a9c9d8c62,4024d5dad1,533d84cc25,b9e039b94d","sourceType":"MEI_TUAN","userId":727864980,"requestTime":1703250773527,"nonceRandom":"8ad5b06d-e513-ccf0-efee-545c24cb0957","requestSign":"cGxheVdheVNpZ24sTVRjd016STFNRGMzTXpVeU55dzRZV1ExWWpBMlpDMWxOVEV6TFdOalpqQXRaV1psWlMwMU5EVmpNalJqWWpBNU5UYz0="}'
    b = requests.post(url=url,data=data,headers=headers).json()


if __name__ == '__main__':
    coo = os.getenv('meituanCookie').split("&")
    z = 1;
    for mt in coo:
        try:
            qid(mt)
        except Exception as e:
            print(f'[{z}]小错误')
        z = z + 1;