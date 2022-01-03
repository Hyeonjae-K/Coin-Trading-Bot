import pyupbit
import time
import datetime

import Secret

upbit = pyupbit.Upbit(Secret.access, Secret.secret)


def get_target():
    df = pyupbit.get_ohlcv("KRW-BTC", "day")
    yesterday = df.iloc[-2]
    today = df.iloc[-1]
    yesterday_range = yesterday['high'] - yesterday['low']
    target = today['open'] + yesterday_range * 0.5
    return target


target = get_target()
op_mode = hold = False
while True:
    now = datetime.datetime.now()
    if now.hour == 9 and now.minute == 1 and now.second < 3:
        target = get_target()
        op_mode = True
        time.sleep(10)

    price = pyupbit.get_current_price("KRW-BTC")
    if op_mode is True and price >= target and hold is False:
        krw_balance = upbit.get_balance("KRW")
        upbit.buy_market_order("KRW-BTC", krw_balance)
        hold = True

    if now.hour == 8 and now.minute == 59 and 50 <= now.second <= 59:
        if op_mode is True and hold is True:
            btc_balance = upbit.get_balance("KRW-BTC")
            upbit.sell_market_order("KRW-BTC", btc_balance)
            hold = False
        op_mode = False
        time.sleep(10)
