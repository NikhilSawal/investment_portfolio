import psycopg2
import os
import datetime
import pandas.io.sql as psql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

pd.set_option('display.max_rows', 20000)
pd.set_option('display.max_columns', 50)

# Setup connection with DB
pg_auth = os.environ.get("PG_AUTH")

conn = psycopg2.connect(host="localhost",
                        user="postgres",
                        dbname="investment_db",
                        password=pg_auth)

cur = conn.cursor()
cur.execute("SELECT * FROM stock_price")
rows = cur.fetchall()

# Query data
df = psql.read_sql("select * from stock_price where date > '2021-01-01 07:00:03'", conn)
df_index = psql.read_sql("select * from market_index where date > '2021-01-01 07:00:03'", conn)

print(df['name'].unique())

# Get simple moving average (SMA)
def sma(data, colName, period):
    temp = []
    for i in range(period, len(data[colName])):
        sma = round(sum(data[colName][i-period:i])/period,2)
        temp.append(sma)

    return [0 if i < period else temp[i-period] for i in range(len(data[colName]))]

# Get exponential moving average (EMA)
def ema(data, colName, period):

    alpha = 2/(period+1)
    sma_1 = sma(data, colName, period)
    temp = []

    for i in range(period, len(data[colName])):
        ema = (sum(data[colName][i:i+1])*alpha) + ((1-alpha)*sma_1[i-1])
        temp.append(ema)

    return [0 if i < period else temp[i-period] for i in range(len(data[colName]))]

# Get weighted moving average (WMA)
def wma(data, colName, period):

    denom = (period*(period+1))/2
    temp = []

    for i in range(period, len(data[colName])):

        time_window = [i for i in data[colName][i-period:i]]
        weighted = []

        for j in range(len(time_window)):

            weighted.append(time_window[j] * (j+1))

        weighted_sum = round(sum(weighted)/denom, 2)
        temp.append(weighted_sum)

    return [0 if i < period else temp[i-period] for i in range(len(data[colName]))]

style.use('ggplot')

# Make plots on moving average
def movAvg_plot(data, period_1, period_2, company=None):

    if company != None:
        df = data.loc[data['name'] == company,:].copy()
    else:
        df = data.copy()

    df.loc[:,'sma_{}'.format(period_1)] = sma(df, 'price', period_1)
    df.loc[:,'sma_{}'.format(period_2)] = sma(df, 'price', period_2)

    df.loc[:,'ema_{}'.format(period_1)] = ema(df, 'price', period_1)
    df.loc[:,'ema_{}'.format(period_2)] = ema(df, 'price', period_2)

    df.loc[:,'wma_{}'.format(period_1)] = wma(df, 'price', period_1)
    df.loc[:,'wma_{}'.format(period_2)] = wma(df, 'price', period_2)

    fig, ax = plt.subplots(3, 1)
    fig.set_figheight(15)
    fig.set_figwidth(10.5)
    top_ax, mid_ax, bottom_ax = ax

    # Simple Moving Average
    top_ax.plot(df['price'][max(period_1, period_2)+1:], label='Stock Price')
    top_ax.plot(df['sma_{}'.format(period_1)][max(period_1, period_2)+1:], label='{} period SMA'.format(period_1))
    top_ax.plot(df['sma_{}'.format(period_2)][max(period_1, period_2)+1:], label='{} period SMA'.format(period_2))
    top_ax.legend(loc='upper left', fontsize=10)
    top_ax.set_title('Simple Moving Average', fontsize=20)

    # Exponential Moving Average
    mid_ax.plot(df['price'][max(period_1, period_2)+1:], label='Stock Price')
    mid_ax.plot(df['ema_{}'.format(period_1)][max(period_1, period_2)+1:], label='{} period EMA'.format(period_1))
    mid_ax.plot(df['ema_{}'.format(period_2)][max(period_1, period_2)+1:], label='{} period EMA'.format(period_2))
    mid_ax.legend(loc='upper left', fontsize=10)
    mid_ax.set_title('Exponential Moving Average', fontsize=20)

    # Weighted Moving Average
    bottom_ax.plot(df['price'][max(period_1, period_2)+1:], label='Stock Price')
    bottom_ax.plot(df['wma_{}'.format(period_1)][max(period_1, period_2)+1:], label='{} period WMA'.format(period_1))
    bottom_ax.plot(df['wma_{}'.format(period_2)][max(period_1, period_2)+1:], label='{} period WMA'.format(period_2))
    bottom_ax.legend(loc='upper left', fontsize=10)
    bottom_ax.set_title('Weighted Moving Average', fontsize=20)

    plt.suptitle('{}'.format(company), fontsize=30, ha='center')
    plt.show()
    # fig.savefig('eda_plots/moving_avg.png')

# movAvg_plot(df, 12, 24, 'Uber Technologies, Inc. (UBER)')

# Compute different moving averages for UBER
uber_df = df.loc[df['name'] == 'Uber Technologies, Inc. (UBER)',:].copy()
uber_df = uber_df.sort_values(by=['date'])
uber_df['date'] = pd.to_datetime(uber_df['date'], format="%Y-%m-%d-%H") #.apply(lambda x: datetime.datetime.date(x))
df_index['date'] = pd.to_datetime(df_index['date'], format="%Y-%m-%d-%H")

uber_df['date'] = uber_df['date'].astype(str)
uber_df = uber_df.set_index('date')

plt.plot(uber_df['price'][:20])
plt.gcf().autofmt_xdate()
plt.show()

# uber_df.loc[:,'ema_12'] = ema(uber_df, 'price', 12)
# uber_df.loc[:,'ema_26'] = ema(uber_df, 'price', 26)
# uber_df.loc[:,'MACD'] = uber_df.loc[:,'ema_12'] - uber_df.loc[:,'ema_26']
# uber_df.loc[:,'Signal'] = ema(uber_df, 'MACD', 9)
# print(uber_df[['date', 'price']].head(30))

# fig, ax = plt.subplots(2, 1)
# fig.set_figheight(10)
# fig.set_figwidth(10)
# top_ax, bottom_ax = ax
#
# top_ax.plot(uber_df['price'][40:], label='Stock Price ($)')
# top_ax.legend(loc='upper left')
#
# bottom_ax.plot(uber_df['MACD'][40:], label='MACD')
# bottom_ax.plot(uber_df['Signal'][40:], label='Signal')
# bottom_ax.legend(loc='upper left')
# bottom_ax.set_yticks(np.arange(-2, 3))
# plt.suptitle('Moving Average Convergence Divergence (MACD) - UBER', fontsize=20, ha='center')
# plt.show()

# fig.savefig('eda_plots/macd.png')

# fig, ax = plt.subplots(4, 1)
# top_ax, mid1_ax, mid2_ax, bottom_ax = ax
#
# top_ax.plot(uber_df['date'], uber_df['price'], label='Stock Pirce')
#
# mid1_ax.plot(df_index['date'], df_index['snp_500'], label='S&P 500')
# mid2_ax.plot(df_index['date'], df_index['dow_30'], label='Dow Jones')
# bottom_ax.plot(df_index['date'], df_index['nasdaq'], label='NASDAQ')
# plt.show()

# for i in range(0, 72, 9):
#     plt.plot(uber_df['date'][i:i+9], uber_df['price'][i:i+9])
#     print(uber_df[['date', 'price']][i:i+9])
#     # i += 9
# plt.show()

# y = np.zeros(len(uber_df['date']), dtype=int)
# plt.plot(uber_df['date'], y)
# plt.plot(uber_df['date'][0:36], uber_df['price'][0:36], label='Stock Pirce')
# plt.show()

# print(len(uber_df['date']))
# print(datetime.datetime.date(pd.to_datetime('2021-01-08 16:00:03')))
