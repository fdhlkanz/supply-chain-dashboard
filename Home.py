import streamlit as st
import plotly.express as px
from query import load_and_process_data
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# ================= CONFIG =================
st.set_page_config(
    page_title="Supply Chain & Logistics Dashboard",
    layout="wide"
)

# ================= LOAD DATA =================
df = load_and_process_data()

# ================= TITLE =================
st.title("📦 Supply Chain & Logistics Dashboard")

# ================= KPI =================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Avg Logistics Cost", f"{df['costs'].mean():,.0f}")
col2.metric("Avg Total Lead Time", f"{df['total_lead_time'].mean():,.1f}")
col3.metric("Avg Defect Rate", f"{df['defect_rates'].mean():.2f}")
col4.metric("Avg Estimated Profit", f"{df['estimated_profit'].mean():,.0f}")

# ================= EDA =================
st.subheader("Exploratory Data Analysis")

col5, col6 = st.columns(2)

with col5:
    fig_hist = px.histogram(
        df,
        x="costs",
        title="Distribusi Biaya Logistik"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col6:
    fig_scatter = px.scatter(
        df,
        x="total_lead_time",
        y="costs",
        title="Total Lead Time vs Costs"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ================= CLUSTERING =================
st.subheader("K-Means Clustering Analysis")

features = df[["costs", "total_lead_time", "defect_rates"]]
scaled = StandardScaler().fit_transform(features)

kmeans = KMeans(n_clusters=3, random_state=42)
df["cluster"] = kmeans.fit_predict(scaled)

fig_cluster = px.scatter(
    df,
    x="total_lead_time",
    y="costs",
    color="cluster",
    title="Clustering Supply Chain Performance"
)
st.plotly_chart(fig_cluster, use_container_width=True)

# ================= TIME SERIES =================
st.subheader("Time Series Analysis of Logistics Costs")

fig_ts = px.line(
    df,
    x="time_index",
    y="costs",
    title="Trend of Logistics Costs Over Time"
)
st.plotly_chart(fig_ts, use_container_width=True)

# ================= DATA TABLE =================
st.subheader("Processed Supply Chain Data")
st.dataframe(df.head(20))
