#2025/1/6 遍历生活特权所有分组的券进行领券，券没啥用但完成可领取30点丰蜜目前一天拉满155点
#变量名：sfsyUrl
#格式：多账号用&分割或创建多个变量sfsyUrl
#关于参数获取如下两种方式：
#❶顺丰APP绑定微信后，前往该站点sm.linzixuan.work用微信扫码登录后，选择复制编码Token，不要复制错
#或者
#❷打开小程序或APP-我的-积分, 手动抓包以下几种URL之一
#https://mcs-mimp-web.sf-express.com/mcs-mimp/share/weChat/shareGiftReceiveRedirect
#https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/shareRedirect
#抓好URL后访问https://www.toolhelper.cn/EncodeDecode/Url进行编码，请务必按提示操作
import hashlib
import json
import os
import random
import time
from datetime import datetime, timedelta
from sys import exit
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from urllib.parse import unquote

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 代理相关配置
PROXY_API_URL = os.getenv('SF_PROXY_API_URL', '')  # 从环境变量获取代理API地址

def get_proxy():
    """
    从代理API获取代理
    返回格式：{'http': 'http://ip:port', 'https': 'http://ip:port'}
    """
    try:
        if not PROXY_API_URL:
            print('⚠️ 未配置代理API地址，将不使用代理')
            return None
            
        response = requests.get(PROXY_API_URL, timeout=10)
        if response.status_code == 200:
            proxy_text = response.text.strip()
            if ':' in proxy_text:
                proxy = f'http://{proxy_text}'
                return {
                    'http': proxy,
                    'https': proxy
                }
        print(f'❌ 获取代理失败: {response.text}')
        return None
    except Exception as e:
        print(f'❌ 获取代理异常: {str(e)}')
        return None

send_msg = ''
one_msg = ''

def Log(cont=''):
    global send_msg, one_msg
    print(cont)
    if cont:
        one_msg += f'{cont}\n'
        send_msg += f'{cont}\n'

inviteId = ['']

class RUN:
    def __init__(self, info, index):
        global one_msg
        one_msg = ''
        split_info = info.split('@')
        url = split_info[0]
        len_split_info = len(split_info)
        last_info = split_info[len_split_info - 1]
        self.send_UID = None
        if len_split_info > 0 and "UID_" in last_info:
            self.send_UID = last_info
        self.index = index + 1

        # 获取代理
        self.proxy = get_proxy()
        if self.proxy:
            print(f"✅ 成功获取代理: {self.proxy['http']}")
        
        self.s = requests.session()
        self.s.verify = False
        if self.proxy:
            self.s.proxies = self.proxy
            
        self.headers = {
            'Host': 'mcs-mimp-web.sf-express.com',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090551) XWEB/6945 Flue',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'zh-CN,zh',
            'platform': 'MINI_PROGRAM',
        }
        
        # 32周年活动相关属性初始化
        self.ifPassAllLevel = False
        self.surplusPushTime = 0
        self.lotteryNum = 0
        
        self.anniversary_black = False
        self.member_day_black = False
        self.member_day_red_packet_drew_today = False
        self.member_day_red_packet_map = {}
        self.login_res = self.login(url)
        self.all_logs = []  # 初始化all_logs属性
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.max_level = 8
        self.packet_threshold = 1 << (self.max_level - 1)

    def get_deviceId(self, characters='abcdef0123456789'):
        result = ''
        for char in 'xxxxxxxx-xxxx-xxxx':
            if char == 'x':
                result += random.choice(characters)
            elif char == 'X':
                result += random.choice(characters).upper()
            else:
                result += char
        return result

    def login(self, sfurl):
        try:
            decoded_url = unquote(sfurl)
            ress = self.s.get(decoded_url, headers=self.headers)
            self.user_id = self.s.cookies.get_dict().get('_login_user_id_', '')
            self.phone = self.s.cookies.get_dict().get('_login_mobile_', '')
            self.mobile = self.phone[:3] + "*" * 4 + self.phone[7:] if self.phone else ''
            
            if self.phone:
                Log(f'👤 账号{self.index}:【{self.mobile}】登陆成功')
                return True
            else:
                Log(f'❌ 账号{self.index}获取用户信息失败')
                return False
        except Exception as e:
            Log(f'❌ 登录异常: {str(e)}')
            return False

    def getSign(self):
        timestamp = str(int(round(time.time() * 1000)))
        token = 'wwesldfs29aniversaryvdld29'
        sysCode = 'MCS-MIMP-CORE'
        data = f'token={token}&timestamp={timestamp}&sysCode={sysCode}'
        signature = hashlib.md5(data.encode()).hexdigest()
        data = {
            'sysCode': sysCode,
            'timestamp': timestamp,
            'signature': signature
        }
        self.headers.update(data)
        return data

    def do_request(self, url, data={}, req_type='post', max_retries=3):
        self.getSign()
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                if req_type.lower() == 'get':
                    response = self.s.get(url, headers=self.headers, timeout=30)  # 添加超时
                elif req_type.lower() == 'post':
                    response = self.s.post(url, headers=self.headers, json=data, timeout=30)  # 添加超时
                else:
                    raise ValueError('Invalid req_type: %s' % req_type)
                    
                # 检查响应状态码
                response.raise_for_status()
                
                try:
                    res = response.json()
                    return res
                except json.JSONDecodeError as e:
                    print(f'JSON解析失败: {str(e)}, 响应内容: {response.text[:200]}')  # 只打印前200个字符
                    retry_count += 1
                    if retry_count < max_retries:
                        print(f'正在进行第{retry_count + 1}次重试...')
                        time.sleep(2)  # 添加延迟
                        continue
                    return None
                    
            except requests.exceptions.RequestException as e:
                retry_count += 1
                if retry_count < max_retries:
                    print(f'请求失败，正在切换代理重试 ({retry_count}/{max_retries}): {str(e)}')
                    # 重新获取代理
                    self.proxy = get_proxy()
                    if self.proxy:
                        print(f"✅ 成功获取新代理: {self.proxy['http']}")
                        self.s.proxies = self.proxy
                    time.sleep(2)  # 等待2秒后重试
                else:
                    print('请求最终失败:', e)
                    return None
                
        return None  # 所有重试都失败后返回None

    def sign(self):
        print(f'🎯 开始执行签到')
        json_data = {"comeFrom": "vioin", "channelFrom": "WEIXIN"}
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTaskSignPlusService~automaticSignFetchPackage'
        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            count_day = response.get('obj', {}).get('countDay', 0)
            if response.get('obj') and response['obj'].get('integralTaskSignPackageVOList'):
                packet_name = response["obj"]["integralTaskSignPackageVOList"][0]["packetName"]
                Log(f'✨ 签到成功，获得【{packet_name}】，本周累计签到【{count_day + 1}】天')
            else:
                Log(f'📝 今日已签到，本周累计签到【{count_day + 1}】天')
        else:
            print(f'❌ 签到失败！原因：{response.get("errorMessage")}')

    def superWelfare_receiveRedPacket(self):
        print(f'🎁 超值福利签到')
        json_data = {
            'channel': 'czflqdlhbxcx'
        }
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberActLengthy~redPacketActivityService~superWelfare~receiveRedPacket'
        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            gift_list = response.get('obj', {}).get('giftList', [])
            if response.get('obj', {}).get('extraGiftList', []):
                gift_list.extend(response['obj']['extraGiftList'])
            gift_names = ', '.join([gift['giftName'] for gift in gift_list])
            receive_status = response.get('obj', {}).get('receiveStatus')
            status_message = '领取成功' if receive_status == 1 else '已领取过'
            Log(f'🎉 超值福利签到[{status_message}]: {gift_names}')
        else:
            error_message = response.get('errorMessage') or json.dumps(response) or '无返回'
            print(f'❌ 超值福利签到失败: {error_message}')

    def get_SignTaskList(self, END=False):
        if not END: print(f'🎯 开始获取签到任务列表')
        json_data = {
            'channelType': '1',
            'deviceId': self.get_deviceId(),
        }
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTaskStrategyService~queryPointTaskAndSignFromES'
        response = self.do_request(url, data=json_data)
        if response.get('success') == True and response.get('obj') != []:
            totalPoint = response["obj"]["totalPoint"]
            if END:
                Log(f'💰 当前积分：【{totalPoint}】')
                return
            Log(f'💰 执行前积分：【{totalPoint}】')
            for task in response["obj"]["taskTitleLevels"]:
                self.taskId = task["taskId"]
                self.taskCode = task["taskCode"]
                self.strategyId = task["strategyId"]
                self.title = task["title"]
                status = task["status"]
                skip_title = ['用行业模板寄件下单', '去新增一个收件偏好', '参与积分活动']
                if status == 3:
                    print(f'✨ {self.title}-已完成')
                    continue
                if self.title in skip_title:
                    print(f'⏭️ {self.title}-跳过')
                    continue
                else:
                    # print("taskId:", taskId)
                    # print("taskCode:", taskCode)
                    # print("----------------------")
                    self.doTask()
                    time.sleep(3)
                self.receiveTask()

    def doTask(self):
        print(f'🎯 开始去完成【{self.title}】任务')
        json_data = {
            'taskCode': self.taskCode,
        }
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonRoutePost/memberEs/taskRecord/finishTask'
        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            print(f'✨ 【{self.title}】任务-已完成')
        else:
            print(f'❌ 【{self.title}】任务-{response.get("errorMessage")}')

    def receiveTask(self):
        print(f'🎁 开始领取【{self.title}】任务奖励')
        json_data = {
            "strategyId": self.strategyId,
            "taskId": self.taskId,
            "taskCode": self.taskCode,
            "deviceId": self.get_deviceId()
        }
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTaskStrategyService~fetchIntegral'
        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            print(f'✨ 【{self.title}】任务奖励领取成功！')
        else:
            print(f'❌ 【{self.title}】任务-{response.get("errorMessage")}')

    def do_honeyTask(self):
        # 做任务
        json_data = {"taskCode": self.taskCode}
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberEs~taskRecord~finishTask'
        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            print(f'>【{self.taskType}】任务-已完成')
        else:
            print(f'>【{self.taskType}】任务-{response.get("errorMessage")}')

    def receive_honeyTask(self):
        print('>>>执行收取丰蜜任务')
        # 收取
        self.headers['syscode'] = 'MCS-MIMP-CORE'
        self.headers['channel'] = 'wxwdsj'
        self.headers['accept'] = 'application/json, text/plain, */*'
        self.headers['content-type'] = 'application/json;charset=UTF-8'
        self.headers['platform'] = 'MINI_PROGRAM'
        json_data = {"taskType": self.taskType}
        # print(json_data)
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~receiveExchangeIndexService~receiveHoney'
        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            print(f'收取任务【{self.taskType}】成功！')
        else:
            print(f'收取任务【{self.taskType}】失败！原因：{response.get("errorMessage")}')


    def get_coupom(self, goods):  
        # 请求参数
        json_data = {
            "from": "Point_Mall",
            "orderSource": "POINT_MALL_EXCHANGE",
            "goodsNo": goods['goodsNo'],
            "quantity": 1,
            "taskCode": self.taskCode
        }
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberGoods~pointMallService~createOrder'
    
        # 发起领券请求
        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
           # print(f'> 领券成功！')
            return True  # 领取成功
        else:
           # print(f'> 领券失败！原因：{response.get("errorMessage")}')
            return False  # 领取失败
    
    
    def get_coupom_list(self):        
        # 请求参数
        json_data = {
            "memGrade": 2,
            "categoryCode": "SHTQ",
            "showCode": "SHTQWNTJ"
        }
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberGoods~mallGoodsLifeService~list'
    
        # 发起获取券列表请求
        response = self.do_request(url, data=json_data)
    
        if response.get('success') == True:
            # 遍历所有分组的券列表
            all_goods = []
            for obj in response.get("obj", []):  # 遍历所有券分组
                goods_list = obj.get("goodsList", [])
                all_goods.extend(goods_list)  # 收集到一个总列表中
               
            # 尝试领取
            for goods in all_goods:
                exchange_times_limit = goods.get('exchangeTimesLimit', 0)
    
                # 检查券是否可兑换
                if exchange_times_limit >= 1:
                    #print(f'尝试领取：{goods["goodsName"]}')
                    
                    # 尝试领取券
                    if self.get_coupom(goods):
                        print('✨ 成功领取券，任务结束！')
                        return  # 成功领取后退出
            print('📝 所有券尝试完成，没有可用的券或全部领取失败。')
        else:
            print(f'> 获取券列表失败！原因：{response.get("errorMessage")}')



    def get_honeyTaskListStart(self):
        print('🍯 开始获取采蜜换大礼任务列表')
        # 任务列表
        json_data = {}
        self.headers['channel'] = 'wxwdsj'
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~receiveExchangeIndexService~taskDetail'

        response = self.do_request(url, data=json_data)
        # print(response)
        if response.get('success') == True:
            for item in response["obj"]["list"]:
                self.taskType = item["taskType"]
                status = item["status"]
                if status == 3:
                    print(f'✨ 【{self.taskType}】-已完成')
                    continue
                if "taskCode" in item:
                    self.taskCode = item["taskCode"]
                    if self.taskType == 'DAILY_VIP_TASK_TYPE':
                        self.get_coupom_list()
                    else:
                        self.do_honeyTask()
                if self.taskType == 'BEES_GAME_TASK_TYPE':
                    self.honey_damaoxian()
                time.sleep(2)

    def honey_damaoxian(self):
        print('>>>执行大冒险任务')
        # 大冒险
        gameNum = 5
        for i in range(1, gameNum):
            json_data = {
                'gatherHoney': 20,
            }
            if gameNum < 0: break
            print(f'>>开始第{i}次大冒险')
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~receiveExchangeGameService~gameReport'
            response = self.do_request(url, data=json_data)
            # print(response)
            stu = response.get('success')
            if stu:
                gameNum = response.get('obj')['gameNum']
                print(f'>大冒险成功！剩余次数【{gameNum}】')
                time.sleep(2)
                gameNum -= 1
            elif response.get("errorMessage") == '容量不足':
                print(f'> 需要扩容')
                self.honey_expand()
            else:
                print(f'>大冒险失败！【{response.get("errorMessage")}】')
                break

    def honey_expand(self):
        print('>>>容器扩容')
        # 大冒险
        gameNum = 5

        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~receiveExchangeIndexService~expand'
        response = self.do_request(url, data={})
        # print(response)
        stu = response.get('success', False)
        if stu:
            obj = response.get('obj')
            print(f'>成功扩容【{obj}】容量')
        else:
            print(f'>扩容失败！【{response.get("errorMessage")}】')

    def honey_indexData(self, END=False):
        if not END: print('--------------------------------\n🍯 开始执行采蜜换大礼任务')
        # 邀请
        random_invite = random.choice([invite for invite in inviteId if invite != self.user_id])
        self.headers['channel'] = 'wxwdsj'
        json_data = {"inviteUserId": random_invite}
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~receiveExchangeIndexService~indexData'
        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            usableHoney = response.get('obj').get('usableHoney')
            activityEndTime = response.get('obj').get('activityEndTime', '')
            activity_end_time = datetime.strptime(activityEndTime, "%Y-%m-%d %H:%M:%S")
            current_time = datetime.now()

            if not END:
                print(f'📅 本期活动结束时间【{activityEndTime}】')
                Log(f'🍯 执行前丰蜜：【{usableHoney}】')
                taskDetail = response.get('obj').get('taskDetail')

                if taskDetail != []:
                    for task in taskDetail:
                        self.taskType = task['type']
                        self.receive_honeyTask()
                        time.sleep(2)
            else:
                Log(f'🍯 执行后丰蜜：【{usableHoney}】')
                return

    def EAR_END_2023_TaskList(self):
        print('\n🎭 开始年终集卡任务')
        # 任务列表
        json_data = {
            "activityCode": "YEAREND_2024",
            "channelType": "MINI_PROGRAM"
        }
        self.headers['channel'] = '24nzdb'
        self.headers['platform'] = 'MINI_PROGRAM'
        self.headers['syscode'] = 'MCS-MIMP-CORE'

        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~activityTaskService~taskList'

        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            for item in response["obj"]:
                self.title = item["taskName"]
                self.taskType = item["taskType"]
                status = item["status"]
                if status == 3:
                    print(f'✨ 【{self.taskType}】-已完成')
                    continue
                if self.taskType == 'INTEGRAL_EXCHANGE':
                    self.EAR_END_2023_ExchangeCard()
                elif self.taskType == 'CLICK_MY_SETTING':
                    self.taskCode = item["taskCode"]
                    self.addDeliverPrefer()
                if "taskCode" in item:
                    self.taskCode = item["taskCode"]
                    self.doTask()
                    time.sleep(3)
                    self.EAR_END_2023_receiveTask()
                else:
                    print(f'⚠️ 暂时不支持【{self.title}】任务')

    def activityTaskService_taskList(self):
        print('🎭 开始32周年活动任务')
        json_data = {
            "activityCode": "DRAGONBOAT_2025",
            "channelType": "MINI_PROGRAM"
        }
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~activityTaskService~taskList'
        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            # 需要过滤的任务类型
            skip_task_types = [
                'PLAY_ACTIVITY_GAME',      # 玩一笔连粽游戏
                'SEND_SUCCESS_RECALL',      # 去寄快递
                'OPEN_SUPER_CARD',         # 开通至尊会员
                'CHARGE_NEW_EXPRESS_CARD',  # 充值新速运通全国卡
                'OPEN_NEW_EXPRESS_CARD',    # 开通新速运通
                'OPEN_FAMILY_CARD',        # 开通亲情卡
                'INTEGRAL_EXCHANGE'         # 积分兑换
            ]
            
            task_list = response.get('obj', [])
            # 过滤掉已完成的和不支持的任务类型
            task_list = [x for x in task_list if x.get('status') == 2 and x.get('taskType') not in skip_task_types]
            
            if not task_list:
                print('没有可执行的任务')
                return
                
            print(f'📝 获取到未完成任务: {len(task_list)}个')
            for task in task_list:
                print(f'📝 开始任务: {task.get("taskName")} [{task.get("taskType")}]')
                await_time = random.randint(1500, 3000) / 1000.0
                time.sleep(await_time)
                self.activityTaskService_finishTask(task)
                time.sleep(1.5)
        else:
            error_msg = response.get("errorMessage", "未知错误")
            print(f'获取活动任务失败: {error_msg}')
            if isinstance(response.get("obj"), dict):
                print(f'错误详情: {json.dumps(response.get("obj"), ensure_ascii=False)}')

    def activityTaskService_finishTask(self, task):
        json_data = {
            "taskCode": task.get('taskCode')
        }
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberEs~taskRecord~finishTask'
        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            result_obj = response.get("obj", "")
            print(f'📝 完成任务[{task.get("taskName")}]: {result_obj}')
        else:
            error_code = response.get("errorCode", "未知错误码")
            error_msg = response.get("errorMessage", "未知错误")
            print(f'❌ 完成任务[{task.get("taskName")}]失败: {error_code} - {error_msg}')
            if isinstance(response.get("obj"), dict):
                print(f'错误详情: {json.dumps(response.get("obj"), ensure_ascii=False)}')

    def dragonBoatGame2025ServiceWin(self, levelIndex):
        json_data = {"levelIndex": levelIndex}
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~dragonBoatGame2025Service~win'
        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            print(f'🎮 第{levelIndex}关通关成功')
        else:
            error_msg = response.get("errorMessage", "未知错误")
            print(f'❌ 第{levelIndex}关通关失败: {error_msg}')
            if isinstance(response.get("obj"), dict):
                print(f'错误详情: {json.dumps(response.get("obj"), ensure_ascii=False)}')

    def dragonBoat2025HastenService(self):
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~dragonBoat2025HastenService~getHastenStatus'
        response = self.do_request(url, data={})
        if response.get('success') == True:
            self.lotteryNum = response.get('obj', {}).get('remainHastenChance')
            print(f'🎲 剩余加速次数: {self.lotteryNum}')
        else:
            print(f'查询加速次数失败: {response.get("errorMessage")}')

    def hastenLottery(self):
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~dragonBoat2025HastenService~hastenLottery'
        response = self.do_request(url, data={})
        if response.get('success') == True:
            remain = response.get('obj', {}).get('remainHastenChance', 0)
            print(f'🎲 加速成功，剩余加速次数: {remain}')
        else:
            error_msg = response.get("errorMessage", "未知错误")
            print(f'❌ 加速失败: {error_msg}')
            if isinstance(response.get("obj"), dict):
                print(f'错误详情: {json.dumps(response.get("obj"), ensure_ascii=False)}')

    def prizeDraw(self, opt):
        json_data = {"currency": opt.get('currency')}
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~dragonBoat2025LotteryService~prizeDraw'
        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            gift_name = response.get('obj', {}).get('giftBagName', '未知奖励')
            print(f'🎁 抽奖获得: {gift_name}')
        else:
            error_msg = response.get("errorMessage", "未知错误")
            print(f'❌ 抽奖失败: {error_msg}')
            if isinstance(response.get("obj"), dict):
                print(f'错误详情: {json.dumps(response.get("obj"), ensure_ascii=False)}')

    def getUpgradeStatus(self):
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~dragonBoat2025UpgradeService~getUpgradeStatus'
        response = self.do_request(url, data={})
        if response.get('success') == True:
            current_ratio = response.get('obj', {}).get('currentRatio', 0)
            level_list = [x for x in response.get('obj', {}).get('levelList', []) if x.get('balance', 0) > 0]
            
            if level_list:
                print(f'🎯 当前进度: {current_ratio}%，已达到兑换条件')
                for item in level_list:
                    self.prizeDraw(item)
                    time.sleep(1.5)
            else:
                print(f'⏳ 当前进度: {current_ratio}%')
        else:
            error_msg = response.get("errorMessage", "未知错误")
            print(f'❌ 查询加速状态失败: {error_msg}')
            if isinstance(response.get("obj"), dict):
                print(f'错误详情: {json.dumps(response.get("obj"), ensure_ascii=False)}')

    def activityTaskService_integralExchange(self):
        json_data = {
            "exchangeNum": 1,
            "activityCode": "DRAGONBOAT_2025"
        }
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~dragonBoat2025TaskService~integralExchange'
        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            print('✅ 积分兑换成功')
        else:
            error_msg = response.get("errorMessage", "未知错误")
            print(f'❌ 积分兑换失败: {error_msg}')
            if isinstance(response.get("obj"), dict):
                print(f'错误详情: {json.dumps(response.get("obj"), ensure_ascii=False)}')

    def dragonBoatGame2025Service(self):
        try:
            json_data = {"channelType": "MINI_PROGRAM"}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~dragonBoatGame2025Service~indexInfo'
            response = self.do_request(url, data=json_data)
            if response.get('success') == True:
                self.surplusPushTime = response.get('obj', {}).get('surplusPushTime', 0)
                self.ifPassAllLevel = response.get('obj', {}).get('ifPassAllLevel', False)
                print(f'🎮 剩余游戏次数: {self.surplusPushTime}')
                return True
            else:
                print(f'访问失败: {response.get("errorMessage")}')
                return False
        except Exception as e:
            print(f'访问异常: {str(e)}')
            return False

    def addDeliverPrefer(self):
        print(f'>>>开始【{self.title}】任务')
        json_data = {
            "country": "中国",
            "countryCode": "A000086000",
            "province": "北京市",
            "provinceCode": "A110000000",
            "city": "北京市",
            "cityCode": "A111000000",
            "county": "东城区",
            "countyCode": "A110101000",
            "address": "1号楼1单元101",
            "latitude": "",
            "longitude": "",
            "memberId": "",
            "locationCode": "010",
            "zoneCode": "CN",
            "postCode": "",
            "takeWay": "7",
            "callBeforeDelivery": 'false',
            "deliverTag": "2,3,4,1",
            "deliverTagContent": "",
            "startDeliverTime": "",
            "selectCollection": 'false',
            "serviceName": "",
            "serviceCode": "",
            "serviceType": "",
            "serviceAddress": "",
            "serviceDistance": "",
            "serviceTime": "",
            "serviceTelephone": "",
            "channelCode": "RW11111",
            "taskId": self.taskId,
            "extJson": "{\"noDeliverDetail\":[]}"
        }
        url = 'https://ucmp.sf-express.com/cx-wechat-member/member/deliveryPreference/addDeliverPrefer'
        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            print('新增一个收件偏好，成功')
        else:
            print(f'>【{self.title}】任务-{response.get("errorMessage")}')

    def member_day_index(self):
        print('🎭 会员日活动')
        try:
            invite_user_id = random.choice([invite for invite in inviteId if invite != self.user_id])
            payload = {'inviteUserId': invite_user_id}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~memberDayIndexService~index'

            response = self.do_request(url, data=payload)
            if response.get('success'):
                lottery_num = response.get('obj', {}).get('lotteryNum', 0)
                can_receive_invite_award = response.get('obj', {}).get('canReceiveInviteAward', False)
                if can_receive_invite_award:
                    self.member_day_receive_invite_award(invite_user_id)
                self.member_day_red_packet_status()
                Log(f'🎁 会员日可以抽奖{lottery_num}次')
                for _ in range(lottery_num):
                    self.member_day_lottery()
                if self.member_day_black:
                    return
                self.member_day_task_list()
                if self.member_day_black:
                    return
                self.member_day_red_packet_status()
            else:
                error_message = response.get('errorMessage', '无返回')
                Log(f'📝 查询会员日失败: {error_message}')
                if '没有资格参与活动' in error_message:
                    self.member_day_black = True
                    Log('📝 会员日任务风控')
        except Exception as e:
            print(e)

    def member_day_receive_invite_award(self, invite_user_id):
        try:
            payload = {'inviteUserId': invite_user_id}

            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~memberDayIndexService~receiveInviteAward'

            response = self.do_request(url, payload)
            if response.get('success'):
                product_name = response.get('obj', {}).get('productName', '空气')
                Log(f'🎁 会员日奖励: {product_name}')
            else:
                error_message = response.get('errorMessage', '无返回')
                Log(f'📝 领取会员日奖励失败: {error_message}')
                if '没有资格参与活动' in error_message:
                    self.member_day_black = True
                    Log('📝 会员日任务风控')
        except Exception as e:
            print(e)

    def member_day_lottery(self):
        try:
            payload = {}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~memberDayLotteryService~lottery'

            response = self.do_request(url, payload)
            if response.get('success'):
                product_name = response.get('obj', {}).get('productName', '空气')
                Log(f'🎁 会员日抽奖: {product_name}')
            else:
                error_message = response.get('errorMessage', '无返回')
                Log(f'📝 会员日抽奖失败: {error_message}')
                if '没有资格参与活动' in error_message:
                    self.member_day_black = True
                    Log('📝 会员日任务风控')
        except Exception as e:
            print(e)

    def member_day_task_list(self):
        try:
            payload = {'activityCode': 'MEMBER_DAY', 'channelType': 'MINI_PROGRAM'}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~activityTaskService~taskList'

            response = self.do_request(url, payload)
            if response.get('success'):
                task_list = response.get('obj', [])
                for task in task_list:
                    if task['status'] == 1:
                        if self.member_day_black:
                            return
                        self.member_day_fetch_mix_task_reward(task)
                for task in task_list:
                    if task['status'] == 2:
                        if self.member_day_black:
                            return
                        if task['taskType'] in ['SEND_SUCCESS', 'INVITEFRIENDS_PARTAKE_ACTIVITY', 'OPEN_SVIP',
                                                'OPEN_NEW_EXPRESS_CARD', 'OPEN_FAMILY_CARD', 'CHARGE_NEW_EXPRESS_CARD',
                                                'INTEGRAL_EXCHANGE']:
                            pass
                        else:
                            for _ in range(task['restFinishTime']):
                                if self.member_day_black:
                                    return
                                self.member_day_finish_task(task)
            else:
                error_message = response.get('errorMessage', '无返回')
                Log('📝 查询会员日任务失败: ' + error_message)
                if '没有资格参与活动' in error_message:
                    self.member_day_black = True
                    Log('📝 会员日任务风控')
        except Exception as e:
            print(e)

    def member_day_finish_task(self, task):
        try:
            payload = {'taskCode': task['taskCode']}

            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberEs~taskRecord~finishTask'

            response = self.do_request(url, payload)
            if response.get('success'):
                Log('📝 完成会员日任务[' + task['taskName'] + ']成功')
                self.member_day_fetch_mix_task_reward(task)
            else:
                error_message = response.get('errorMessage', '无返回')
                Log('📝 完成会员日任务[' + task['taskName'] + ']失败: ' + error_message)
                if '没有资格参与活动' in error_message:
                    self.member_day_black = True
                    Log('📝 会员日任务风控')
        except Exception as e:
            print(e)

    def member_day_fetch_mix_task_reward(self, task):
        try:
            payload = {'taskType': task['taskType'], 'activityCode': 'MEMBER_DAY', 'channelType': 'MINI_PROGRAM'}

            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~activityTaskService~fetchMixTaskReward'

            response = self.do_request(url, payload)
            if response.get('success'):
                Log('🎁 领取会员日任务[' + task['taskName'] + ']奖励成功')
            else:
                error_message = response.get('errorMessage', '无返回')
                Log('📝 领取会员日任务[' + task['taskName'] + ']奖励失败: ' + error_message)
                if '没有资格参与活动' in error_message:
                    self.member_day_black = True
                    Log('📝 会员日任务风控')
        except Exception as e:
            print(e)

    def member_day_receive_red_packet(self, hour):
        try:
            payload = {'receiveHour': hour}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~memberDayTaskService~receiveRedPacket'

            response = self.do_request(url, payload)
            if response.get('success'):
                print(f'🎁 会员日领取{hour}点红包成功')
            else:
                error_message = response.get('errorMessage', '无返回')
                print(f'📝 会员日领取{hour}点红包失败: {error_message}')
                if '没有资格参与活动' in error_message:
                    self.member_day_black = True
                    Log('📝 会员日任务风控')
        except Exception as e:
            print(e)

    def member_day_red_packet_status(self):
        try:
            payload = {}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~memberDayPacketService~redPacketStatus'
            response = self.do_request(url, payload)
            if response.get('success'):
                packet_list = response.get('obj', {}).get('packetList', [])
                for packet in packet_list:
                    self.member_day_red_packet_map[packet['level']] = packet['count']

                for level in range(1, self.max_level):
                    count = self.member_day_red_packet_map.get(level, 0)
                    while count >= 2:
                        self.member_day_red_packet_merge(level)
                        count -= 2
                packet_summary = []
                remaining_needed = 0

                for level, count in self.member_day_red_packet_map.items():
                    if count == 0:
                        continue
                    packet_summary.append(f"[{level}级]X{count}")
                    int_level = int(level)
                    if int_level < self.max_level:
                        remaining_needed += 1 << (int_level - 1)

                Log("📝 会员日合成列表: " + ", ".join(packet_summary))

                if self.member_day_red_packet_map.get(self.max_level):
                    Log(f"🎁 会员日已拥有[{self.max_level}级]红包X{self.member_day_red_packet_map[self.max_level]}")
                    self.member_day_red_packet_draw(self.max_level)
                else:
                    remaining = self.packet_threshold - remaining_needed
                    Log(f"📝 会员日距离[{self.max_level}级]红包还差: [1级]红包X{remaining}")

            else:
                error_message = response.get('errorMessage', '无返回')
                Log(f'📝 查询会员日合成失败: {error_message}')
                if '没有资格参与活动' in error_message:
                    self.member_day_black = True
                    Log('📝 会员日任务风控')
        except Exception as e:
            print(e)

    def member_day_red_packet_merge(self, level):
        try:
            # for key,level in enumerate(self.member_day_red_packet_map):
            #     pass
            payload = {'level': level, 'num': 2}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~memberDayPacketService~redPacketMerge'

            response = self.do_request(url, payload)
            if response.get('success'):
                Log(f'🎁 会员日合成: [{level}级]红包X2 -> [{level + 1}级]红包')
                self.member_day_red_packet_map[level] -= 2
                if not self.member_day_red_packet_map.get(level + 1):
                    self.member_day_red_packet_map[level + 1] = 0
                self.member_day_red_packet_map[level + 1] += 1
            else:
                error_message = response.get('errorMessage', '无返回')
                Log(f'📝 会员日合成两个[{level}级]红包失败: {error_message}')
                if '没有资格参与活动' in error_message:
                    self.member_day_black = True
                    Log('📝 会员日任务风控')
        except Exception as e:
            print(e)

    def member_day_red_packet_draw(self, level):
        try:
            payload = {'level': str(level)}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~memberDayPacketService~redPacketDraw'
            response = self.do_request(url, payload)
            if response and response.get('success'):
                coupon_names = [item['couponName'] for item in response.get('obj', [])] or []

                Log(f"🎁 会员日提取[{level}级]红包: {', '.join(coupon_names) or '空气'}")
            else:
                error_message = response.get('errorMessage') if response else "无返回"
                Log(f"📝 会员日提取[{level}级]红包失败: {error_message}")
                if "没有资格参与活动" in error_message:
                    self.memberDay_black = True
                    print("📝 会员日任务风控")
        except Exception as e:
            print(e)

    def main(self):
        global one_msg
        wait_time = random.randint(1000, 3000) / 1000.0  
        time.sleep(wait_time)  
        one_msg = ''
        if not self.login_res: return False

        # 执行签到任务
        self.sign()
        self.superWelfare_receiveRedPacket()
        self.get_SignTaskList()
        self.get_SignTaskList(True)

        # 执行丰蜜任务
        self.get_honeyTaskListStart()
        self.honey_indexData()
        self.honey_indexData(True)

        activity_end_date = get_quarter_end_date()
        days_left = (activity_end_date - datetime.now()).days
        if days_left == 0:
            message = "⏰ 今天采蜜活动截止兑换还有{days_left}天，请及时进行兑换！！"
            Log(message)
        else:
            message = f"⏰ 今天采蜜活动截止兑换还有{days_left}天，请及时进行兑换！！\n--------------------------------"
            Log(message)

        # 执行32周年活动任务
        try:
            self.activityTaskService_taskList()
            self.activityTaskService_integralExchange()
            if self.dragonBoatGame2025Service():  # 只有在成功获取游戏信息时才继续
                if not self.ifPassAllLevel:
                    index = 1
                    count = 4
                    while count > 0:
                        self.dragonBoatGame2025ServiceWin(index)
                        index += 1
                        count -= 1
                        time.sleep(1.5)
                self.dragonBoat2025HastenService()
                while self.lotteryNum and self.lotteryNum > 0:
                    self.hastenLottery()
                    time.sleep(1)
                    self.getUpgradeStatus()
                    self.lotteryNum -= 1
        except Exception as e:
            print(f'32周年活动执行异常: {str(e)}')

        target_time = datetime(2025, 4, 8, 19, 0)
        if datetime.now() < target_time:
            self.EAR_END_2023_TaskList()
        else:
            print('🎭 周年庆活动已结束')

        current_date = datetime.now().day
        if 26 <= current_date <= 28:
            self.member_day_index()
        else:
            print('⏰ 未到指定时间不执行会员日任务\n==================================')

        self.sendMsg()
        return True

    def sendMsg(self, help=False):
          #send("顺丰-通知", one_msg)
          pass

def get_quarter_end_date():
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    # 计算下个季度的第一天
    next_quarter_first_day = datetime(current_year, ((current_month - 1) // 3 + 1) * 3 + 1, 1)

    # 计算当前季度的最后一天
    quarter_end_date = next_quarter_first_day - timedelta(days=1)

    return quarter_end_date


def is_activity_end_date(end_date):
    current_date = datetime.now().date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    return current_date == end_date

if __name__ == '__main__':
    APP_NAME = '顺丰速运'
    ENV_NAME = 'sfsyUrl'
    CK_NAME = 'url'
    local_script_name = os.path.basename(__file__)
    local_version = '2025.01.06'
    token = os.getenv(ENV_NAME)
    # 将分隔符从\n改为&
    tokens = token.split('&')
    # print(tokens)
    if len(tokens) > 0:
        print(f"==================================\n🚚 共获取到{len(tokens)}个账号\n😣 修改By:呆呆呆呆\n==================================")
        for index, infos in enumerate(tokens):
            run_result = RUN(infos, index).main()
            if not run_result: continue