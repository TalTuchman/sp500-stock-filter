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
        eps_value = st.number_input("EPS Growth Threshold (%)", value=10.0)

    with col2:
        peg_operator = st.selectbox("PEG Ratio Filter Type", [">", "<"])
        peg_value = st.number_input("PEG Ratio Threshold", value=1.0)

        marketcap_operator = st.selectbox("Market Cap Filter Type", [">", "<"])
        marketcap_value = st.number_input("Market Cap Threshold (in billions)", value=10.0)

    submitted = st.form_submit_button("Search Stocks")

if submitted:
    st.success("Filters applied. Running stock scan...")

import yfinance as yf

def passes_filter(value, operator, threshold):
    if value is None:
        return False
    return value > threshold if operator == ">" else value < threshold

@st.cache_data
def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "symbol": ticker,
            "name": info.get("shortName", ""),
            "trailingPE": info.get("trailingPE"),
            "forwardPE": info.get("forwardPE"),
            "debtToEquity": info.get("debtToEquity"),
            "pegRatio": info.get("pegRatio"),
            "epsGrowth": info.get("earningsQuarterlyGrowth"),
            "marketCap": info.get("marketCap")
        }
    except:
        return None

results = []

for ticker in tickers:
    data = fetch_stock_data(ticker)
    if not data:
        continue

    # Convert market cap from raw number to billions
    mc = data["marketCap"]
    market_cap_bil = mc / 1e9 if mc else None

    if not passes_filter(data["trailingPE"] if pe_type == "Trailing" else data["forwardPE"], pe_operator, pe_value):
        continue
    if not passes_filter(data["debtToEquity"], debt_operator, debt_value):
        continue
    if not passes_filter((data["epsGrowth"] or 0) * 100, eps_operator, eps_value):  # EPS is a %
        continue
    if not passes_filter(data["pegRatio"], peg_operator, peg_value):
        continue
    if not passes_filter(market_cap_bil, marketcap_operator, marketcap_value):
        continue

    results.append(data)

if results:
    st.subheader("Matching Stocks")
    df_results = pd.DataFrame(results)
    st.dataframe(df_results)
else:
    st.warning("No stocks matched your filters.")
