import datetime
import pandas as pd
from ib_insync import *

pd.set_option('display.max_rows', None)

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=15)

contract = Stock('SPY', 'SMART', 'USD')

end = datetime.datetime(2022, 11, 2, 12, 17)

bars = ib.reqHistoricalData(
    contract,
    endDateTime=end,
    durationStr='1 D',
    barSizeSetting='5 secs',
    whatToShow='TRADES',
    useRTH=True,
    formatDate=1)

df = util.df(bars)

powell_start_time = "2022-11-02 14:31:15"
powell_end_time = "2022-11-02 15:16:25"

df = df.set_index('date')
df = df[powell_start_time:powell_end_time]

df.to_csv(contract.symbol + '2.csv')