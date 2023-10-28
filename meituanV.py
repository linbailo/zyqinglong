# -*- coding:utf-8 -*-
"""
美团 外卖红包
自行捉包把meituan.com里面的token(一般在请求头里)填到变量 meituanCookie 中,
多账号换行或&隔开
export meituanCookie="AgGZIgsYHyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

cron: 1,30 0,6,7,10,11,16,17,20,21 * * *
const $ = new Env("美团辅助");
"""
import os
import requests
import json
import urllib
import re
from urllib import parse



def main(mt):
    print('----------------------------------')
    cookie = f"token={mt};"
    headers = {"Cookie": cookie,"Content-Type":"application/json;","User-Agent":"Mozilla/5.0 (Linux; Android 6.0.1; OPPO R9s Plus Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36"}
    url = 'https://mediacps.meituan.com/gundam/gundamGrabV4?yodaReady=h5&csecplatform=4&csecversion=2.2.1&mtgsig=%7B%22a1%22%3A%221.1%22%2C%22a2%22%3A1698504867588%2C%22a3%22%3A%2299uz8397yvx55z1y16w334959v3vxvy581y3u9wvuy0979588vwx57x1%22%2C%22a5%22%3A%22GR3G2ZYfmue9ktMPozbDtHL0FX%2BNFwPxcc%3D%3D%22%2C%22a6%22%3A%22hs1.4rMLnSSN7%2FTuDgTJbLhpKNOP7G6dUz8T2CCHjsw3G4CnL0pySkmGTvdDmfIDwE6hIQj6HRVowIK%2BA7iC41fxqE%2B0QCDchF9WoZk%2B%2BYSYs3qw%3D%22%2C%22x0%22%3A4%2C%22d1%22%3A%22a360debf153a38948d8e4273b65ae638%22%7D'
    data = '{"gundamId":531693,"instanceId":"16970942475030.47518664115092070","actualLongitude":108198240,"actualLatitude":23158490,"needTj":true,"couponConfigIdOrderCommaString":"620969479,2189245219456,2237835510400,4298495230601,10976581976713,11025609523849,10977675051657,11024291201673,10977017135753,8199578190473,8200987935369,8201667543689,8200025342601,8200025473673,7390907925129,7622642631305,7606006907529,604064706,604064705,4987378139785,345822793","couponAllConfigIdOrderString":"620969479,2189245219456,2237835510400,4298495230601,10976581976713,11025609523849,10977675051657,11024291201673,10977017135753,8199578190473,8200987935369,8201667543689,8200025342601,8200025473673,7390907925129,7622642631305,7606006907529,604064706,604064705,4987378139785,345822793","platform":13,"app":-1,"h5Fingerprint":"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"}'
    b = requests.post(url=url,data=data,headers=headers).json()
    print(f'[{z}]账号登录成功')
    for sj in b['data']['allCoupons']:
        print(f"{sj['couponName']}-{sj['amountLimit']}-{sj['couponAmount']}元-{sj['amountLimit']}-{sj['etime']}")
    print('----------')


def main1(mt):
    cookie = f"token={mt};"
    headers = {"Cookie": cookie,"Content-Type":"application/json;","User-Agent":"Mozilla/5.0 (Linux; Android 6.0.1; OPPO R9s Plus Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36"}
    url = 'https://mediacps.meituan.com/gundam/gundamGrabV4?yodaReady=h5&csecplatform=4&csecversion=2.2.1&mtgsig=%7B%22a1%22%3A%221.1%22%2C%22a2%22%3A1698506149400%2C%22a3%22%3A%2299uz8397yvx55z1y16w334959v3vxvy581y3u9wvuy0979588vwx57x1%22%2C%22a5%22%3A%22cqd2eLaWKIy2%2F9vP%2FEDs6%2BPwMTEdfmXB%22%2C%22a6%22%3A%22hs1.4rMLnSSN7%2FTuDgTJbLhpKNOP7G6dUz8T2CCHjsw3G4Ck9NdcmgZIhm%2BwQjywSt4a%2BfJhIIJIbI0hFbVFODuTD5LuXnVzatJC5ZggGDlTQVDs%3D%22%2C%22x0%22%3A4%2C%22d1%22%3A%22a23dc428ce77c69d151b881f6c4a02bd%22%7D'
    data = '{"gundamId":527994,"instanceId":"16977916717790.8310434034926044","actualLongitude":108197150,"actualLatitude":23158876,"needTj":true,"couponConfigIdOrderCommaString":"511616988,511516780","couponAllConfigIdOrderString":"511616988,511516780"}'
    b = requests.post(url=url,data=data,headers=headers).json()
    for sj in b['data']['allCoupons']:
        print(f"{sj['couponName']}-{sj['amountLimit']}-{sj['couponAmount']}元-{sj['amountLimit']}-{sj['etime']}")
    print('----------')
    print('----------------------------------')



if __name__ == '__main__':
    coo = os.getenv('meituanCookie').split("&")
    z = 1;
    for mt in coo:
        try:
            main(mt)
            main1(mt)
        except Exception as e:
            print(f'[{z}]账号登录失败')
        z = z + 1;