import pyupbit
import csv


def volatilityBreakoutSystem1(df):
    # 변동성 돌파전략 수익률 계산기
    df['range'] = [df['high'][i] - df['low'][i] for i in range(len(df))]
    w = max_profit_rate = max_weight = 0

    while w < 1:
        profit_rate = 1
        w += 0.01
        for i in range(100, len(df)):
            target = df['open'][i] + df['range'][i-1] * w
            if df['high'][i] >= target:
                profit_rate *= df['close'][i] / target * 0.998

        if profit_rate > max_profit_rate:
            max_profit_rate = profit_rate
            max_weight = w
        print("가중치: %.2f, 변동성 돌파전략: %.2f%%" % (w, profit_rate * 100))

    print("단순 보유: %.2f%%" % (df['open'][-1] * 100 / df['open'][0]))
    print("최대 수익률: %.2f%%, 가중치: %.2f" % (max_profit_rate * 100, max_weight))


def volatilityBreakoutSystem2(df):
    def _get_weight(df):
        weight = max_weight = max_profit_rate = 0
        while weight < 1:
            profit_rate = 100
            weight += 0.01
            for i in range(1, len(df)):
                target = df['open'][i] + df['range'][i-1] * weight
                if df['high'][i] >= target:
                    profit_rate *= df['close'][i] / target
            if profit_rate > max_profit_rate:
                max_profit_rate = profit_rate
                max_weight = weight
        return max_weight

    df['range'] = [df['high'][i] - df['low'][i] for i in range(len(df))]
    profit_rates = []
    for i in range(2, 100):
        A = []
        profit_rate = 100
        for j in range(100):
            today = 100 + j
            yesterday = today - 1
            start_date = today - i
            weight = _get_weight(df.iloc[start_date-1:yesterday+1])
            target = df['open'][today] + df['range'][yesterday] * weight
            if df['high'][today] >= target:
                profit_rate *= df['close'][today] / target
            A.append(profit_rate)
        profit_rates.append(A)

    with open('profit_rates_report.csv', 'w', newline='') as f:
        wr = csv.writer(f)
        for i in range(len(profit_rates[0])):
            wr.writerow([profit_rates[j][i] for j in range(len(profit_rates))])


df = pyupbit.get_ohlcv("KRW-BTC")
volatilityBreakoutSystem1(df)
volatilityBreakoutSystem2(df)
