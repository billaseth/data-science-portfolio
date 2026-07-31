import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import io

# Page configuration
st.set_page_config(page_title="Data Cleaning & Reporting Automation", page_icon="🧹", layout="wide")

st.title("🧹 Automated Data Cleaning & Reporting Dashboard")
st.markdown("Automate data preprocessing, handle missing values and duplicates, and generate clean visual reports instantly.")

# Sidebar File Uploader
st.sidebar.header("📁 Upload Raw Dataset")
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

@st.cache_data
def get_sample_messy_data():
    np.random.seed(42)
    n = 200
    df_sample = pd.DataFrame({
        "CustomerID": [f"CUST_{np.random.randint(100, 999)}" for _ in range(n)],
        "CustomerName": np.random.choice(["  john doe  ", "alice smith", "BOB JONES", "john doe", None], size=n),
        "Region": np.random.choice(["North", "South", "East", "West", "North ", "  East"], size=n),
        "Sales": [np.nan if i % 10 == 0 else np.random.randint(100, 5000) for i in range(n)],
        "Date": pd.date_range(start="2026-01-01", periods=n, freq="D")
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
        st.sidebar.success("Raw file uploaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Error reading file: {e}")
        df = get_sample_messy_data()
else:
    df = get_sample_messy_data()

# Capture initial dirty dataset metrics
initial_rows = len(df)
initial_duplicates = df.duplicated().sum()
initial_missing = df.isnull().sum().sum()

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Automation Cleaning Rules")

remove_dups = st.sidebar.checkbox("Remove Duplicate Rows", value=True)
handle_missing = st.sidebar.checkbox("Handle Missing Values (Drop / Fill)", value=True)
clean_text_cols = st.sidebar.checkbox("Standardize Text (Trim Spaces & Case)", value=True)

# Automated Data Cleaning Pipeline
cleaned_df = df.copy()

if remove_dups:
    cleaned_df = cleaned_df.drop_duplicates()

if handle_missing:
    # Fill numeric columns with median, text with 'Unknown'
    for col in cleaned_df.columns:
        if cleaned_df[col].dtype in [np.float64, np.int64]:
            cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].median())
        else:
            cleaned_df[col] = cleaned_df[col].fillna("Unknown")

if clean_text_cols:
    for col in cleaned_df.select_dtypes(include=[object]).columns:
        cleaned_df[col] = cleaned_df[col].astype(str).str.strip().str.title()

# Post-cleaning metrics
final_rows = len(cleaned_df)
final_missing = cleaned_df.isnull().sum().sum()

# KPI Metrics Section
st.markdown("---")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows Cleaned", f"{final_rows:,}", delta=f"{final_rows - initial_rows} rows")
c2.metric("Duplicates Removed", f"{initial_duplicates}")
c3.metric("Missing Values Resolved", f"{initial_missing} -> {final_missing}")
c4.metric("Automation Status", "Active 🟢")

st.markdown("---")

# Visualizations & Automated Reporting Section
st.subheader("📊 Automated Visual Summary & Reports")

numeric_cols = cleaned_df.select_dtypes(include=[np.number]).columns.tolist()
text_cols = cleaned_df.select_dtypes(exclude=[np.number]).columns.tolist()

if numeric_cols and text_cols:
    r1_c1, r1_c2 = st.columns(2)
    
    with r1_c1:
        group_col = st.selectbox("Select Dimension for Report:", options=text_cols, key="rep_dim")
        metric_col = st.selectbox("Select Metric for Report:", options=numeric_cols, key="rep_met")
        
        rep_data = cleaned_df.groupby(group_col)[metric_col].sum().reset_index()
        fig_bar = px.bar(rep_data, x=group_col, y=metric_col, color=group_col, title=f"Automated Report: {metric_col} by {group_col}")
        st.plotly_chart(fig_bar, use_container_width=True)

    with r1_c2:
        fig_box = px.box(cleaned_df, y=metric_col, title=f"Distribution & Outlier Analysis for {metric_col}")
        st.plotly_chart(fig_box, use_container_width=True)
else:
    st.info("Dataset requires both numeric and text columns for automated grouping reports.")

st.markdown("---")
st.subheader("📋 Cleaned Data Preview & Export Report")

# Dataframe comparison view
tab1, tab2 = st.tabs(["Cleaned Data Output", "Original Raw Data"])
with tab1:
    st.dataframe(cleaned_df.head(200), use_container_width=True)
    
    # Download automated clean report button
    csv_buffer = io.BytesIO()
    cleaned_df.to_csv(index=False, path_or_buf=csv_buffer)
    st.download_button(
        label="📥 Download Cleaned Report (CSV)",
        data=csv_buffer.getvalue(),
        file_name="automated_cleaned_report.csv",
        mime="text/csv"
    )

with tab2:
    st.dataframe(df.head(200), use_container_width=True)
