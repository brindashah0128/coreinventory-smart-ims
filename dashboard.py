import streamlit as st
import sqlite3
import pandas as pd
from analytics import show_analytics

def show_dashboard():

    st.header("Inventory Dashboard")

    conn = sqlite3.connect("inventory.db")

    products = pd.read_sql("SELECT * FROM products", conn)

    total_products = len(products)
    total_stock = products["stock"].sum() if not products.empty else 0
    LOW_STOCK_LIMIT = 10

    # Calculate low stock FIRST
    if not products.empty:
        low_stock = products[products["stock"] <= LOW_STOCK_LIMIT]
    else:
        low_stock = pd.DataFrame()

    # col1, col2 = st.columns(2)

    # col1.metric("Total Products", total_products)
    # col2.metric("Total Stock", total_stock)

    col1, col2, col3 = st.columns(3)

    col1.metric("📦 Total Products", total_products)
    col2.metric("📊 Total Stock", total_stock)
    col3.metric("⚠ Low Stock Items", len(low_stock))

    st.divider()

    st.subheader("Low Stock Alerts")

    LOW_STOCK_LIMIT = 10

    if not products.empty:
        low_stock = products[products["stock"] <= LOW_STOCK_LIMIT]

        if low_stock.empty:
            st.success("No low stock items.")
        else:
            st.warning("Some products are running low!")

            st.dataframe(low_stock)

    st.divider()

    st.subheader("Product List")

    st.dataframe(products)

    conn.close()

    show_analytics()