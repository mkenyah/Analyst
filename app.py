import streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect("retail_analytics.db")
df = pd.read_sql("SELECT * FROM retail_sales", conn)





# Ensure numeric types
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0)
df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0)
df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce').fillna(0)

# Create calculated columns
df['Revenue'] = df['Quantity'] * df['Price']
df['Profit'] = (df['Price'] - df['Cost']) * df['Quantity']

# KPIs
col1, col2, col3 = st.columns(3)

total_revenue = df['Revenue'].sum()
total_profit = df['Profit'].sum()
profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0

col1.metric("Total Revenue", f"Ksh {total_revenue:,.0f}")
col2.metric("Total Profit", f"Ksh {total_profit:,.0f}")
col3.metric("Profit Margin", f"{profit_margin:.2f}%")

# Charts
st.subheader("Revenue by Product")
st.bar_chart(df.groupby("Product")["Revenue"].sum())

st.subheader("Profit by Category")
st.bar_chart(df.groupby("Category")["Profit"].sum())

df.to_excel("Retail_Analytics_Report.xlsx", index=False)

