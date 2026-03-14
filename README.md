# 📦 CoreInventory Smart IMS

CoreInventory Smart IMS is a Smart Inventory Management System designed to help businesses manage and monitor their inventory efficiently. The system allows users to track product stock, perform inventory operations, analyze inventory data, and generate AI-driven insights for better decision making.

Live Web Application  
https://coreinventory-smart-ims.streamlit.app/

---

## Problem Statement

Many small and medium businesses still manage inventory using manual records or spreadsheets. This approach often leads to several issues such as inaccurate stock tracking, delayed restocking decisions, lack of visibility into stock movement, and inefficient warehouse operations.

Without a proper inventory management system, businesses may face problems like stock shortages, overstocking, and difficulty analyzing inventory data.

---

## Proposed Solution

CoreInventory Smart IMS provides a digital platform to manage inventory operations efficiently. The system enables businesses to track product stock in real time, manage product movements, and generate data-driven insights using analytics and AI-based predictions.

This helps businesses maintain optimal inventory levels and improve overall warehouse efficiency.

---

## Features

### Product Management
- Add and manage products
- Store product category, price, and stock details

### Inventory Operations
- Receive stock from suppliers
- Deliver products to customers
- Transfer products between storage locations
- Adjust stock quantities when required

### Inventory Analytics
- Visualize product distribution by category
- Monitor stock levels using charts and graphs

### AI Insights
- Predict product demand using historical sales data
- Generate restock recommendations
- Calculate inventory health score

---

## Technologies Used

- Python
- Streamlit
- SQLite
- Pandas
- Matplotlib
- Scikit-learn

---

## System Architecture

The system consists of the following modules:

- Dashboard
- Product Management
- Inventory Operations
- Analytics
- AI Insights

All data is stored in a SQLite database and processed using Python libraries for analysis and machine learning.

---

## System Workflow

```mermaid
flowchart TD

A[User Login] --> B[Dashboard]

B --> C[Product Management]
C --> D[Add / Manage Products]

B --> E[Inventory Operations]

E --> F[Receive Stock]
E --> G[Deliver Products]
E --> H[Internal Transfer]
E --> I[Stock Adjustment]

F --> J[Update Inventory Database]
G --> J
H --> J
I --> J

J --> K[Analytics Dashboard]

K --> L[AI Insights]

L --> M[Demand Prediction]
L --> N[Restock Recommendation]
L --> O[Inventory Health Score]


---

## Installation and Setup

### 1 Clone the repository

```bash
git remote add origin https://github.com/brindashah0128/coreinventory-smart-ims.git
