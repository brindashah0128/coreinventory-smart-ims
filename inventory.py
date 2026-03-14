import streamlit as st
import sqlite3
import pandas as pd


def get_connection():
    return sqlite3.connect("inventory.db", check_same_thread=False)


def inventory_page():
    st.header("Inventory Operations")

    conn = get_connection()
    cursor = conn.cursor()

    # Load products
    products = pd.read_sql("SELECT * FROM products", conn)

    if products.empty:
        st.warning("No products available. Please add products first.")
        return

    product_dict = dict(zip(products["name"], products["id"]))

    # tab1, tab2 = st.tabs(["Receipts (Incoming)", "Delivery Orders (Outgoing)"])
    # tab1, tab2, tab3 = st.tabs(["Receipts", "Delivery Orders", "Internal Transfers"])
    tab1, tab2, tab3, tab4 = st.tabs(["Receipts", "Delivery Orders", "Internal Transfers", "Stock Adjustment"])


    # RECEIPTS

    with tab1:

        st.subheader("Receive Stock from Vendor")

        product_name = st.selectbox(
            "Select Product",
            products["name"]
        )

        quantity = st.number_input(
            "Quantity Received",
            min_value=1,
            step=1
        )

        if st.button("Receive Stock"):

            product_id = product_dict[product_name]

            cursor.execute(
                "SELECT stock FROM products WHERE id=?",
                (product_id,)
            )

            current_stock = cursor.fetchone()[0]
            new_stock = current_stock + quantity

            # Update stock
            cursor.execute(
                "UPDATE products SET stock=? WHERE id=?",
                (new_stock, product_id)
            )

            # Record transaction
            cursor.execute(
                """
                INSERT INTO transactions (product_id, type, quantity)
                VALUES (?, 'RECEIPT', ?)
                """,
                (product_id, quantity)
            )

            conn.commit()

            st.success(f"{quantity} units added to {product_name}")

  
    # DELIVERY

    with tab2:

        st.subheader("Deliver Goods to Customer")

        product_name = st.selectbox(
            "Select Product for Delivery",
            products["name"],
            key="delivery_product"
        )

        quantity = st.number_input(
            "Quantity to Deliver",
            min_value=1,
            step=1,
            key="delivery_qty"
        )

        if st.button("Deliver Product"):

            product_id = product_dict[product_name]

            cursor.execute(
                "SELECT stock FROM products WHERE id=?",
                (product_id,)
            )

            current_stock = cursor.fetchone()[0]

            if quantity > current_stock:
                st.error("Not enough stock available!")

            else:
                new_stock = current_stock - quantity

                cursor.execute(
                    "UPDATE products SET stock=? WHERE id=?",
                    (new_stock, product_id)
                )

                cursor.execute(
                    """
                    INSERT INTO transactions (product_id, type, quantity)
                    VALUES (?, 'DELIVERY', ?)
                    """,
                    (product_id, quantity)
                )

                conn.commit()

                st.success(f"{quantity} units delivered from {product_name}")

    with tab3:

        st.subheader("Internal Transfer")

        product_name = st.selectbox(
            "Select Product",
            products["name"],
            key="transfer_product"
        )

        transfer_qty = st.number_input(
            "Quantity to Transfer",
            min_value=1,
            step=1
        )

        new_location = st.selectbox(
            "Move To Location",
            ["Main Warehouse", "Rack A", "Rack B", "Production Floor"]
        )

        product_id = product_dict[product_name]

        cursor.execute(
            "SELECT stock FROM products WHERE id=?",
            (product_id,)
        )

        current_stock = cursor.fetchone()[0]

        st.info(f"Current Stock Available: {current_stock}")

        if st.button("Transfer Product"):

            if transfer_qty > current_stock:

                st.error("Not enough stock for transfer!")

            else:

                remaining_stock = current_stock - transfer_qty

                cursor.execute(
                    "UPDATE products SET stock=?, location=? WHERE id=?",
                    (remaining_stock, new_location, product_id)
                )

                cursor.execute(
                    """
                    INSERT INTO transactions (product_id, type, quantity)
                    VALUES (?, 'TRANSFER', ?)
                    """,
                    (product_id, transfer_qty)
                )

                conn.commit()

                st.success(f"{transfer_qty} units of {product_name} moved to {new_location}")

        # if st.button("Transfer Product"):

        #     product_id = product_dict[product_name]

        #     cursor.execute(
        #     "UPDATE products SET location=? WHERE id=?",
        #     (new_location, product_id)
        #     )

        #     cursor.execute(
        #     """
        #     INSERT INTO transactions (product_id, type, location)
        #     VALUES (?, 'TRANSFER', ?)
        #     """,
        #     (product_id)
        #     )

        #     conn.commit()

        #     st.success(f"{product_name} moved to {new_location}")

    with tab4:

        st.subheader("Inventory Adjustment")

        product_name = st.selectbox(
            "Select Product",
            products["name"],
            key="adjust_product"
        )

        new_quantity = st.number_input(
            "Actual Stock Count",
            min_value=0,
            step=1
        )

        if st.button("Adjust Inventory"):

            product_id = product_dict[product_name]

            cursor.execute(
            "UPDATE products SET stock=? WHERE id=?",
            (new_quantity, product_id)
            )

            cursor.execute(
            """
            INSERT INTO transactions (product_id, type, quantity)
            VALUES (?, 'ADJUSTMENT', ?)
            """,
            (product_id, new_quantity)
            )

            conn.commit()

            st.success("Stock updated successfully")
    conn.close()
    st.divider()
    show_stock_ledger()

def show_stock_ledger():

    st.subheader("Stock Movement History")

    conn = get_connection()

    query = """
    SELECT 
        transactions.id,
        products.name,
        transactions.type,
        transactions.quantity,
        transactions.date
    FROM transactions
    JOIN products ON transactions.product_id = products.id
    ORDER BY transactions.date DESC
    """

    df = pd.read_sql(query, conn)

    if df.empty:
        st.info("No inventory transactions yet.")
    else:
        st.dataframe(df)

    conn.close()