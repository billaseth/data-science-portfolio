import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Page configuration
st.set_page_config(page_title="Predictive Analytics & Forecasting Dashboard", page_icon="📈", layout="wide")

st.title("📈 Predictive Analytics & Trend Forecasting Dashboard")
st.markdown("Forecast future trends and analyze historical datasets using regression and time-series projections.")

# Sidebar File Uploader
st.sidebar.header("📁 Upload Historical Dataset")
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

@st.cache_data
def get_sample_forecasting_data():
    np.random.seed(42)
    dates = pd.date_range(start="2024-01-01", end="2026-06-30", freq="D")
    base_trend = np.linspace(100, 500, len(dates))
    noise = np.random.normal(0, 30, len(dates))
    seasonality = 50 * np.sin(np.linspace(0, 3 * np.pi, len(dates)))
    values = np.clip(base_trend + noise + seasonality, 10, None)
    
    df_sample = pd.DataFrame({
        "Date": dates,
        "Actual_Value": values.round(2),
        "Region": np.random.choice(["North", "South", "East", "West"], size=len(dates)),
        "Product": np.random.choice(["Laptop", "Smartphone", "Tablet"], size=len(dates))
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
        df = get_sample_forecasting_data()
else:
    df = get_sample_forecasting_data()

# Clean column headers
df.columns = [str(col).strip() for col in df.columns]

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Forecasting Configuration")

columns = list(df.columns)
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

# Smart detection of date and value columns
date_col = next((col for col in columns if any(kw in col.lower() for kw in ["date", "time", "year", "period"])), columns[0])
val_col = next((col for col in numeric_cols if any(kw in col.lower() for kw in ["value", "sales", "revenue", "price", "amount"])), numeric_cols[0] if numeric_cols else columns[0])

selected_date_col = st.sidebar.selectbox("Select Date/Time Column:", options=columns, index=columns.index(date_col) if date_col in columns else 0)
selected_val_col = st.sidebar.selectbox("Select Target Metric Column:", options=numeric_cols if numeric_cols else columns, index=numeric_cols.index(val_col) if val_col in numeric_cols else 0)

forecast_periods = st.sidebar.slider("Forecast Future Steps (Days/Months):", min_value=7, max_value=90, value=30)

# Data Preprocessing & Modeling (Linear Trend Regression & Forecasting)
try:
    df["_Clean_Date_"] = pd.to_datetime(df[selected_date_col], errors='coerce')
    df["_Clean_Val_"] = pd.to_numeric(df[selected_val_col], errors='coerce').fillna(0)
    df = df.dropna(subset=["_Clean_Date_"]).sort_values(by="_Clean_Date_")
    
    # Aggregate by date if multiple entries per date
    ts_df = df.groupby("_Clean_Date_")["_Clean_Val_"].mean().reset_index()
    
    # Simple Linear Regression (Trend Analysis y = mx + c)
    ts_df["Time_Index"] = np.arange(len(ts_df))
    x = ts_df["Time_Index"]
    y = ts_df["_Clean_Val_"]
    
    if len(x) > 1:
        slope, intercept = np.polyfit(x, y, 1)
        r_squared = np.corrcoef(x, y)[0, 1] ** 2
    else:
        slope, intercept, r_squared = 0, y.iloc[0] if len(y)>0 else 0, 0

    # Generate Future Projections
    last_date = ts_df["_Clean_Date_"].max()
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_periods, freq='D')
    future_indices = np.arange(len(ts_df), len(ts_df) + forecast_periods)
    future_preds = slope * future_indices + intercept

    future_df = pd.DataFrame({
        "_Clean_Date_": future_dates,
        "_Clean_Val_": future_preds,
        "Type": "Forecasted (Predicted)"
    })
    
    ts_df["Type"] = "Historical"
    combined_df = pd.concat([ts_df[["_Clean_Date_", "_Clean_Val_", "Type"]], future_df], ignore_index=True)

except Exception as e:
    st.error(f"Preprocessing/Modeling error: {e}")
    st.stop()

# KPI Metrics Section
st.markdown("---")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Historical Data Points", f"{len(ts_df):,}")
c2.metric("Model R² Accuracy Score", f"{r_squared:.2f}" if not np.isnan(r_squared) else "N/A")
c3.metric("Projected Trend Growth", f"{slope:.2f} per unit")
c4.metric("Forecast Horizon", f"{forecast_periods} Steps")

st.markdown("---")

# Visualizations Section
st.subheader("📉 Historical Trends & Future Predictions")
fig_forecast = px.line(combined_df, x="_Clean_Date_", y="_Clean_Val_", color="Type",
                       title=f"Trend Analysis & Forecasting for {selected_val_col}",
                       labels={"_Clean_Date_": "Timeline", "_Clean_Val_": selected_val_col})
fig_forecast.update_traces(mode="lines+markers", selector=dict(name="Forecasted (Predicted)"))
st.plotly_chart(fig_forecast, use_container_width=True)

r1_c1, r1_c2 = st.columns(2)

with r1_c1:
    st.subheader("📊 Historical vs Forecast Summary")
    summary_data = pd.DataFrame({
        "Metric Type": ["Historical Average", "Forecasted Average (Predicted)", "Trend Direction"],
        "Value": [f"{ts_df['_Clean_Val_'].mean():,.2f}", f"{future_df['_Clean_Val_'].mean():,.2f}", "Upward 📈" if slope > 0 else "Downward 📉"]
    })
    st.dataframe(summary_data, use_container_width=True)

with r1_c2:
    st.subheader("📋 Raw Historical Data Preview")
    st.dataframe(df.head(100), use_container_width=True)
