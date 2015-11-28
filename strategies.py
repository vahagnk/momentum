import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math


class MomentumStrategy:

    def __init__(self,series, maPeriod=5, portfolioInitialValue = 1000):
        self.__maPeriod = maPeriod
        series.price = [float(price) for price in series.price]
        self.__series = series
        self.__series['ma'] = pd.rolling_mean(series, maPeriod)
        self.__sharesCount = 1
        self.__cashPosition = portfolioInitialValue
        self.__position = 0
        self.__sharePosition = 0
        self.__posArr = []
        self.__cashPositionArr = []
        self.__sharePositionArr = []

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
                    self.__cashPosition -= self.__sharesCount*dayData.price
                    self.__sharePosition += self.__sharesCount
                    self.__posArr[-1] = 1
                    print str(dateIndex) + " LONG AT PRICE: " + str(dayData.price)
            elif dayData.price < dayData.ma:
                self.__position = 0
                self.__cashPosition += self.__sharesCount*dayData.price
                self.__sharePosition -= self.__sharesCount
                self.__posArr[-1] = 0
                print str(dateIndex) + " SHORT AT PRICE: " + str(dayData.price)
            else:
                self.__position = 1
                self.__posArr[-1] = 1

        self.__series['position'] = self.__posArr
        self.__series['cashPosition'] = self.__cashPositionArr
        self.__series['sharePosition'] = self.__sharePositionArr
        self.__series['portfolio'] = self.__series['cashPosition']+self.__series['sharePosition']*self.__series.price
        self.__series['returns'] = self.__series['portfolio']/self.__series['portfolio'].shift()-1
        self.__series['cumulativeReturns'] = self.__series['returns'].cumsum()

    def getPortfolioValue(self):
        return self.__series.portfolio[-1]

    def getPortfolioReturn(self):
        return self.__series.cumulativeReturns[-1]

    def getPortfolioAnnualReturn(self):
        holdingPeriodReturn = self.getPortfolioReturn()
        daysCount = len(self.__series)
        return math.pow(holdingPeriodReturn+1,252.0/daysCount)-1

    def getPortfolioExpectedReturn(self):
        return self.__series.cumulativeReturns.mean()

    def getPortfolioStd(self):
        return self.__series.cumulativeReturns.std()

    def getPortfolioSharpeRatio(self):
        print self.getPortfolioExpectedReturn()/self.getPortfolioStd()

    def plot(self):
        fig,ax = plt.subplots()
        ax = plt.subplot(311)
        ax.plot(self.__series.index, self.__series.price,'g', label='Price')
        ax.plot(self.__series.index, self.__series.ma,'r', label='MA '+str(self.__maPeriod))
        ax.legend(loc='upper left')

        returnsFig = plt.subplot(312)
        returnsFig.plot(self.__series.index, self.__series['returns'],'y',label='Simple Returns')
        returnsFig.legend(loc='upper left')

        portfolioFig = plt.subplot(313)
        portfolioFig.plot(self.__series.index, self.__series['cumulativeReturns'],'b', label='Cumulative Returns')
        portfolioFig.legend(loc='upper left')
        # format the ticks
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_minor_locator(mdates.MonthLocator())
        # datemin = datetime.date(self.__series.index.min().year, 1, 1)
        # datemax = datetime.date(self.__series.index.max().year + 1, 1, 1)
        # ax.set_xlim(datemin, datemax)
        fig.autofmt_xdate()
        plt.show()

