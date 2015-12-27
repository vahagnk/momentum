import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math
import numpy as np


class MomentumStrategy:

    def __init__(self,series, maPeriod = 5, portfolioInitialValue = 1000):
        self.__maPeriod = maPeriod
        series.price = map(float, series.price)
        self.__series = series
        self.__series['benchmark_returns'] = self.__series.price/self.__series.price.shift()-1
        self.__series['benchmark_cumulative_returns'] = self.__series.benchmark_returns.cumsum()
        self.__series['ma'] = pd.rolling_mean(series.price, maPeriod)
        self.__sharesCount = 1
        self.__cashPosition = portfolioInitialValue
        self.__position = 0
        self.__sharePosition = 0
        self.__posArr = []
        self.__cashPositionArr = []
        self.__sharePositionArr = []

    def getMa(self):
        return  self.__maPeriod

    def run(self):
        for dateIndex, dayData in self.__series.iterrows():
            self.__posArr.append(0)
            self.__cashPositionArr.append(self.__cashPosition)
            self.__sharePositionArr.append(self.__sharePosition)
            if math.isnan(dayData.ma):
                continue
            if self.__position == 0:
                if dayData.price > dayData.ma:
                    self.__position = 1
                    self.__sharesCount = self.__cashPosition/dayData.price
                    self.__cashPosition -= self.__sharesCount*dayData.price
                    self.__sharePosition += self.__sharesCount
                    self.__posArr[-1] = 1
                    # print str(dateIndex) + " LONG AT PRICE: " + str(dayData.price)
            elif dayData.price < dayData.ma:
                self.__position = 0
                self.__cashPosition += self.__sharesCount*dayData.price
                self.__sharePosition -= self.__sharesCount
                self.__posArr[-1] = 0
                # print str(dateIndex) + " SHORT AT PRICE: " + str(dayData.price)
            else:
                self.__position = 1
                self.__posArr[-1] = 1

        self.__series['position'] = self.__posArr
        self.__series['cashPosition'] = self.__cashPositionArr
        self.__series['sharePosition'] = self.__sharePositionArr
        self.__series['portfolio'] = self.__series['cashPosition']+self.__series['sharePosition']*self.__series.price
        self.__series['returns'] = self.__series['portfolio']/self.__series['portfolio'].shift()-1
        self.__series['cumulativeReturns'] = self.__series['returns'].cumsum()

    def get_series(self):
        return self.__series

    def get_value(self):
        return self.__series.portfolio[-1]

    def get_return(self):
        return self.__series.cumulativeReturns[-1]

    def get_annual_return(self):
        holdingPeriodReturn = self.get_return()
        daysCount = len(self.__series)
        return math.pow(holdingPeriodReturn+1,252.0/daysCount)-1

    def get_annual_expected_return(self):
        dailyMeanReturn = self.__series.returns.mean()
        return math.pow(dailyMeanReturn+1,252.0)-1

    def get_std(self):
        return self.__series.returns.std()

    def get_annual_std(self):
        dailyStd = self.get_std()
        return dailyStd*math.sqrt(252.0)

    def get_sharpe_ratio(self):
        return self.get_annual_expected_return()/self.get_annual_std()

    def plot(self):
        fig,ax = plt.subplots()
        ax = plt.subplot(411)
        ax.plot(self.__series.index, self.__series.price,'g', label='Price',linewidth=2)
        ax.plot(self.__series.index, self.__series.ma,'r', label='MA '+str(self.__maPeriod),linewidth=2)
        ax.legend(loc='upper left')

        returnsFig = plt.subplot(412)
        returnsFig.plot(self.__series.index, self.__series['returns'],'y',label='Simple Returns',linewidth=2)
        returnsFig.legend(loc='upper left')

        portfolioFig = plt.subplot(413)
        portfolioFig.plot(self.__series.index, self.__series['cumulativeReturns'],'b', label='Cumulative Returns',linewidth=2)
        portfolioFig.legend(loc='upper left')

        portfolioFig = plt.subplot(414)
        portfolioFig.plot(self.__series.index, self.__series['cumulativeReturns']-self.__series.benchmark_cumulative_returns,'g', label='Returns Relative to Benchmark',linewidth=2)
        portfolioFig.legend(loc='upper left')
        # format the ticks
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_minor_locator(mdates.MonthLocator())
        fig.autofmt_xdate()
        plt.show()

    @staticmethod
    def comparison_plot(priceSeries, maPeriods):
        if len(maPeriods)==0:
            return
        fig,ax = plt.subplots()

        cmap = plt.get_cmap('hsv')
        colors = [cmap(i) for i in np.linspace(0, 1, len(maPeriods)+1)]
        for index,maPeriod in enumerate(maPeriods):
            momentum = MomentumStrategy(priceSeries,maPeriod)
            momentum.run()
            series = momentum.get_series()
            ax.plot(series.index, series.cumulativeReturns,label='MA'+str(maPeriod),color=colors[index],linewidth=2)
            ax.legend(loc='upper left',ncol=2)

        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        ax.xaxis.set_minor_locator(mdates.MonthLocator())
        fig.autofmt_xdate()
        plt.show()