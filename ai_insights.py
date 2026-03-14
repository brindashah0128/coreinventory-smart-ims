import streamlit as st
import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np


def get_connection():
    return sqlite3.connect("inventory.db", check_same_thread=False)


def show_ai_insights():

    st.header("🤖 AI Inventory Insights")

    conn = get_connection()

    query = """
    SELECT 
        transactions.date,
        products.name,
        transactions.quantity
    FROM transactions
    JOIN products 
    ON transactions.product_id = products.id
    WHERE transactions.type='DELIVERY'
    """

    df = pd.read_sql(query, conn)

    if df.empty:
        st.warning("Not enough sales data for prediction.")
        return

    df["date"] = pd.to_datetime(df["date"])

    st.subheader("Demand Prediction")

    product_name = st.selectbox(
        "Select Product",
        df["name"].unique()
    )

    product_df = df[df["name"] == product_name]

    product_df["day"] = (
        product_df["date"] - product_df["date"].min()
    ).dt.days

    X = product_df[["day"]]
    y = product_df["quantity"]

    model = LinearRegression()
    model.fit(X, y)

    next_day = np.array([[product_df["day"].max() + 1]])

    prediction = model.predict(next_day)

    predicted_demand = int(round(prediction[0]))

    st.metric(
        "Predicted Demand Tomorrow",
        predicted_demand
    )

    show_restock_recommendation()
    show_inventory_health()

    st.info(
        f"AI predicts approximately {predicted_demand} units of {product_name} may be sold tomorrow."
    )

    conn.close()

def show_restock_recommendation():

    st.subheader("AI Restock Recommendation")

    conn = get_connection()

    query = """
    SELECT 
        products.name,
        products.stock,
        SUM(transactions.quantity) as total_sales
    FROM products
    LEFT JOIN transactions
    ON products.id = transactions.product_id
    AND transactions.type = 'DELIVERY'
    GROUP BY products.id
    """

    df = pd.read_sql(query, conn)

    if df.empty:
        st.warning("No data available for recommendation.")
        return

    df["total_sales"] = df["total_sales"].fillna(0)

    # Calculate priority score
    df["priority_score"] = df["total_sales"] / (df["stock"] + 1)

    df = df.sort_values(by="priority_score", ascending=False)

    st.success("AI has analyzed stock and sales to recommend restocking priorities.")

    st.write("Products that should be restocked first:")

    st.dataframe(
        df[["name", "stock", "total_sales", "priority_score"]]
    )

    conn.close()

def show_inventory_health():

    st.subheader("Inventory Health Score")

    conn = get_connection()

    query = "SELECT stock FROM products"

    df = pd.read_sql(query, conn)

    if df.empty:
        st.warning("No inventory data available.")
        return

    total_products = len(df)

    low_stock = len(df[df["stock"] < 10])

    health_score = 100 - (low_stock / total_products * 100)

    health_score = round(health_score)

    st.metric("Inventory Health Score", f"{health_score} / 100")

    if health_score > 80:
        st.success("Inventory is in good condition.")
    elif health_score > 50:
        st.warning("Inventory needs attention.")
    else:
        st.error("Inventory health is poor. Immediate restocking required.")

    st.progress(health_score / 100)

    conn.close()