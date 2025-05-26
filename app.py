# PriceSmart Global AI Agent – Enhanced Prototype (Streamlit-based UI)

import streamlit as st
import pandas as pd
from difflib import get_close_matches
import matplotlib.pyplot as plt

# --- UI Section ---
st.title("PriceSmart Global – Menu Price Benchmarking")

city = st.text_input("Enter your city (e.g., Santiago, Chile):")

st.markdown("### Add Menu Items")
menu_data = []
with st.form("menu_form"):
    item_name = st.text_input("Menu Item Name")
    portion = st.text_input("Portion Size (e.g., 350g)")
    price = st.number_input("Current Price ($)", min_value=0.0, format="%.2f")
    category = st.selectbox("Price Positioning", ["Premium", "Quality", "Value"])
    submitted = st.form_submit_button("Add to List")
    if submitted:
        menu_data.append({"Item": item_name, "Portion": portion, "Price": price, "Positioning": category})

if "menu_items" not in st.session_state:
    st.session_state.menu_items = []

if submitted:
    st.session_state.menu_items.append(menu_data[0])

if st.session_state.menu_items:
    st.markdown("### Your Menu Items")
    df_user = pd.DataFrame(st.session_state.menu_items)
    st.dataframe(df_user)

# --- Placeholder: Simulated Uber Eats Scrape Data ---
sample_data = pd.DataFrame({
    "Item": ["Chicken Caesar Salad", "Classic Cheeseburger", "Vegan Wrap"],
    "Portion": ["350g", "250g", "300g"],
    "Price": [11.25, 9.00, 7.50],
    "Positioning": ["Quality", "Premium", "Value"]
})

# --- Price Comparison ---
if st.button("Compare Prices") and st.session_state.menu_items:
    st.markdown("### Price Comparison Results")
    results = []
    for item in st.session_state.menu_items:
        match = get_close_matches(item['Item'], sample_data['Item'], n=1, cutoff=0.4)
        if match:
            matched_row = sample_data[sample_data['Item'] == match[0]].iloc[0]
            price_diff = item['Price'] - matched_row['Price']
            pct_diff = (price_diff / matched_row['Price']) * 100
            results.append({
                "Your Item": item['Item'],
                "Matched Item": matched_row['Item'],
                "Your Price": item['Price'],
                "Avg Market Price": matched_row['Price'],
                "$ Variance": round(price_diff, 2),
                "% Variance": round(pct_diff, 1),
                "Market Position": matched_row['Positioning']
            })
    if results:
        df_results = pd.DataFrame(results)
        st.dataframe(df_results)

        # --- Visualization ---
        st.markdown("### Visual Price Variance Analysis")
        fig, ax = plt.subplots()
        ax.bar(df_results["Your Item"], df_results["% Variance"], color=['green' if x >= 0 else 'red' for x in df_results["% Variance"]])
        ax.set_ylabel("% Variance vs Market")
        ax.set_title("Your Menu Pricing vs Market Average")
        st.pyplot(fig)

        # --- Export Option ---
        st.download_button(
            label="Download Report as CSV",
            data=df_results.to_csv(index=False).encode('utf-8'),
            file_name=f"pricesmart_comparison_{city.replace(' ', '_')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("No close matches found in simulated dataset. Web scraping or real API connection is needed for live data.")
