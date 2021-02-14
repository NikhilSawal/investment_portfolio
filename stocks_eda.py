import psycopg2
import os
import pandas.io.sql as psql
import pandas as pd
import matplotlib.pyplot as plt
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


uber_df = df.loc[df['name'] == 'Uber Technologies, Inc. (UBER)',:]

uber_df.loc[:,'sma_9'] = sma(uber_df, 'price', 9)
uber_df.loc[:,'sma_12'] = sma(uber_df, 'price', 12)

uber_df.loc[:,'ema_9'] = ema(uber_df, 'price', 9)
uber_df.loc[:,'ema_12'] = ema(uber_df, 'price', 12)

uber_df.loc[:,'wma_9'] = wma(uber_df, 'price', 9)
uber_df.loc[:,'wma_12'] = wma(uber_df, 'price', 12)

# plt.figure(figsize=[10, 7.5])
# plt.plot(uber_df['price'][12:], label='Stock Price')
# plt.plot(uber_df['sma_9'][13:], label='9 period SMA')
# plt.plot(uber_df['sma_12'][13:], label='12 period SMA')
# plt.plot(uber_df['ema_9'][13:], label='9 period EMA')
# plt.plot(uber_df['ema_12'][13:], label='12 period EMA')
# plt.plot(uber_df['wma_9'][13:], label='9 period WMA')
# plt.plot(uber_df['wma_12'][13:], label='12 period WMA')
# plt.legend(loc='upper left')
# plt.title('Uber - Simple Moving Average (SMA)')
# plt.show()

fig, ax = plt.subplots(3, 1)
fig.set_figheight(15)
fig.set_figwidth(10.5)
top_ax, mid_ax, bottom_ax = ax


top_ax.plot(uber_df['price'][12:], label='Stock Price')
top_ax.plot(uber_df['sma_9'][13:], label='9 period SMA')
top_ax.plot(uber_df['sma_12'][13:], label='12 period SMA')
top_ax.legend(loc='upper left', fontsize=10)
top_ax.set_title('Simple Moving Average', fontsize=20)


mid_ax.plot(uber_df['price'][12:], label='Stock Price')
mid_ax.plot(uber_df['ema_9'][13:], label='9 period EMA')
mid_ax.plot(uber_df['ema_12'][13:], label='12 period EMA')
mid_ax.legend(loc='upper left', fontsize=10)
mid_ax.set_title('Exponential Moving Average', fontsize=20)


bottom_ax.plot(uber_df['price'][12:], label='Stock Price')
bottom_ax.plot(uber_df['wma_9'][13:], label='9 period WMA')
bottom_ax.plot(uber_df['wma_12'][13:], label='12 period WMA')
bottom_ax.legend(loc='upper left', fontsize=10)
bottom_ax.set_title('Weighted Moving Average', fontsize=20)

plt.suptitle('UBER', fontsize=50, ha='center')
# plt.show()
fig.savefig('/Users/nikhilsawal/OneDrive/investment_portfolio/eda_plots/moving_avg.png')
