import streamlit as st

st.title("S&P 500 Stock Filter App")

import pandas as pd

@st.cache_data
def load_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url)
    df = tables[0]  # the first table on the page
    return df

df_sp500 = load_sp500_tickers()
tickers = df_sp500["Symbol"].tolist()
st.subheader("S&P 500 Tickers (First 10)")
st.write(tickers[:10])
