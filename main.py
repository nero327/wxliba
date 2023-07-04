import datetime
import threading
import requests
import time
import json
import os
import hashlib
import uuid
import sys

id = ""
password = ""
ime = ""
max = ""

# begin = 0
begin = 11 * 3600 + 59 * 60 + 50
end = 12 * 3600 + 0 * 60 + 30
# stime=14 * 3600 + 29 * 60 + 55
time_out = 2.3
# time_out = 0.1
url = "************************"
Pushurl = 'http://www.pushplus.plus/send'
token = ['**************************']  # 在pushpush网站中可以找到
title = '座位信息'  # 改成你要的标题内容
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
amount = 0
text = []
text1 = []
users = []
user1 = {
    'id': 1,
    'userPhysicalCard': id,
    'password': password,
    'imei': ime,
    'token': '',
    'seatId': '',
    'haveseat': 0,
    'seatNo': "",
    'roomId': '',
    'reservedid': "",
}


def read_credentials(filename):
    with open(filename) as f:
        room = f.readline().strip()
        seatNO = f.readline().strip()
    return (room, seatNO)



def getuuid():
    s_uuid = str(uuid.uuid4())
    l_uuid = s_uuid.split('-')
    s_uuid = ''.join(l_uuid)[0:20]
    return s_uuid


def tvers():
    return int(str(time.time() * 1000)[0:13])


# c8753253f24ff8638b99
def login(userPhysicalCard, password, imei):
    payload = json.dumps({
        "intf_code": "QRY_LOGIN",
        "params": {
            "userPhysicalCard": userPhysicalCard,
            "password": password,
            "imei": imei,
            "pushid": 'c8753253f24ff8638fff',
            "os": "android",
            "wmac": '*******************',
            "version": "2.9.6",
            "tversion": 1665553048528,
            "md5username": '*******************',
        }
    })
    headers = {
        'host': '***************************',
        'accept': '*/*',
        'charset': 'UTF-8',
        'connection': 'Keep-Alive',
        'user-agent': 'Mozilla/5.0 (Linux; Android 11; MI 11 Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/105.0.5195.136 Mobile Safari/537.36',
        'content-type': 'text/plain; charset=UTF-8',
        'authorization': '',
        'content-length': '282',
        'accept-encoding': 'gzip'
    }
    attempts = 0
    global amount
    success = False
    while attempts < 3 and not success:
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            # print(response.text)
            token1 = response.json()['result_data']['token']
            i.update(token=token1)
            print('账号' + str(i['id']) + '|' + str(i['userPhysicalCard']) + '登录成功')
            success = True
            amount += 1
        except Exception as e:
            print('账号' + str(i['id']) + "登陆失败原因是：" + str(e))
            attempts += 1
            if attempts == 2:
                break


def reserved(userPhysicalCard, token):
    payload = json.dumps({
        "intf_code": "QRY_RECORD",
        "params": {
            "userPhysicalCard": userPhysicalCard,
            "flag": "0"
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'authorization': token,
    }
    # response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.text)
    try:
        response = requests.request("POST", url, headers=headers, data=payload, timeout=1.8)
        totalPage = response.json()["result_data"]['totalPage']
        # print(response.text)
        if totalPage == 0:
            print('今天账号' + str(i['id']) + '|' + str(i['userPhysicalCard']) + '未查询到任何座位信息\n')
        else:
            seatId = response.json()["result_data"]["rows"][0]["seatId"]
            reservid = response.json()["result_data"]["rows"][0]["id"]
            i.update(reservedid=reservid)
            t1 = response.json()["result_data"]["rows"][0]["appointmentDate"]
            t2 = tvers()
            t3 = int(t1 + 21600000)

            # print(t3)
            # t3=t1+
            mes = response.json()["result_data"]["rows"][0]["roomName"] + response.json()["result_data"]["rows"][0][
                "seatNo"]
            status = response.json()["result_data"]["rows"][0]["status"]
            if status == 1 and t1 > t2:
                print('明天账号' + str(i['id']) + '|' + str(i['userPhysicalCard']) + '可入座的座位是' + mes + '\n')
                text1.append('账号' + str(i['id']) + '|' + mes + '\n')
            elif status == 1 and t3 < t2:
                print('今天账号' + str(i['id']) + '|' + str(i['userPhysicalCard']) + '可入座的座位是' + mes + '\n')
                i.update(haveseat=1, seatId=seatId)
                text.append('账号' + str(i['id']) + '|' + mes + '\n')
            elif status == 2:
                print('今天账号' + str(i['id']) + '|' + str(i['userPhysicalCard']) + '已经入座' + mes + '\n')
                text.append('账号' + str(i['id']) + '|' + mes + '\n')
            elif status == 4:
                print('今天账号' + str(i['id']) + '|' + str(i['userPhysicalCard']) + '超时未入座' + mes + '\n')
                text.append('账号' + str(i['id']) + '|' + '未入坐' + mes + '\n')
            elif status == 6:
                print('今天账号' + str(i['id']) + '|' + str(i['userPhysicalCard']) + '已从' + mes + '离座' + '\n')
                text.append('账号' + str(i['id']) + '|' + mes + '离座' + '\n')
            else:
                print('今天账号' + str(i['id']) + '|' + str(i['userPhysicalCard']) + '未查询到座位信息\n')
    except Exception as e:
        print('reserederro：' + str(e))
        text.append(str(i['id']) + '账号异常')
        text1.append(str(i['id']) + '账号异常')
        pass


def checkin(userPhysicalCard, token, imei, seatId, haveseat, reservedid):
    payload = json.dumps({
        "intf_code": "UPD_SCAN_SEAT",
        "params": {
            "userPhysicalCard": userPhysicalCard,
            "deviceType": "mix",
            "dvModel": "MI 9",
            "sysVersion": "11",
            "operType": "click",
            "imei": str(imei),
            "reback": "",
            "seatId": seatId,
            "bssid": "**************",
            "phoneSystem": "android",
            "mixBssid": "",
            "appVersion": 1,
            "version": "2.9.6",
            "tversion": tvers(),
            "md5username": "******************",
            "reservedId": str(reservedid),
        }
    })
    headers = {
        'authorization': token,
        "sign": sign(),
        "sign2": sign2(),
    }
    if haveseat == 1:
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.text)
            if response.status_code == 200:
                text.append('账号' + str(i['id']) + '入座成功\n')
        except Exception as e:
            print("入座异常" + str(e))
            pass
    else:
        print('账号' + str(i['id']) + '|' + str(i['userPhysicalCard']) + '还不能入座\n')


def bookseat(userPhysicalCard, token, seatNo, roomId, dateStr, id):
    now = get_now()
    while 1:
        if now < end:
            now = get_now()
            payload = json.dumps({
                "intf_code": "UPD_PRE_SEAT",
                "params": {
                    "seatNo": seatNo,
                    "roomId": str(roomId),
                    "dateStr": dateStr,
                    "startHour": "6:30",
                    "endHour": "23:00",
                    "userPhysicalCard": str(userPhysicalCard),
                    "version": "2.9.6"
                }
            })
            headers = {
                'authorization': token,
                "Connection": 'keep-alive',
            }
            try:
                # if id<=8:
                #    requests.request("POST", url, headers=headers, data=payload)
                # # requests.request("POST", url, headers=headers, data=payload, timeout=0.3)
                # else:
                # requests.request("POST", url, headers=headers, data=payload, timeout=1.5)
                # if (now < 43200):
                # if (now < stime):
                #     requests.request("POST", url, headers=headers, data=payload, timeout=0.6)
                # else:
                a = requests.request("POST", url, headers=headers, data=payload, timeout=time_out)
                # print('账号' + str(id) + '正在抢座' + str(datetime.datetime.now()))
                print('账号' + str(id) + '正在抢座' + str(datetime.datetime.now()) + '超时为：' + str(time_out))
                print(a.text)
                # if '座位预占成功' in a.text:
                #     text1.append('账号' + str(id) + '预约' + str('203' if str(roomId) == '10' else '202') + '-' + str(
                #         seatNo) + '成功\n')
                #     print('账号' + str(id) + '预约' + str('203' if str(roomId) == '10' else '202') + '-' + str(
                #         seatNo) + '成功\n'+str(datetime.datetime.now()))
            except requests.exceptions.RequestException as e:
                print('账号' + str(id) + str(e))
                time.sleep(5)
                # if (time_out <= 5):
                #     time_out += 0.3
                pass
        else:
            time.sleep(10)
            break


def pushplus(token):
    print("正在推送信息")
    content1 = "".join(str(e) for e in text)
    content2 = "".join(str(e) for e in text1)
    print(content1 + content2)
    data = {
        "token": token,
        "title": title,
        "content": content1 + content2
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    requests.post(Pushurl, data=body, headers=headers)
    print("信息推送完成")


def Kaoyan():
    a = datetime.datetime.now()  # 实施时间
    y = str(a.year)
    m = str(a.month)
    d = str(a.day)  # 转换为字符串，便于打印
    b = datetime.datetime(2022, 12, 24)  # 自己设置的研究生考试时间
    count_down = (b - a).days  # 考研倒计时
    return count_down


def get_now():
    b = time.localtime()
    c = b.tm_hour * 3600 + b.tm_min * 60 + b.tm_sec
    return c


def true_room(roomnu):
    if roomnu == 203:
        return 10
    elif roomnu == 202:
        return 9
    elif roomnu == 101:
        return 12
    else:
        print("输入自习室号错误")
        time.sleep(3)
        quit()


class Logger(object):
    def __init__(self, filename='log\\book{a}.log'.format(a=today), stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


if __name__ == '__main__':
    folder_path = os.getcwd() + '/log'
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    room, seatId = read_credentials('room.txt')
    user1.update(roomId=true_room(int(room)), seatNo=seatId)
    print("座位信息:")
    print(room, user1['seatNo'])
    sys.stdout = Logger(stream=sys.stdout)
    print("当前时间:")
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time()))))
    print("到期时间:")
    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(max)))
    print(time_str)
    # text.append('距离考研还有：' + str(Kaoyan()) + '天' + '\n')
    text.append("今天\n")
    # text1.append("1231313131\n")
    users = []
    users.append(user1)
    threads1 = []
    threads2 = []
    threads3 = []
    # threads4 = []
    # threads5 = []
    # threads6 = []
    if int(max) >= int(time.time()):

        if begin < end:
            for i in users:
                login(i['userPhysicalCard'], i['password'], i['imei'])
            text.append("进程2登录成功：" + str(amount) + '个账号')
            title = "进程2登录成功：" + str(amount) + '个账号'
            print('登录完成开始等待抢座')
            # pushplus(token[0])
            # print(user1['roomId'], user1['seatNo'])
            while 1:
                now = get_now()
                time.sleep(1)
                if now >= begin:
                    for i in users:
                        threads1.append(threading.Thread(target=bookseat, args=(
                            i['userPhysicalCard'], i['token'], i['seatNo'], i['roomId'], str(tomorrow), i['id'])))
                        threads2.append(threading.Thread(target=bookseat, args=(
                            i['userPhysicalCard'], i['token'], i['seatNo'], i['roomId'], str(tomorrow), i['id'])))
                        # threads3.append(threading.Thread(target=bookseat, args=(
                        #     i['userPhysicalCard'], i['token'], i['seatNo'], i['roomId'], str(tomorrow), i['id'])))
                    for t in threads1:
                        t.start()
                    for t in threads2:
                        t.start()
                    # for t in threads3:
                    #     t.start()
                    break
                elif now < begin:
                    mins, secs = divmod(begin - now, 60)
                    print("\r", end='')
                    print("距离预约开始还有：" + str(mins) + "分:" + str(secs) + "秒", end='', flush=True)
        else:
            print("开始结束时间错误")
    else:
        print("已过期\n")
        time.sleep(10)
