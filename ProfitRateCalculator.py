import pyupbit


def volatilityBreakoutSystems(df):
    # 변동성 돌파전략 수익률 계산기
    df['range'] = [df['high'][i] - df['low'][i] for i in range(len(df))]
    w = max_profit_rate = max_weight = 0

    while w < 1:
        profit_rate = 1
        w += 0.01
        for i in range(1, len(df)):
            target = df['open'][i] + df['range'][i-1] * w
            if df['high'][i] >= target:
                profit_rate *= df['close'][i] / target

        if profit_rate > max_profit_rate:
            max_profit_rate = profit_rate
            max_weight = w
        print("가중치: %.2f, 변동성 돌파전략: %.2f%%" % (w, profit_rate * 100))

    print("단순 보유: %.2f%%" % (df['open'][-1] * 100 / df['open'][0]))
    print("최대 수익률: %.2f%%, 가중치: %.2f" % (max_profit_rate * 100, max_weight))


df = pyupbit.get_ohlcv("KRW-BTC")
volatilityBreakoutSystems(df)
