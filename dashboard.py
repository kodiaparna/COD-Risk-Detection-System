import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="COD Risk Detection",
    page_icon="📦",
    layout="wide"
)

st.title("COD Order Risk Detection Dashboard")

# Load dataset
df = pd.read_csv("orders_sample (1).csv")

# Clean status
df["final_status"] = (
    df["final_status"].astype(str).str.strip().str.upper()
)
# Convert order date
df["order_datetime"] = pd.to_datetime(df["order_datetime"], errors="coerce")

# Check available date range
st.write("Dataset start date:", df["order_datetime"].min())
st.write("Dataset end date:", df["order_datetime"].max())
# Get latest available date
reporting_date = df["order_datetime"].max().date()

# Filter orders for that date
daily_df = df[
    df["order_datetime"].dt.date == reporting_date
]

st.subheader(f"Daily Report: {reporting_date}")

# Calculate daily statistics
total_orders = len(daily_df)

delivered = (daily_df["final_status"] == "DELIVERED").sum()

rto = (daily_df["final_status"] == "RTO").sum()

completed = delivered + rto

rto_rate = (rto / completed * 100) if completed else 0

# Display metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Orders", total_orders)
col2.metric("Delivered", delivered)
col3.metric("RTO Orders", rto)
col4.metric("RTO Rate", f"{rto_rate:.2f}%")

# Display order status
st.subheader("Order Status Analysis")

status_data = pd.DataFrame({
    "Status": ["Delivered", "RTO"],
    "Orders": [delivered, rto]
})

st.bar_chart(status_data.set_index("Status"))

# Display dataset
st.subheader("Order Details")

st.dataframe(daily_df, width="stretch")
# FINANCIAL IMPACT ANALYSIS

st.subheader("Financial Impact Analysis")

avg_order_value = df["order_value"].mean()

st.metric(
    "Average Order Value",
    f"₹{avg_order_value:,.2f}"
)

st.metric(
    "Total COD Order Value",
    f"₹{df['order_value'].sum():,.2f}"
)

st.write(
    "Financial savings and losses will be calculated "
    "after applying the decision engine and business assumptions."
)
# ESTIMATED RTO SAVINGS

st.subheader("Estimated RTO Savings")

# Business assumptions
rto_prevention_rate = 0.20
rto_handling_cost = 100
genuine_order_rate = 0.20

# Calculate expected prevented RTOs
prevented_rtos = rto * rto_prevention_rate

# Calculate estimated savings
estimated_savings = prevented_rtos * rto_handling_cost

st.metric(
    "Expected Prevented RTOs",
    f"{prevented_rtos:.2f}"
)

st.metric(
    "Estimated RTO Cost Savings",
    f"₹{estimated_savings:,.2f}"
)

# Cancellation loss analysis
st.subheader("Cancellation Loss Analysis")

genuine_orders_cancelled = (
    prevented_rtos * genuine_order_rate
)

cancellation_loss = (
    genuine_orders_cancelled * avg_order_value
)

net_impact = estimated_savings - cancellation_loss

st.metric(
    "Expected Genuine Orders Cancelled",
    f"{genuine_orders_cancelled:.2f}"
)

st.metric(
    "Estimated Cancellation Revenue Loss",
    f"₹{cancellation_loss:,.2f}"
)

st.metric(
    "Net Estimated Financial Impact",
    f"₹{net_impact:,.2f}"
)

st.caption(
    "Assumptions: 20% of historical RTOs are prevented, "
    "RTO handling cost is ₹100, and 20% of prevented RTOs "
    "are genuine orders. These are illustrative estimates, "
    "not verified savings. Cancellation loss represents "
    "gross revenue at risk, not profit."
)