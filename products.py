import streamlit as st
import sqlite3
import pandas as pd


def get_connection():
    return sqlite3.connect("inventory.db", check_same_thread=False)


def product_page():
    st.header("Product Management")

    conn = get_connection()
    cursor = conn.cursor()

    tab1, tab2 = st.tabs(["Add Product", "View Products"])

  
    # Add Product

    with tab1:

        st.subheader("Create New Product")

        name = st.text_input("Product Name")
        sku = st.text_input("SKU Code")
        category = st.text_input("Category")
        unit = st.selectbox("Unit of Measure", ["pcs", "kg", "litre", "box"])
        # stock = st.number_input("Initial Stock", min_value=0, step=1)
        stock = st.number_input("Initial Stock", min_value=0, value=0)
        location = st.selectbox(
            "Product Location",
            ["Main Warehouse", "Rack A", "Rack B", "Production Floor"]
        )

        if st.button("Add Product"):

            if name == "" or sku == "":
                st.error("Product name and SKU are required")
            else:
                cursor.execute(
                    """
                    INSERT INTO products (name, sku, category, unit, stock, location)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (name, sku, category, unit, stock, location)
                )
                

                conn.commit()

                st.success("Product added successfully!")


    # View Products

    with tab2:

        st.subheader("Product List")

        df = pd.read_sql("SELECT * FROM products", conn)

        category_filter = st.selectbox(
            "Filter by Category",
            ["All"] + list(df["category"].unique())
        )

    if category_filter != "All":
        products = df[df["category"] == category_filter]

    if df.empty:
         st.info("No products available.")
    else:
         search = st.text_input("🔍 Search Product")
         if search:
             filtered_products = df[df["name"].str.contains(search, case=False)]
             st.dataframe(filtered_products)
         else:
             st.dataframe(df)

    conn.close()