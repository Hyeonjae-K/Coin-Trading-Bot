import pyupbit
from prophet import Prophet

df = pyupbit.get_ohlcv("KRW-BTC", interval="minute60")
data = df.reset_index()
data['ds'] = data['index']
data['y'] = data['close']
data = data[['ds', 'y']]

model = Prophet(
    seasonality_mode='multiplicative',
    changepoint_prior_scale=0.5
)
model.fit(data)

future = model.make_future_dataframe(periods=24, freq='H')
forcast = model.predict(future)

print(forcast['yhat'][201:])
model.plot(forcast).savefig('forcast.png')
