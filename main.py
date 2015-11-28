import pandas as pd
import strategies
import datetime
from yahoo_finance import Share

spy = Share('SPY')
spyData = spy.get_historical('2014-01-01','2015-01-01')

df = pd.DataFrame(data=spyData)
df = df.set_index([[datetime.datetime.strptime(d, "%Y-%m-%d") for d in df.Date]])
df = df.sort(['Date'])

if 'Adj Close' in df:
    priceColumnName = 'Adj Close'
elif 'Adj_Close' in df:
    priceColumnName = 'Adj_Close'
elif 'price' in df:
    priceColumnName = 'price'
else:
    print "Please load price data"
    exit()

priceSeries = df[[priceColumnName]].rename(columns={priceColumnName:'price'})
momentumStrategy = strategies.MomentumStrategy(priceSeries,20)
momentumStrategy.run()
momentumStrategy.plot()
