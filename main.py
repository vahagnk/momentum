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
maPeriods = [5*i for i in range(1,13)]

for maPeriod in maPeriods:
    momentumStrategy = strategies.MomentumStrategy(priceSeries,maPeriod)
    momentumStrategy.run()
    annualReturn = momentumStrategy.get_annual_return()
    annualStd = momentumStrategy.get_annual_std()
    sharpe = momentumStrategy.get_sharpe_ratio()
    if sharpe>maxSharpe:
        maxSharpe=sharpe
        maxSharpePeriod = maPeriod
    resTable.loc[len(resTable)] = [maPeriod, str(round(100*annualReturn,2))+"%", str(round(100*annualStd,2))+"%", round(sharpe,2)]

print resTable
print maxSharpe
maxSharpeStrategy = strategies.MomentumStrategy(priceSeries,maxSharpePeriod)
maxSharpeStrategy.run()

# plot graphs for the strategy with highest Sharpe ratio
maxSharpeStrategy.plot()

# plot strategies' cumulative return comparison graph for different MA periods
# strategies.MomentumStrategy.comparison_plot(priceSeries, maPeriods)
