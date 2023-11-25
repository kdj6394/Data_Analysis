import numpy as np
import tensorflow as tf
from pandas import read_csv
from keras.models import Sequential
from keras.layers.core import Dense
from keras.layers import LSTM
import sys,os
from os.path import join
import random

def _load_data(df, n_prev=100):
    docX, docY = [], []
    for i in range(len(df) - n_prev):
        docX.append(df.iloc[i:i + n_prev].values)
        docY.append(df.iloc[i + n_prev].values)
    alsX = np.array(docX)
    alsY = np.array(docY)
    return alsX, alsY

def train_test_split(df, test_size=0.15):
    num_train = round(len(df) * (1 - test_size))
    X_train, y_train = _load_data(df.iloc[0:num_train])
    X_test, y_test = _load_data(df.iloc[num_train:])
    return X_train, y_train, X_test, y_test

if __name__ == '__main__':
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            # Currently, memory growth needs to be the same across GPUs
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            logical_gpus = tf.config.experimental.list_logical_devices('GPU')
            print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            # Memory growth must be set before GPUs have been initialized
            print(e)

    # root = sys.argv[1]
    root = r'/Users/kdj/Documents/GitHub/Data_Analysis/Lotto/data'
    path = join(root,'lottery.csv')
    COLS = [0, 1, 2, 3, 4, 5, 6]

    # load the dataset
    data = read_csv(path, header=0, index_col=0, usecols=COLS)

    predeict_list = list()

    for index,a in enumerate(range(0,5)):
        model = Sequential()
        model.add(LSTM(49, input_shape=(None, 6)))
        model.add(Dense(6, input_dim=49))
        model.compile(loss="mse", optimizer="adam")

        X_train, y_train, X_test, y_test = train_test_split(data)
        epochs_size = (index+random.randrange(5))
        model.fit(X_train, y_train, batch_size=50, epochs=epochs_size, validation_split=0.3)

        predicted = model.predict(X_test)
        rmse = np.sqrt(((predicted - y_test) ** 2).mean(axis=0))

        predeict_list.append(np.around(rmse))
        # print(f"\nPredicted numbers: {np.around(rmse)}")
        print('-------------------',index+1,'/',5,'-------------------\n')

    print('\n=======================================Prediction Number=======================================\n')
    unique_list = list()
    for p in predeict_list:
        print(p)
        for a in p:
            unique_list.append(int(a))
    