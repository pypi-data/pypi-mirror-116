import math
import pandas_datareader as web
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
import datetime


class USStocks:
    def __init__(self, code):
        self.code = code
        self.today = datetime.date.today()

    def History(self):
        df = web.DataReader(self.code, data_source='yahoo', start='2018-01-01', end=self.today)

        plt.figure(figsize=(16, 8))
        plt.title(self.code + ' \'s Close Price History')
        plt.plot(df['Close'])
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Close Price USD($)', fontsize=12)

        plt.show()


    def TrainAndPredict(self):
        df = web.DataReader(self.code, data_source='yahoo', start='2018-01-01', end=self.today)
        data = df.filter(['Close'])
        dataset = data.values
        training_data_len = math.ceil(len(dataset) * .8)

        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(dataset)

        train_data = scaled_data[0:training_data_len, :]


        x_train = []
        y_train = []
        for i in range(60, len(train_data)):
            x_train.append(train_data[i - 60:i, 0])
            y_train.append(train_data[i, 0])

        x_train, y_train = np.array(x_train), np.array(y_train)

        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        model.add(LSTM(units=50, return_sequences=False))
        model.add(Dense(units=25))
        model.add(Dense(units=1))

        model.compile(optimizer='adam', loss='mean_squared_error')

        model.fit(x_train, y_train, batch_size=1, epochs=1)

        test_data = scaled_data[training_data_len - 60:, :]

        x_test = []
        y_test = dataset[training_data_len:, :]

        for i in range(60, len(test_data)):
            x_test.append(test_data[i - 60:i, 0])

        x_test = np.array(x_test)

        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

        predictions = model.predict(x_test)
        predictions = scaler.inverse_transform(predictions)

        rmse = np.sqrt(np.mean(((predictions - y_test) ** 2)))


        train = data[:training_data_len]
        valid = data[training_data_len:]
        valid['Predictions'] = predictions

        plt.figure(figsize=(16, 8))
        plt.title(self.code + ' \'s Close Price Train')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Close Price USD ($)', fontsize=12)
        plt.plot(train['Close'])
        plt.plot(valid[['Close', 'Predictions']])
        plt.legend(['Train', 'Actual', 'Predictions'], loc='lower right')
        plt.show()



        apple_quote = web.DataReader('AAPL', data_source='yahoo', start='2018-01-01', end=self.today)

        new_df = apple_quote.filter(['Close'])

        last_60_days = new_df[-60:].values
        last_60_days_scaled = scaler.transform(last_60_days)

        X_test = []
        X_test.append(last_60_days_scaled)
        X_test = np.array(X_test)

        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

        pred_price = model.predict(X_test)
        pred_price = scaler.inverse_transform(pred_price)
        print(pred_price)


        ### 一次循环
        day1 = datetime.date.today()

        number = float(pred_price)
        new_df.loc[day1] = [number]

        last_60_days = new_df[-60:].values
        last_60_days_scaled = scaler.transform(last_60_days)

        X_test = []
        X_test.append(last_60_days_scaled)
        X_test = np.array(X_test)

        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

        pred_price = model.predict(X_test)
        pred_price = scaler.inverse_transform(pred_price)
        print(pred_price)

        hello = {'Close': [number]}
        week_data = pd.DataFrame(hello, index=[day1])

        ###二次循环
        day2 = day1 + datetime.timedelta(days=1)

        number = float(pred_price)
        new_df.loc[day2] = [number]

        last_60_days = new_df[-60:].values
        last_60_days_scaled = scaler.transform(last_60_days)

        X_test = []
        X_test.append(last_60_days_scaled)
        X_test = np.array(X_test)

        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

        pred_price = model.predict(X_test)
        pred_price = scaler.inverse_transform(pred_price)
        print(pred_price)


        week_data.loc[day2] = [number]

        ###三次循环
        day3 = day2 + datetime.timedelta(days=1)

        number = float(pred_price)
        new_df.loc[day3] = [number]

        last_60_days = new_df[-60:].values
        last_60_days_scaled = scaler.transform(last_60_days)

        X_test = []
        X_test.append(last_60_days_scaled)
        X_test = np.array(X_test)

        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

        pred_price = model.predict(X_test)
        pred_price = scaler.inverse_transform(pred_price)
        print(pred_price)

        week_data.loc[day3] = [number]

        ###四次循环
        day4 = day3 + datetime.timedelta(days=1)

        number = float(pred_price)
        new_df.loc[day4] = [number]

        last_60_days = new_df[-60:].values
        last_60_days_scaled = scaler.transform(last_60_days)

        X_test = []
        X_test.append(last_60_days_scaled)
        X_test = np.array(X_test)

        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

        pred_price = model.predict(X_test)
        pred_price = scaler.inverse_transform(pred_price)
        print(pred_price)

        week_data.loc[day4] = [number]

        ###五次循环
        day5 = day4 + datetime.timedelta(days=1)

        number = float(pred_price)
        new_df.loc[day5] = [number]

        last_60_days = new_df[-60:].values
        last_60_days_scaled = scaler.transform(last_60_days)

        X_test = []
        X_test.append(last_60_days_scaled)
        X_test = np.array(X_test)

        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

        pred_price = model.predict(X_test)
        pred_price = scaler.inverse_transform(pred_price)
        print(pred_price)

        week_data.loc[day5] = [number]

        ###六次循环
        day6 = day5 + datetime.timedelta(days=1)

        number = float(pred_price)
        new_df.loc[day6] = [number]

        last_60_days = new_df[-60:].values
        last_60_days_scaled = scaler.transform(last_60_days)

        X_test = []
        X_test.append(last_60_days_scaled)
        X_test = np.array(X_test)

        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

        pred_price = model.predict(X_test)
        pred_price = scaler.inverse_transform(pred_price)
        print(pred_price)

        week_data.loc[day6] = [number]

        ###七次循环
        day7 = day6 + datetime.timedelta(days=1)

        number = float(pred_price)
        new_df.loc[day7] = [number]

        last_60_days = new_df[-60:].values
        last_60_days_scaled = scaler.transform(last_60_days)

        X_test = []
        X_test.append(last_60_days_scaled)
        X_test = np.array(X_test)

        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

        pred_price = model.predict(X_test)
        pred_price = scaler.inverse_transform(pred_price)
        print(pred_price)

        week_data.loc[day7] = [number]


        ### 预测一周的趋势图
        plt.figure(figsize=(16, 8))
        plt.title(self.code + ' \'s Next Week Close Price Prediction')
        plt.plot(week_data)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Close Price USD($)', fontsize=12)

        plt.show()


class CNStocks:
    def __init__(self, code):
        self.code = code
        self.today = datetime.date.today()

    def History(self):
        df = web.get_data_yahoo(self.code, '2018-01-01', self.today)

        plt.figure(figsize=(16, 8))
        plt.title(self.code + ' \'s Close Price History')
        plt.plot(df['Close'])
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Close Price CNY(¥)', fontsize=12)

        plt.show()


    def TrainAndPredict(self):
        df = web.get_data_yahoo(self.code, '2018-01-01', self.today)
        data = df.filter(['Close'])
        dataset = data.values
        training_data_len = math.ceil(len(dataset) * .8)

        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(dataset)

        train_data = scaled_data[0:training_data_len, :]


        x_train = []
        y_train = []
        for i in range(60, len(train_data)):
            x_train.append(train_data[i - 60:i, 0])
            y_train.append(train_data[i, 0])

        x_train, y_train = np.array(x_train), np.array(y_train)

        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        model.add(LSTM(units=50, return_sequences=False))
        model.add(Dense(units=25))
        model.add(Dense(units=1))

        model.compile(optimizer='adam', loss='mean_squared_error')

        model.fit(x_train, y_train, batch_size=1, epochs=1)

        test_data = scaled_data[training_data_len - 60:, :]

        x_test = []
        y_test = dataset[training_data_len:, :]

        for i in range(60, len(test_data)):
            x_test.append(test_data[i - 60:i, 0])

        x_test = np.array(x_test)

        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

        predictions = model.predict(x_test)
        predictions = scaler.inverse_transform(predictions)

        rmse = np.sqrt(np.mean(((predictions - y_test) ** 2)))


        train = data[:training_data_len]
        valid = data[training_data_len:]
        valid['Predictions'] = predictions

        plt.figure(figsize=(16, 8))
        plt.title(self.code + ' \'s Close Price Train')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Close Price CNY(¥)', fontsize=12)
        plt.plot(train['Close'])
        plt.plot(valid[['Close', 'Predictions']])
        plt.legend(['Train', 'Actual', 'Predictions'], loc='lower right')
        plt.show()



        apple_quote = web.get_data_yahoo(self.code, '2018-01-01', self.today)

        new_df = apple_quote.filter(['Close'])

        last_60_days = new_df[-60:].values
        last_60_days_scaled = scaler.transform(last_60_days)

        X_test = []
        X_test.append(last_60_days_scaled)
        X_test = np.array(X_test)

        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

        pred_price = model.predict(X_test)
        pred_price = scaler.inverse_transform(pred_price)
        print(pred_price)


        ### 一次循环
        day1 = datetime.date.today()

        number = float(pred_price)
        new_df.loc[day1] = [number]

        last_60_days = new_df[-60:].values
        last_60_days_scaled = scaler.transform(last_60_days)

        X_test = []
        X_test.append(last_60_days_scaled)
        X_test = np.array(X_test)

        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

        pred_price = model.predict(X_test)
        pred_price = scaler.inverse_transform(pred_price)
        print(pred_price)

        hello = {'Close': [number]}
        week_data = pd.DataFrame(hello, index=[day1])

        ###二次循环
        day2 = day1 + datetime.timedelta(days=1)

        number = float(pred_price)
        new_df.loc[day2] = [number]

        last_60_days = new_df[-60:].values
        last_60_days_scaled = scaler.transform(last_60_days)

        X_test = []
        X_test.append(last_60_days_scaled)
        X_test = np.array(X_test)

        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

        pred_price = model.predict(X_test)
        pred_price = scaler.inverse_transform(pred_price)
        print(pred_price)


        week_data.loc[day2] = [number]

        ###三次循环
        day3 = day2 + datetime.timedelta(days=1)

        number = float(pred_price)
        new_df.loc[day3] = [number]

        last_60_days = new_df[-60:].values
        last_60_days_scaled = scaler.transform(last_60_days)

        X_test = []
        X_test.append(last_60_days_scaled)
        X_test = np.array(X_test)

        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

        pred_price = model.predict(X_test)
        pred_price = scaler.inverse_transform(pred_price)
        print(pred_price)

        week_data.loc[day3] = [number]

        ###四次循环
        day4 = day3 + datetime.timedelta(days=1)

        number = float(pred_price)
        new_df.loc[day4] = [number]

        last_60_days = new_df[-60:].values
        last_60_days_scaled = scaler.transform(last_60_days)

        X_test = []
        X_test.append(last_60_days_scaled)
        X_test = np.array(X_test)

        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

        pred_price = model.predict(X_test)
        pred_price = scaler.inverse_transform(pred_price)
        print(pred_price)

        week_data.loc[day4] = [number]

        ###五次循环
        day5 = day4 + datetime.timedelta(days=1)

        number = float(pred_price)
        new_df.loc[day5] = [number]

        last_60_days = new_df[-60:].values
        last_60_days_scaled = scaler.transform(last_60_days)

        X_test = []
        X_test.append(last_60_days_scaled)
        X_test = np.array(X_test)

        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

        pred_price = model.predict(X_test)
        pred_price = scaler.inverse_transform(pred_price)
        print(pred_price)

        week_data.loc[day5] = [number]

        ###六次循环
        day6 = day5 + datetime.timedelta(days=1)

        number = float(pred_price)
        new_df.loc[day6] = [number]

        last_60_days = new_df[-60:].values
        last_60_days_scaled = scaler.transform(last_60_days)

        X_test = []
        X_test.append(last_60_days_scaled)
        X_test = np.array(X_test)

        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

        pred_price = model.predict(X_test)
        pred_price = scaler.inverse_transform(pred_price)
        print(pred_price)

        week_data.loc[day6] = [number]

        ###七次循环
        day7 = day6 + datetime.timedelta(days=1)

        number = float(pred_price)
        new_df.loc[day7] = [number]

        last_60_days = new_df[-60:].values
        last_60_days_scaled = scaler.transform(last_60_days)

        X_test = []
        X_test.append(last_60_days_scaled)
        X_test = np.array(X_test)

        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

        pred_price = model.predict(X_test)
        pred_price = scaler.inverse_transform(pred_price)
        print(pred_price)

        week_data.loc[day7] = [number]


        ### 预测一周的趋势图
        plt.figure(figsize=(16, 8))
        plt.title(self.code + ' \'s Next Week Close Price Prediction')
        plt.plot(week_data)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Close Price CNY(¥)', fontsize=12)

        plt.show()
