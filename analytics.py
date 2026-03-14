# import streamlit as st
# import sqlite3
# import pandas as pd
# import matplotlib.pyplot as plt


# def show_analytics():

#     st.header("📈 Inventory Analytics")

#     conn = sqlite3.connect("inventory.db")

#     df = pd.read_sql("SELECT * FROM products", conn)

#     if not df.empty:

#         st.subheader("Stock Distribution")

#         fig, ax = plt.subplots()

#         ax.bar(df["name"], df["stock"])

#         ax.set_xlabel("Products")
#         ax.set_ylabel("Stock Quantity")

#         plt.xticks(rotation=45)

#         st.pyplot(fig)

#         st.subheader("Stock Distribution")

#         fig2, ax2 = plt.subplots()

#         ax2.pie(df["stock"], labels=["name"], autopct='%1.1f%%')

#         st.pyplot(fig2)

#     else:
#         st.info("No products available")

#     conn.close()

# # AI Feature – Smart Reorder Prediction

#     st.subheader("🤖 Smart Reorder Suggestions")

#     LOW_STOCK_LIMIT = 15

#     low_stock = df[df["stock"] <= LOW_STOCK_LIMIT]

#     if not low_stock.empty:

#         st.warning("Products that should be reordered")

#         st.dataframe(low_stock)

#     else:
#         st.success("All products have sufficient stock")

import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


def show_analytics():

    st.subheader("📊 Inventory Analytics")

    conn = sqlite3.connect("inventory.db")
    df = pd.read_sql("SELECT * FROM products", conn)

    # check if table empty
    if df.empty:
        st.info("No product data available yet. Add products to see analytics.")
        conn.close()
        return

    st.divider()

    # CATEGORY DISTRIBUTION
    category_counts = df["category"].dropna().value_counts()

    if category_counts.empty:
        st.warning("No category data available")
    else:
        fig1, ax1 = plt.subplots()
        ax1.pie(category_counts, labels=category_counts.index, autopct="%1.1f%%")
        ax1.set_title("Products by Category")
        st.pyplot(fig1)

    st.divider()

    # STOCK DISTRIBUTION
    st.subheader("📊 Stock Distribution")

    stock_data = df.groupby("category")["stock"].sum()

    if stock_data.empty:
        st.warning("No stock data available")
    else:
        fig2, ax2 = plt.subplots()
        ax2.bar(stock_data.index, stock_data.values)
        ax2.set_xlabel("Category")
        ax2.set_ylabel("Stock")
        ax2.set_title("Stock by Category")

        st.pyplot(fig2)

    conn.close()