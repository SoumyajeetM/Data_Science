import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
#from keras.models import load_model
import streamlit as st

start ='2018-01-01'
end='2023-09-26'

st.title('Stock Trend Prediction')
user_input=st.text_input('Enter Stock Ticker','TSLA')
# Fetch stock data using yfinance
df = yf.download('TSLA', start=start, end=end)
st.subheader('Data 2018-2023')
st.write()
