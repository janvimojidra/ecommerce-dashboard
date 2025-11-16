import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

# Load data
data = pd.read_excel("sales_data.xlsx")
data['Date'] = pd.to_datetime(data['Date'])

# KPIs
total_sales = data['Amount'].sum()
total_customers = data['CustomerID'].nunique()
total_products = data['ProductID'].nunique()
avg_sales_per_customer = total_sales / total_customers

# Display KPIs
st.title("E-commerce Dashboard")
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Customers", total_customers)
col3.metric("Total Products", total_products)
col4.metric("Avg Sales/Customer", f"${avg_sales_per_customer:,.2f}")

# Sales Trend
st.subheader("Sales Trend Over Time")
sales_trend = data.groupby('Date')['Amount'].sum()
fig1 = go.Figure()
fig1.add_trace(go.Scatter(
    x=sales_trend.index, y=sales_trend.values,
    mode='lines+markers', name='Sales Trend', line=dict(color='green')
))
st.plotly_chart(fig1, use_container_width=True)

# Sales by Category
st.subheader("Sales by Product Category")
category_sales = data.groupby('Category')['Amount'].sum().reset_index()
fig2 = px.pie(category_sales, names='Category', values='Amount', hole=0.4)
st.plotly_chart(fig2, use_container_width=True)

# Top 10 Customers
st.subheader("Top 10 Customers")
top_customers = data.groupby('CustomerID')['Amount'].sum().sort_values(ascending=False).head(10)
fig3, ax = plt.subplots(figsize=(10,5))
top_customers.plot(kind='bar', color='skyblue', ax=ax)
plt.title("Top 10 Customers")
plt.ylabel("Total Purchase Amount")
plt.xlabel("Customer ID")
plt.xticks(rotation=0)
st.pyplot(fig3)

# Key Insights
st.subheader("Key Insights")
st.markdown("""
- Highest sales categories are shown in the donut chart.
- Top 10 customers contribute most to revenue.
- Overall sales trend indicates growth or seasonality.
""")
