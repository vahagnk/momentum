import pandas as pd
import strategies
import datetime
from yahoo_finance import Share

spy = Share('SPY')
spyData = spy.get_historical('2008-01-01', '2012-12-01')
df = pd.DataFrame(data=spyData)
df = df.set_index([[datetime.datetime.strptime(d, "%Y-%m-%d") for d in df.Date]])
df = df.sort(['Date'])

priceSeries = df[['Adj_Close']].rename(columns={'Adj_Close': 'price'})
resTable = pd.DataFrame(columns=['ma', 'return', 'std', 'sharpe'])
maxSharpe = 0

for index, maPeriod in enumerate([5, 10, 20, 50, 200]):
    momentumStrategy = strategies.MomentumStrategy(priceSeries, maPeriod)
    momentumStrategy.run()
    annualReturn = momentumStrategy.get_annual_return()
    annualStd = momentumStrategy.get_annual_std()
    sharpe = momentumStrategy.get_sharpe_ratio()
    if sharpe > maxSharpe:
        maxSharpe = sharpe
        maxSharpeStrategy = momentumStrategy
    resTable.loc[index] = [maPeriod, annualReturn, annualStd, sharpe]

print resTable
print "Best strategy Sharpe ratio: "+str(maxSharpe)
maxSharpeStrategy.plot()
