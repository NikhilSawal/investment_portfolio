import psycopg2
import os
import pandas.io.sql as psql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
# import xgboost
# %matplotlib

pd.set_option('display.max_rows', 20000)
pd.set_option('display.max_columns', 50)

file_path = "/Users/nikhilsawal/OneDrive/investment_portfolio/datafiles/"
file_name = "stock_prices.jl"
pg_auth = os.environ.get("PG_AUTH")

# print(pg_auth)

conn = psycopg2.connect(host="localhost",
                        user="postgres",
                        dbname="investment_db",
                        password=pg_auth)

cur = conn.cursor()
cur.execute("SELECT * FROM stock_price")
rows = cur.fetchall()

df = psql.read_sql('select * from stock_price', conn)
df_index = psql.read_sql('select * from market_index', conn)

def sma(data, colName, period):
    temp = []
    for i in range(period, len(data[colName])):
        sma = round(sum(data[colName][i-period:i])/period,2)
        temp.append(sma)

    return [0 if i < period else temp[i-period] for i in range(len(data[colName]))]


def ema(data, colName, period):

    alpha = 2/(period+1)
    sma_1 = sma(data, colName, period)
    temp = []

    for i in range(period, len(data[colName])):
        ema = (sum(data[colName][i:i+1])*alpha) + ((1-alpha)*sma_1[i-1])
        temp.append(ema)

    return [0 if i < period else temp[i-period] for i in range(len(data[colName]))]


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

def movAvg_plot(data, period_1, period_2, company=None):

    if company != None:
        df = data.loc[data['name'] == company,:]
    else:
        df = data

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
    fig.savefig('eda_plots/moving_avg.png')

# movAvg_plot(df, 12, 24, 'Uber Technologies, Inc. (UBER)')

uber_df = df.loc[df['name'] == 'Uber Technologies, Inc. (UBER)',:]

uber_df.loc[:,'ema_12'] = ema(uber_df, 'price', 12)
uber_df.loc[:,'ema_26'] = ema(uber_df, 'price', 26)
uber_df.loc[:,'MACD'] = uber_df.loc[:,'ema_12'] - uber_df.loc[:,'ema_26']
uber_df.loc[:,'Signal'] = ema(uber_df, 'MACD', 9)

fig, ax = plt.subplots(2, 1)
fig.set_figheight(10)
fig.set_figwidth(10)
top_ax, bottom_ax = ax

top_ax.plot(uber_df['price'][40:], label='Stock Price ($)')
top_ax.legend(loc='upper left')

bottom_ax.plot(uber_df['MACD'][40:], label='MACD')
bottom_ax.plot(uber_df['Signal'][40:], label='Signal')
bottom_ax.legend(loc='upper left')
bottom_ax.set_yticks(np.arange(-2, 3))

plt.suptitle('Moving Average Convergence Divergence (MACD) - UBER', fontsize=20, ha='center')
# fig.savefig('eda_plots/macd.png')


fig, ax = plt.subplots(4, 1)
top_ax, mid1_ax, mid2_ax, bottom_ax = ax

top_ax.plot(uber_df['price'], label='Stock Pirce')

mid1_ax.plot(df_index['snp_500'], label='S&P 500')
mid2_ax.plot(df_index['dow_30'], label='Dow Jones')
bottom_ax.plot(df_index['nasdaq'], label='NASDAQ')
plt.show()
# print(df_index.head())
