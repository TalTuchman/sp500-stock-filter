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

st.header("Filter Settings")

with st.form("filters_form"):
    col1, col2 = st.columns(2)

    with col1:
        pe_type = st.selectbox("Trailing P/E or Forward P/E", ["Trailing", "Forward"])
        pe_operator = st.selectbox("P/E Filter Type", [">", "<"])
        pe_value = st.number_input("P/E Threshold", value=15.0)

        debt_operator = st.selectbox("Debt/Equity Filter Type", [">", "<"])
        debt_value = st.number_input("Debt/Equity Threshold", value=1.0)

        eps_operator = st.selectbox("EPS Growth Filter Type", [">", "<"])
