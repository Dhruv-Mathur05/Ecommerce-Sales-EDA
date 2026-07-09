import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(layout = 'wide')
st.title("Amazon Sales Dashboard")
st.caption("Interactive dashboard for sales, customers and revenue insights")

#Load data
df = pd.read_csv("data/amazon_sales_2025_INR.csv")

#Total_revenue
#1. Filters
st.sidebar.header('Filters')
state = st.sidebar.selectbox("Select State", ['All'] +  list(df['State'].unique()))
if state != 'All':
    df = df[df['State'] == state]
    
#2. KPI
total_revenue = df['Total_Sales_INR'].sum()
total_orders = df['Order_ID'].nunique()
avg_order_value = df['Total_Sales_INR'].mean()
total_customers = df['Customer_ID'].nunique()

st.metric("Total Revenue", f"Rs{total_revenue:,.0f}")
st.metric("Total Orders", total_orders)
st.metric("Avg Order Value", f"Rs{avg_order_value:,.2f}")
st.metric("Total Customers", total_customers)

#3. Charts
df['Date'] = pd.to_datetime(df['Date'], errors = 'coerce')
monthly = df.groupby(df['Date'].dt.to_period('M'))['Total_Sales_INR'].sum()
monthly.index = monthly.index.to_timestamp()
st.subheader('Monthly Revenue Trend')
st.line_chart(monthly)

col1, col2 = st.columns(2)
with col1:
    st.subheader('Top 10 Products by Revenue') 
    st.bar_chart(df.groupby('Product_Name')['Total_Sales_INR'].sum().nlargest(10))

with col2:
    st.subheader('Top 10 Products by Quantity Sold')
    st.bar_chart(df.groupby('Product_Name')['Quantity'].sum().nlargest(10))

payment_counts = df['Payment_Method'].value_counts().reset_index()
payment_counts.columns = ['Payment_Method', 'count']
fig = px.pie(payment_counts,
             names = 'Payment_Method',
             values = 'count',
             hole = 0.45,
             title = 'Payment Method Dsitribution').update_traces(textinfo = 'percent+label').update_layout(title_x = 0.5)
st.plotly_chart(fig, use_container_width = True)

col3, col4 = st.columns(2)
with col3:
    st.subheader('Total Revenue by Category')
    st.bar_chart(df.groupby('Product_Category')['Total_Sales_INR'].sum())

with col4:
    st.subheader('Top 5 customers')
    st.bar_chart(df.groupby('Customer_ID')['Total_Sales_INR'].sum().nlargest(5))

st.subheader('Total Orders by State')
st.bar_chart(df['State'].value_counts())

st.markdown('---')
st.caption("Dashboard created by Dhruv Mathur | Data Analysis Project")