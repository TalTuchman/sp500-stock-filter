import yfinance as yf

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
