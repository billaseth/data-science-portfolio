import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Page configuration
st.set_page_config(page_title="Customer Segmentation Dashboard", page_icon="👥", layout="wide")

st.title("👥 Customer Segmentation & Analytics Dashboard")
st.markdown("Segment customers based on behavior and demographics without external ML dependencies.")

# Sidebar File Uploader
st.sidebar.header("📁 Upload Customer Dataset")
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

@st.cache_data
def get_sample_customer_data():
    np.random.seed(42)
    n_customers = 300
    df_sample = pd.DataFrame({
        "CustomerID": [f"CUST_{i:03d}" for i in range(1, n_customers + 1)],
        "Age": np.random.randint(18, 65, size=n_customers),
        "Annual_Spend": np.random.uniform(500, 20000, size=n_customers).round(2),
        "Purchase_Frequency": np.random.randint(1, 25, size=n_customers),
        "Satisfaction_Score": np.random.randint(1, 10, size=n_customers)
    })
    return df_sample

# Load data safely
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            xls = pd.ExcelFile(uploaded_file)
            df = pd.read_excel(uploaded_file, sheet_name=xls.sheet_names[0])
        st.sidebar.success("File uploaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Error reading file: {e}")
        df = get_sample_customer_data()
else:
    df = get_sample_customer_data()

# Clean column headers
df.columns = [str(col).strip() for col in df.columns]

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Segmentation Configuration")

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
spend_col = st.sidebar.selectbox("Select Spending/Value Column:", options=numeric_cols, index=1 if len(numeric_cols)>1 else 0)

# Smart Rule-Based Segmentation (No sklearn required, 100% stable)
try:
    # Divide customers into 3 behavioral tiers based on the selected spending column
    df["Spend_Rank"] = pd.qcut(df[spend_col].rank(method="first"), q=3, labels=["Bronze / Budget", "Silver / Regular", "Gold / High-Value"])
    df["Segment"] = df["Spend_Rank"]
except Exception:
    df["Segment"] = "Standard Segment"

# KPI Metrics Section
st.markdown("---")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Customers", f"{len(df):,}")
c2.metric("Total Segments", "3 Tiers")
c3.metric("Primary Metric", f"{spend_col}")
c4.metric("Status", "Active & Stable")

st.markdown("---")

# Visualizations Section
r1_c1, r1_c2 = st.columns(2)

with r1_c1:
    st.subheader("📊 Customer Distribution across Segments")
    seg_counts = df["Segment"].value_counts().reset_index()
    seg_counts.columns = ["Segment", "Count"]
    fig_bar = px.bar(seg_counts, x="Segment", y="Count", color="Segment", title="Number of Customers per Segment")
    st.plotly_chart(fig_bar, use_container_width=True)

with r1_c2:
    st.subheader("🔍 Spend vs Record Distribution")
    if len(numeric_cols) >= 2:
        fig_scatter = px.scatter(df, x=numeric_cols[0], y=spend_col, color="Segment", 
                                 title=f"{numeric_cols[0]} vs {spend_col} by Segment", hover_data=df.columns)
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("Insufficient numeric columns for scatter plot.")

st.markdown("---")
st.subheader("📋 Segmented Customer Data Preview")
st.dataframe(df.head(200), use_container_width=True)
