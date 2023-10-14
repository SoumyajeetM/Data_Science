import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from keras.models import load_model
import streamlit as st

start ='2018-01-01'
end='2023-09-26'

st.title('Stock Trend Prediction')
user_input=st.text_input('Enter Stock Ticker','TSLA')
# Fetch stock data using yfinance
df = yf.download(user_input, start=start, end=end)

#Describing Data
st.subheader('Data From 2018 till Today')
st.write(df.describe())

#Visualisations
st.subheader('Closing Price Vs Time Chart with 100MA and 200MA')
ma100=df.Close.rolling(100).mean()
ma200=df.Close.rolling(200).mean()
fig=plt.figure(figsize=(12,6))
plt.plot(ma100,'r',label='MA100')
plt.plot(ma200,'g',label='MA200')
plt.xlabel('Time')
plt.ylabel('Price')
plt.plot(df.Close, label='Close')
plt.legend()
st.pyplot(fig)

data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])

from sklearn.preprocessing import MinMaxScaler
scaler=MinMaxScaler(feature_range=(0,1))
data_training_array=scaler.fit_transform(data_training)

model=load_model('keras_model.h5')

#streamlit run app.py
past_100_days=data_training.tail(100)
#final_df=past_100_days.append(data_testing, ignore_index=True)
final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
input_data=scaler.fit_transform(final_df)

#Tesing
x_test=[]
y_test=[]
for i in range(100, input_data.shape[0]):
  x_test.append(input_data[i-100:i])
  y_test.append(input_data[i,0])

x_test,y_test=np.array(x_test),np.array(y_test)

#Make Predictions
y_predicted=model.predict(x_test)

scaler=scaler.scale_
scale_factor=1/scaler[0]
y_predicted=y_predicted*scale_factor
y_test=y_test*scale_factor

st.subheader('Predicted Vs Original Price for 30% of Test data')
fig2=plt.figure(figsize=(12,6))
plt.plot(y_predicted,'r',label='Predicted Price')
plt.plot(y_test,'b',label='Original Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)

