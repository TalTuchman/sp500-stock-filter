from model import fetch_stock_data

def passes_filter(value, operator, threshold):
    if value is None:
        return False
    return value > threshold if operator == ">" else value < threshold

def filter_stocks(tickers, filters, pe_type):
    results = []

    for ticker in tickers:
        data = fetch_stock_data(ticker)
        if not data:
            continue

        mc = data["marketCap"]
        market_cap_bil = mc / 1e9 if mc else None

        if not passes_filter(data["trailingPE"] if pe_type == "Trailing" else data["forwardPE"], filters["pe_op"], filters["pe_val"]):
            continue
        if not passes_filter(data["debtToEquity"], filters["de_op"], filters["de_val"]):
            continue
        if not passes_filter((data["epsGrowth"] or 0) * 100, filters["eps_op"], filters["eps_val"]):
            continue
        if not passes_filter(data["pegRatio"], filters["peg_op"], filters["peg_val"]):
            continue
        if not passes_filter(market_cap_bil, filters["mc_op"], filters["mc_val"]):
            continue

        results.append(data)

    return results
