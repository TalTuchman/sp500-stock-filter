import streamlit as st

def show_results(results):
    import pandas as pd
    if results:
        df = pd.DataFrame(results)
        st.subheader("Matching Stocks")
        st.dataframe(df)
    else:
        st.warning("No stocks matched your filters.")
