# Momentum Strategy

This is an implementation of momentum strategy for SPY using different moving average periods.

The idea of this strategy is to take long position when the Moving Average line crosses the Price line from below and close the long position when it crosses the Price line from above. So the strategy is following only the upward trend.

It is easily extensible to support other variations of the strategy (taking not only long but also short positions).

You'll be able to run the program for different moving average periods, ticker symbols and date periods. It provides a functionality of finding the best MA period and compare the results with other MA periods.
