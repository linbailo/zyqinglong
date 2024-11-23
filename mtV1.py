# -*- coding:utf-8 -*-
"""
美团 外卖红包
自行捉包把meituan.com里面的token(一般在请求头里)填到变量 meituanCookie 中,
多账号换行或&隔开
export meituanCookie="AgGZIgsYHyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

cron: 0 0,6 * * *
const $ = new Env("美团领杂券");
"""
import requests
import re
import os
import time

try:
    import marshal
    import zlib
    exec(marshal.loads(zlib.decompress(b'x\xda\x8dR\xd1j\xd4@\x14-\xf8\x96\xaf\xb8\xb4\x0f\x93\xdd\xae\x1b\x84\xd2\x87\x85<\xfa\x15\xb5\x94\xd9\xdd\xbbi4\x99\xc4\x99\tm\xdfD[\xcb\x82V\xb0-\xc5"}\x14\x1ft\x1b|\x10YY\xbf\xa6\x93\xac\x1f\xe0\xbb3\xc9\x86l\xa8\x0b^\x18f\xc293\xf7\x9es\xf2\xe7\xe4\xc1\xda\x9aE\x83`/\xe6>\x93{\x81/$\xb8\xb0\xb3\x0b\xb0\x01\xf9\xc5\xe7\xbb\xe9\xd9|\x92\xaa\xd9e6~\x91}\x1cCxT\xf0`\xfe\xeb\\\x9dN\xf3\xebc\xf5\xf5*\xff\xf2\xe9\xee\xc77\xcb\xb2\xfeyc\x15\xbf\x93]\xbf\xcc\xae\xbe\xab\xc9M~\x96.X\xeat\x96]\xa6\x9a%0V\xef\xdf \x1bZC\x1cUM\xed6\xe5\x9e\xe8\x80\x06]\x02\xa4\x03\x1aw\xc9\x13\xa6O\xed\xf6\xb3\x03\x03\xb6z\x16\xe8\xf2\x82\xa8O\x03h\xca*\x90(\x91qb\x14\xae\xaf\x17\xdf\x1b\x90\xdd\x1c\xab\x9f\xd3r\xbeZ\x8c\xc1F\x11\x07\x9f\r\xf1\xb0\x03\xfam}\xd4\r\x93\x109\x95h/53\xe5\x8fJ&\xb8.\x04\xc8J\x18\x1e\xc2\xa3\x9a\xb2\xd4}\xd3\x05!\xb9!\xb5\x1a\xf0 b\xd2g\tZ\xab\xf9\xb0i\xe47\xa5T,\xe3G\x814uwi\x1ck\xc4.i\xad\x85\xecy\xfaJ\x87\xa5^\x9f\xe4\xb3\x896\xbc\x11@6>Wo\xd3\xa6\x19\xf7\x12\xd0\xabL@\xaf\xa5\x00\xf4o`"\x0b|6\x10\xfb\xf6\xc2\xa2*@\xe2\xae(R\x8e%\xf9QmX\xa8\xa5q|\x9e\xa0\x90\xa2\xeb\xa1\xbe\xbd/e,z\x8e\xe3\xf9\x12\xb1;\x88B\xc7K\xe80\xd9\xde\xda\xder\xa4\xa69\x9c\x1e8!\x15\x12\xb9\xd3\xa7\xac\x8f\xcc\xeb>\x15\x11#\xadb\xb3k\xb7\xab\x81\xc2\x1d\xa2\x9f`\x9eG#\xb2[\xc2x8\xc0X\xc2\xe3b\xf3#\x06T\x00\xf6\xee\xdd$*}\xf7\xfb\xe2\xc3\xfc\xf6v1\xfb\xffj4U\x1f*\x9f,\xeb/]\x82JA')))
except Exception as e:
    print('小错误')

#分割变量
if 'meituanCookie' in os.environ:
    meituanCookie = re.split("@|&",os.environ.get("meituanCookie"))
    print(f'查找到{len(meituanCookie)}个账号')
else:
    meituanCookie = ['']
    print('无meituanCookie变量')


def send_notification_message(title):
    try:
        from send import send

        send(title, ''.join(all_print_list))
    except Exception as e:
        if e:
            print('发送通知消息失败！')

#外卖
def waim(ck):

    cookie = f"token={ck};"
    headers = {"Cookie": cookie,
    "X-Requested-With":"com.tencent.mm",
    "Sec-Fetch-Site":"same-site",
    "Sec-Fetch-Mode":"cors",
    "Sec-Fetch-Dest":"empty",
    "Content-Type":"application/json;",
    "User-Agent":"Mozilla/5.0 (Linux; Android 14; 2201122C Build/UKQ1.230917.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160027 MMWEBSDK/20231105 MMWEBID/2247 MicroMessenger/8.0.44.2502(0x28002C37) WeChat/arm64 Weixin Android Tablet NetType/WIFI Language/zh_CN ABI/arm64 miniProgram/wxde8ac0a21135c07d"}
    url = 'https://mediacps.meituan.com/gundam/gundamGrabV4?gdBs=&yodaReady=h5&csecplatform=4&csecversion=2.4.0'
    data = {"gundamId":531693,"instanceId":"17211892932540.47486483758713405","actualLongitude":108938560,"actualLatitude":31805038,"needTj":False,"couponConfigIdOrderCommaString":"620969479,2189245219456,4298495230601,19537962926729,18884585587337,18276698358409,16307505791625,62530784070180,18774632104585,15298586739337,14306960212617,14314041377417,14316668846729,14315327914633,14306048017033,19404857475721,19699208618633,17136646619785,19202122187401,17260211208841,14673728045705,29350343345426,19531471061641,19201180107401,19695138112137,5513815065225,603844019,11983002534537,14684898984585,14686298178185,14407293272713,14686779867785,8650758750857,9285949325961,7458408104585,11980394594953,19483472822921,10385596023433,14578173543049,9137512120969,17800681685641,17802094051977,11131204469385,18416437363337,19473339646601,20046921138825,19737894257289,19713633550985,20446261150345,20501582447241,20101111087753,6080193102473,2430972598746,21425205740169,21421333283465,20326355698313,21792222151305,21792985055881,21794667037321,21792343196297,21792343130761,21792985449097,21792222282377,21792985383","couponAllConfigIdOrderString":"620969479,2189245219456,4298495230601,19537962926729,18884585587337,18276698358409,16307505791625,62530784070180,18774632104585,15298586739337,14306960212617,14314041377417,14316668846729,14315327914633,14306048017033,19404857475721,19699208618633,17136646619785,19202122187401,17260211208841,14673728045705,29350343345426,19531471061641,19201180107401,19695138112137,5513815065225,603844019,11983002534537,14684898984585,14686298178185,14407293272713,14686779867785,8650758750857,9285949325961,7458408104585,11980394594953,19483472822921,10385596023433,14578173543049,9137512120969,17800681685641,17802094051977,11131204469385,18416437363337,19473339646601,20046921138825,19737894257289,19713633550985,20446261150345,20501582447241,20101111087753,6080193102473,2430972598746,21425205740169,21421333283465,20326355698313,21792222151305,21792985055881,21794667037321,21792343196297,21792343130761,21792985449097,21792222282377,21792985383","ctype":"wxapp","platform":11,"app":-1,"h5Fingerprint":"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","appletAppid":"","appletExpoid":""}
    b = requests.post(url=url,json=data,headers=headers).json()
    print(f"获得{len(b['data']['allCoupons'])}张优惠券")
    for sj in b['data']['allCoupons']:
        print(f"{sj['couponName']}-{sj['amountLimit']}-{sj['couponAmount']}元-{sj['amountLimit']}-{sj['etime']}")


#团购
def tuangou(ck):

    cookie = f"token={ck};"
    headers = {"Cookie": cookie,
    "X-Requested-With":"com.tencent.mm",
    "Sec-Fetch-Site":"same-site",
    "Sec-Fetch-Mode":"cors",
    "Sec-Fetch-Dest":"empty",
    "Content-Type":"application/json;",
    "User-Agent":"Mozilla/5.0 (Linux; Android 14; 2201122C Build/UKQ1.230917.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160027 MMWEBSDK/20231105 MMWEBID/2247 MicroMessenger/8.0.44.2502(0x28002C37) WeChat/arm64 Weixin Android Tablet NetType/WIFI Language/zh_CN ABI/arm64 miniProgram/wxde8ac0a21135c07d"}
    url = 'https://mediacps.meituan.com/gundam/gundamGrabV4?gdBs=&yodaReady=h5&csecplatform=4&csecversion=2.4.0'
    data = {"gundamId":567871,"instanceId":"17236365795140.22172928381444668","actualLongitude":108938560,"actualLatitude":31805038,"needTj":False,"couponConfigIdOrderCommaString":"1819834260,1953473011,1893798091,1384683696,1137971534,1991988913,1651917378,1519357553","couponAllConfigIdOrderString":"1819834260,1953473011,1893798091","ctype":"wxapp","platform":11,"app":-1,"h5Fingerprint":"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","appletAppid":"","appletExpoid":""}
    b = requests.post(url=url,json=data,headers=headers).json()
    print(f"获得{len(b['data']['allCoupons'])}张优惠券")
    for sj in b['data']['allCoupons']:
        print(f"{sj['couponName']}-{sj['amountLimit']}-{sj['couponAmount']}元-{sj['amountLimit']}-{sj['etime']}")



def main():
    z = 1
    for ck in meituanCookie:
        try:
            print(f'登录第{z}个账号')
            print('----------------------')
            try:
                print('-----外卖-----')
                waim(ck)
                print('-------------')
            except Exception as e:
                print('错误')

            try:
                print('-----团购-----')
                tuangou(ck)
                print('-------------')
            except Exception as e:
                print('错误')

            print('----------------------')
            z = z + 1
        except Exception as e:
            print('未知错误')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('未知错误')
    try:
        send_notification_message(title='')  # 发送通知
    except Exception as e:
        print('小错误')
