# import packages
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import yfinance as yf
import datetime


# title
st.title(":blue[Stock Dashboard]")


# sidebar
ticker = st.sidebar.text_input("Ticker", value="MSFT")
start_date = st.sidebar.date_input(
    "Start Date", value=datetime.date(2020, 1, 1))
end_date = st.sidebar.date_input("End Date")


# getting data using yfinace
@st.cache_data
def get_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data


st.subheader(f"{ticker} DATA", divider='rainbow')
show_data = st.checkbox('Show Data')
loading_status = st.text("Data Loading...")
data = get_data(ticker, start_date, end_date)
loading_status.text("Data Loaded :)")
if show_data:
    st.dataframe(data)

# line chart
st.subheader("Line Chart", divider='rainbow')
show_line_chart = st.checkbox("Show Line Chart")
if show_line_chart:
    base = st.selectbox(label=" ", options=(
        "Open", "High", "Low", "Close"), index=3)
    fig = px.line(data, x=data.index, y=base, title=ticker)
    # fig.update_traces(line_color='green')
    st.plotly_chart(fig)
