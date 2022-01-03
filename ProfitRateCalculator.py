import pyupbit


def volatilityBreakoutSystems():
    # 변동성 돌파전략 수익률 계산기
    df = pyupbit.get_ohlcv("KRW-BTC")
    df['range'] = [df['high'][i] - df['low'][i] for i in range(len(df))]
    profit_rate = 1

    for i in range(1, len(df)):
        target = df['open'][i] + df['range'][i-1] * 0.5
        if df['high'][i] >= target:
            profit_rate *= df['close'][i] / target

    print("변동성 돌파전략: %.3f%%, 단순 보유: %.3f%%" %
          (profit_rate, df['open'][-1]/df['open'][0]))


volatilityBreakoutSystems()
