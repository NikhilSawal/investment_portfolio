import os
import numpy as np
import pandas as pd
import pandas.io.sql as psql
import matplotlib.pyplot as plt
import psycopg2

from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import MinMaxScaler

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

# SetUp connection to DB
pg_auth = os.environ.get("PG_AUTH")

conn = psycopg2.connect(host="localhost",
                        user="postgres",
                        dbname="investment_db",
                        password=pg_auth)

cur = conn.cursor()
cur.execute("SELECT * FROM stock_price")
rows = cur.fetchall()

# Query data
df = psql.read_sql("SELECT * FROM stock_price", conn)
names = df['name'].unique()

# Filter data to company
comp_df = df[df['name']=='Alphabet Inc. (GOOGL)']
comp_df = comp_df.sort_values(by=['date'])

total_df = comp_df.iloc[:,3:4].values

tsv = TimeSeriesSplit(n_splits=3)
for train_index, test_index in tsv.split(total_df):
    train, test = total_df[train_index], total_df[test_index]

print(train.shape)

# Perform feature scaling on data
sc = MinMaxScaler(feature_range=(0,1))
training_set_scaled = sc.fit_transform(train)

# Create data structure with 30 timestamps as input and 10 as output
X_train = []
y_train = []
for i in range(30, training_set_scaled.shape[0]-10):
    X_train.append(training_set_scaled[i-30:i,0])
    y_train.append(training_set_scaled[i:i+10, 0])

X_train, y_train = np.array(X_train), np.array(y_train)

# Reshape from LSTM
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

# Train and fit model
# Initialize the RNN
regressor = Sequential()

# Adding first LSTM layer and Dropout regularization
regressor.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
regressor.add(Dropout(0.2))

# Adding second layer
regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))

# Adding third layer
regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))

# Adding forth layer
regressor.add(LSTM(units=50))
regressor.add(Dropout(0.2))

# Adding output layer
regressor.add(Dense(units=10))

# Compile the RNN
regressor.compile(optimizer='adam', loss='mean_squared_error')

# Fitting the RNN to the training set
regressor.fit(X_train, y_train, epochs=100, batch_size=30)

# Make Predictions
# Get real stock prices i.e test set
test = np.append(train[train.shape[0]-30:,0:], test, axis=0)
test_set_scaled = sc.transform(test)

X_test = []
y_test = []
for i in range(30, test_set_scaled.shape[0]):
    X_test.append(test_set_scaled[i-30:i, 0])
    y_test.append(test_set_scaled[i:i+10, 0])

X_test, y_test = np.array(X_test), np.array(y_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# get predictions
predicted_stock_price = regressor.predict(X_test)

predicted_stock_price = np.reshape(predicted_stock_price[128], (predicted_stock_price[128].shape[0], 1))
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

real_stock_price = psql.read_sql("""
                                    select price from stock_price
                                    where date::date = current_date and
                                    name = 'Alphabet Inc. (GOOGL)'
                                 """, conn)


# Visualize the results
plt.plot(real_stock_price, color='red', label='Real stock prices')
plt.plot(predicted_stock_price, color='blue', label='Predicted stock prices')
plt.legend()
plt.show()
