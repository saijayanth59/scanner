# import packages
import streamlit as st
import plotly.express as px
import yfinance as yf
import datetime

# custom class


class Swing:
    def __init__(self, stock, period='1mo'):
        self.data = yf.download(
            tickers=stock + '.NS', period=period, progress=False).sort_index(ascending=False)
        self.high = self.data['High'].argmax()
        self.low = self.data['Low'].argmin()
        self.trend = "Upward" if self.high < self.low else 'Downward'
        self.trend_idx = min(self.high, self.low)

    def get_data(self):
        return self.data

    def indicator(self):

        if self.trend == 'Upward':
            return abs(self.data.iloc[:self.trend_idx + 1, 0] - self.data.iloc[:self.trend_idx + 1, 2]).sort_values()
        return abs(self.data.iloc[:self.trend_idx + 1, 0] - self.data.iloc[:self.trend_idx + 1, 2]).sort_values()


# sidebar
ticker = st.sidebar.text_input("Ticker", value="CIPLA")

# title
st.title(f":blue[{ticker}]")


@st.cache_data
def get_swing(stock):
    return Swing(stock)


swing = Swing(ticker)

color = 'green' if swing.trend == "Upward" else 'red'

# Data
st.subheader(f":{color}[Trend: {swing.trend}]", divider='rainbow')
show_data = st.checkbox('Show Data')
data = swing.get_data()


def highlight_extremes(val):
    color = ''
    if val == data['High'].max():
        color = 'green'
    elif val == data['Low'].min():
        color = 'red'
    return f'background-color: {color}'


styled_df = data.style.applymap(
    lambda val: highlight_extremes(val), subset=['High', 'Low'])
if show_data:
    st.dataframe(styled_df)


# line chart
st.subheader("Line Chart", divider='rainbow')
show_line_chart = st.checkbox("Show Line Chart")
if show_line_chart:
    base = st.selectbox(label=" ", options=(
        "Open", "High", "Low", "Close"), index=3)
    fig = px.line(data, x=data.index, y=base, title=ticker)
    # fig.update_traces(line_color='green')
    st.plotly_chart(fig)
