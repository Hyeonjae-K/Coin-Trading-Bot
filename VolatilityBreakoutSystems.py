import pyupbit
import time
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

import Secret


def update_target():
    global target, is_updated, order_uuid
    print(datetime.datetime.now(), 'RUN update_target()')

    while True:
        df = pyupbit.get_ohlcv("KRW-BTC", count=11)
        df_date = str(df.index[-1]).split()[0]
        today_date = str(datetime.datetime.now()).split()[0]
        if df_date == today_date:
            break
        time.sleep(0.5)
    df['range'] = [df['high'][i] - df['low'][i] for i in range(len(df))]
    upbit.sell_market_order("KRW-BTC", upbit.get_balance("KRW-BTC"))

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
            is_updated = False
            print(datetime.datetime.now(), 'target:', target, 'bill:', bill)

    time.sleep(0.5)
