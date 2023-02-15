from json import dumps
from time import sleep
from requests import post, get
from datetime import datetime, timedelta


def send_msg_serverJ(SendKey, title, Text):

    if not SendKey:
        # 无SendKey则拦截推送
        return '未配置SendKey，无法进行消息推送。'
    url = f'https://sctapi.ftqq.com/{SendKey}.send?title={title}&desp={Text}'
    rsp = post(url=url)
    pushid = rsp.json()['data']['pushid']
    readkey = rsp.json()['data']['readkey']
    state_url = f'https://sctapi.ftqq.com/push?id={pushid}&readkey={readkey}'
    stop_time = datetime.now() + timedelta(minutes=0, seconds=30)
    count = 1
    while True:
        status_rsp = get(url=state_url)
        result = status_rsp.json()['data']['wxstatus']
        now_time = datetime.now()
        print(now_time, ' ---> ', stop_time, '  :  ', count)
        if result:
            return '消息推送成功！'
        elif now_time >= stop_time:
            return '程序运行结束！推送结果未知！'
        elif count >= 60:   # 防止程序一直运行
            return '程序运行结束！推送结果未知！'
        count += 1
        sleep(1)

def send_msg_pushplus(token, title, Text):

    if not token:
        # 无token则拦截推送
        return '未配置token，无法进行消息推送。'
    url = 'http://www.pushplus.plus/send/'
    headers = {'Content-Type':'application/json'}
    token = '44898c97339f450daf8a548f6080c6c6'
    data = {
        "token": token,
        "title": title,
        "content": Text,
        "template": "txt",
        "channel": "wechat"
    }
    data = dumps(data).encode(encoding='utf-8')
    rsp = post(url=url, data=data, headers=headers)
    return rsp.json()['msg']