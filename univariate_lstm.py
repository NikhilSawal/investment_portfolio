import os
import pandas as pd
import pandas.io.sql as psql
import numpy as np
import matplotlib.pyplot as plt
import psycopg2

from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import MinMaxScaler

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

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
df = psql.read_sql('select * from stock_price', conn)
names = df['name'].unique()

# Filter data to company
comp_df = df[df['name']=='Twilio Inc. (TWLO)']
comp_df = comp_df.sort_values(by=['date'])

total_df = comp_df.iloc[:,3:4].values

tsv = TimeSeriesSplit(n_splits=3)
for train_index, test_index in tsv.split(total_df):
    train, test = total_df[train_index], total_df[test_index]

# Perform feature scaling on data
sc = MinMaxScaler(feature_range=(0,1))
training_set_scaled = sc.fit_transform(train)

# Create a data structure with 20 timestamps as input and 1 output
X_train = []
y_train = []
for i in range(20, training_set_scaled.shape[0]):
    X_train.append(training_set_scaled[i-20:i,0])
    y_train.append(training_set_scaled[i,0])

X_train, y_train = np.array(X_train), np.array(y_train)

# Reshape for LSTM
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

# Train and fit model
# Initialize the RNN
regressor = Sequential()

# Adding the fitst LSTM layer and some Dropout regularization
regressor.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
regressor.add(Dropout(0.2))

# Adding second layer
regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))

# Adding third layer
regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))

# Adding fourth layer
regressor.add(LSTM(units=50))
regressor.add(Dropout(0.2))

# Adding output layer
regressor.add(Dense(units=1))

# Compile the RNN
regressor.compile(optimizer='adam', loss='mean_squared_error')

# Fitting the RNN to the training set
regressor.fit(X_train, y_train, epochs=100, batch_size=32)

# Make prediction
# Get real stock price
test = np.append(train[train.shape[0]-20:,0:], test, axis=0)
test_set_scaled = sc.transform(test)

X_test = []
y_test = []
for i in range(20, test_set_scaled.shape[0]):
    X_test.append(test_set_scaled[i-20:i,0])
    y_test.append(test_set_scaled[i, 0:1])

X_test, y_test = np.array(X_test), np.array(y_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# Get predictions
predicted_stock_price = regressor.predict(X_test)

predicted_stock_price = sc.inverse_transform(predicted_stock_price)
y_test = sc.inverse_transform(y_test)

comp = np.append(predicted_stock_price, y_test, axis=1)

# Visualize the results
plt.plot(y_test, color='red', label='real stock price')
plt.plot(predicted_stock_price, color='blue', label='predicted stock price')
plt.legend()
plt.show()
