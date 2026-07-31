# 📈 Predictive Analytics & Trend Forecasting Dashboard

An advanced, interactive web-based data forecasting and trend analysis application built with **Python**, **Streamlit**, and **Plotly**. This tool allows users to upload historical datasets, automatically preprocess time-series data, run regression-based trend models, and forecast future projections with accuracy metrics.

---

## 🚀 Key Features

* **Universal Dataset Upload:** Supports uploading custom historical CSV and Excel files (`.csv`, `.xlsx`).
* **Smart Column Mapping:** Automatically detects and parses date/time columns and target numeric metrics.
* **Predictive Modeling & Regression:** Utilizes linear regression and time-series trend analysis to evaluate historical performance.
* **Accuracy Evaluation:** Computes and displays statistical metrics including the **Model R² Accuracy Score**.
* **Future Trend Forecasting:** Generates custom-horizon future projections (adjustable step sliders from 7 to 90 days/periods).
* **Interactive Visualizations:** Dynamic line charts contrasting actual historical data with forecasted future trends.
* **Summary & KPIs:** Instant performance metrics tracking historical averages, predicted averages, and directional growth trends.

---

## 🛠️ Tech Stack

* **Frontend & UI:** [Streamlit](https://streamlit.io/)
* **Data Processing & Math:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
* **Visualizations:** [Plotly Express](https://plotly.com/python/plotly-express/)

---

## ⚙️ Installation & Local Setup

To run this dashboard locally on your machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/billaseth/sales-dashboard.git](https://github.com/billaseth/sales-dashboard.git)
   cd sales-dashboard
