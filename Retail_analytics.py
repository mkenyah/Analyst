import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns


# 1. Fetching from excel
file_path = r"C:\Users\Joseph kirika\Desktop\retail_sales.csv.xlsx"
df = pd.read_excel(file_path, parse_dates=["Date"])

# 2. Feature Engineering
df["Revenue"] = df["Quantity"] * df["Price"]
df["Profit"] = df["Revenue"] - df["Cost"] # Note: 'Profit' capitalized here for consistency

# IMPORTANT FIX: Convert Period to String for SQLite compatibility
df["Month"] = df["Date"].dt.to_period("M").astype(str)



# 3. Engaging SQLite3
conn = sqlite3.connect("retail_analytics.db")

# FIX: Insert into the correct table name: "sales_records"
# Using if_exists="replace" handles table creation automatically
df.to_sql("sales_records", conn, if_exists="replace", index=False)
print("Data inserted into 'sales_records' table successfully.")


# 4. Fetching data from DB for analysis
query = """
SELECT Month, SUM(Revenue) AS Monthly_Revenue
FROM sales_records  -- FIX: Corrected table name
GROUP BY Month
ORDER BY Month
"""
monthly_df = pd.read_sql(query, conn)


# 5. Plot Monthly Revenue Trend
plt.figure(figsize=(10, 6))
plt.plot(monthly_df["Month"], monthly_df["Monthly_Revenue"], marker="o", label="Monthly Revenue")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (Ksh)")
plt.legend()
plt.grid(True)
plt.show()


# 6. Plot Profit by Product (using the original 'df' DataFrame)
plt.figure(figsize=(10, 6))
# FIX: Added 'data=df' parameter and using 'Profit' column created earlier
# sns.barplot(x="Product", y="Profit", data=df, estimator="sum") 
plt.title("Total Profit by Product Category")
plt.xlabel("Product")
plt.ylabel("Total Profit (Ksh)")
plt.show()
conn.close()
