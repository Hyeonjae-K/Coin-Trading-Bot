import pyupbit
import time
import datetime
import requests
from apscheduler.schedulers.background import BackgroundScheduler

import Secret

URL = 'https://slack.com/api/chat.postMessage'
data = {'Content-Type': 'application/x-www-form-urlencoded',
        'token': Secret.slack_token, 'channel': Secret.slack_channel, 'text': None}


def update_target():
    global target, is_updated

    while True:
        df = pyupbit.get_ohlcv("KRW-BTC", count=11)
        df_date = str(df.index[-1]).split()[0]
        today_date = str(datetime.datetime.now()).split()[0]
        if df_date == today_date:
            break
        time.sleep(0.5)
    df['range'] = [df['high'][i] - df['low'][i] for i in range(len(df))]
    bill = upbit.sell_market_order("KRW-BTC", upbit.get_balance("KRW-BTC"))
    if bill:
        data['text'] = '%s 비트코인 시장가 판매\n%s' % (
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), bill)
        requests.post(URL, data=data)

    weight = max_weight = max_profit_rate = 0
    while weight < 1:
        profit_rate = 1
        weight += 0.01
        for i in range(1, len(df)):
            target = df['open'][i] + df['range'][i-1] * weight
            if df['high'][i] >= target:
                profit_rate *= df['close'][i] / target
        if profit_rate > max_profit_rate:
            max_profit_rate = profit_rate
            max_weight = weight

    weight = max_weight
    yesterday = df.iloc[-2]
    today = df.iloc[-1]
    target = today['open'] + yesterday['range'] * weight
    target = int(target / 1000)
    target *= 1000
    is_updated = True

    data['text'] = '%s 비트코인 target 업데이트\ntarget: %d' % (
        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), target)
    requests.post(URL, data=data)


sched = BackgroundScheduler()
sched.add_job(update_target, 'cron', hour='8', minute='59')
sched.start()

upbit = pyupbit.Upbit(Secret.access, Secret.secret)
target = is_updated = False
while True:
    if is_updated:
        now_price = pyupbit.get_current_price("KRW-BTC")
        if now_price >= target:
            krw_balance = upbit.get_balance("KRW")
            bill = upbit.buy_market_order("KRW-BTC", krw_balance)
            if bill:
                data['text'] = '%s 비트코인 시장가 구매\n%s' % (
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), bill)
                requests.post(URL, data=data)
            is_updated = False

    time.sleep(0.5)
