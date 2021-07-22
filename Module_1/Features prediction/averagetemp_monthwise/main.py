import pandas as pd
import tensorflow as tf
import numpy as np
from tensorflow import keras
from sklearn.model_selection import train_test_split

df = pd.read_csv('Average temperature_1901-2002.csv')
finale = pd.DataFrame()
dis_arr = np.array(df['District'].unique())
for dist in dis_arr:
    f = df.loc[df['District'] == dist]
    sing = np.array(f["State"].unique())
    arr = np.array(df.columns)
    print(arr)
    col_list = arr[3:]
    callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=3)
    ps = np.empty(shape=20)
    y = 0
    pr = np.empty(shape=0)
    years = [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020,
             2021, 2022]
    for x in col_list:
        xyz = f[x].to_numpy()
        xs = xyz[:-1]
        ys = xyz[1:]
        model = tf.keras.Sequential([
                                    tf.keras.layers.Dense(units=1, input_shape=[1]),
                                    tf.keras.layers.Dense(3),
                                    tf.keras.layers.Dense(2),
                                    tf.keras.layers.Dense(1)
                                    ])
        model.compile(optimizer='Adam', loss='mean_squared_error')
        model.fit(xs, ys, epochs=2000, callbacks=callback)
        ps[y] = model.predict([xyz[-1]])
        for i in range(19):
            ps[i+1] = model.predict([ps[i]])
            print(ps[i+1])
        pr = np.append(pr, ps)

    predictions = np.array_split(pr, 12)
    r = pd.DataFrame(predictions, columns=years, index=None)
    r.insert(0, 'State', sing[0])
    r.insert(1, 'District', dist)
    r.insert(2, 'Month', col_list)
    if dist == dis_arr[0]:
        finale = r.copy()
    else:
        finale = finale.append(r)

        
finale.to_csv('avg_temp_predictions.csv', index=False)



