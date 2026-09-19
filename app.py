import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Business Intelligence Dashboard", page_icon="📊", layout="wide")

df = pd.read_csv("interactive_dashboard_dataset.csv")
df["Date"] = pd.to_datetime(df["Date"])

st.title("📊 Interactive Business Intelligence Dashboard")
st.caption("Illustrative dataset — demonstration dashboard")

st.sidebar.header("Dashboard Filters")

date_range = st.sidebar.date_input(
    "Date Range",
    [df["Date"].min().date(), df["Date"].max().date()],
    min_value=df["Date"].min().date(),
    max_value=df["Date"].max().date()
)

region_filter = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

category_filter = st.sidebar.multiselect(
    "Category",
    sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

filtered = df[
    (df["Date"].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[-1]))) &
    (df["Region"].isin(region_filter)) &
    (df["Category"].isin(category_filter))
]

total_revenue = filtered["Revenue"].sum()
total_users = filtered["Users"].sum()
total_churned = filtered["ChurnedUsers"].sum()
churn_rate = total_churned / total_users * 100 if total_users else 0
total_tickets = filtered["Tickets"].sum()
avg_ticket = total_revenue / total_tickets if total_tickets else 0
active_users = total_users - total_churned

c1,c2,c3,c4=st.columns(4)
c1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
c2.metric("Active Users", f"{active_users:,}")
c3.metric("Churn %", f"{churn_rate:.2f}%")
c4.metric("Avg Ticket Size", f"₹{avg_ticket:,.0f}")

st.divider()

region_data=filtered.groupby("Region",as_index=False).agg(Revenue=("Revenue","sum"),Users=("Users","sum"))
st.plotly_chart(px.bar(region_data,x="Region",y="Revenue",title="Revenue by Region"),use_container_width=True)

category_data=filtered.groupby("Category",as_index=False).agg(Revenue=("Revenue","sum"),Users=("Users","sum"))
st.plotly_chart(px.bar(category_data,x="Category",y="Revenue",title="Revenue by Category"),use_container_width=True)

trend=filtered.groupby("Date",as_index=False).agg(Revenue=("Revenue","sum"))
st.plotly_chart(px.line(trend,x="Date",y="Revenue",markers=True,title="Revenue Trend"),use_container_width=True)

churn_data=filtered.groupby("Region",as_index=False).agg(Users=("Users","sum"),Churned=("ChurnedUsers","sum"))
churn_data["ChurnRate"]=churn_data["Churned"]/churn_data["Users"]*100
st.plotly_chart(px.bar(churn_data,x="Region",y="ChurnRate",title="Churn Rate by Region"),use_container_width=True)

st.subheader("Filtered Data")
st.dataframe(filtered,use_container_width=True)
