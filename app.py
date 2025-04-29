import streamlit as st
from controller import filter_stocks
from presenter import show_results
import pandas as pd

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
openai_api_key = os.getenv("OPENAI_API_KEY")


@st.cache_data
def get_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    df = pd.read_html(url)[0]
    return df["Symbol"].tolist()

tickers = get_sp500_tickers()

# UI filters
with st.form("filters"):
    st.title("S&P 500 Stock Filter App")
    pe_type = st.selectbox("Trailing or Forward P/E", ["Trailing", "Forward"])
    pe_op = st.selectbox("P/E Operator", [">", "<"])
    pe_val = st.number_input("P/E Value", value=15.0)

    de_op = st.selectbox("Debt/Equity Operator", [">", "<"])
    de_val = st.number_input("Debt/Equity Value", value=1.0)

    eps_op = st.selectbox("EPS Growth Operator", [">", "<"])
    eps_val = st.number_input("EPS Growth (%)", value=10.0)

    peg_op = st.selectbox("PEG Ratio Operator", [">", "<"])
    peg_val = st.number_input("PEG Ratio Value", value=1.0)

    mc_op = st.selectbox("Market Cap Operator", [">", "<"])
    mc_val = st.number_input("Market Cap (in billions)", value=10.0)

    submitted = st.form_submit_button("Search")

if submitted:
    filters = {
        "pe_op": pe_op,
        "pe_val": pe_val,
        "de_op": de_op,
        "de_val": de_val,
        "eps_op": eps_op,
        "eps_val": eps_val,
        "peg_op": peg_op,
        "peg_val": peg_val,
        "mc_op": mc_op,
        "mc_val": mc_val
    }
    results = filter_stocks(tickers, filters, pe_type)
    show_results(results)
