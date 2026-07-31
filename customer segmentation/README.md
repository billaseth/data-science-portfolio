# 👥 Customer Segmentation & Analytics Dashboard

An interactive, web-based data analytics and customer segmentation dashboard built with **Python**, **Streamlit**, and **Plotly**. This application allows users to upload any custom sales or customer dataset and automatically analyzes behavioral patterns, performs automated customer tiering, and generates insightful visualizations.

---

## 🚀 Features

* **Universal File Upload:** Supports uploading any CSV or Excel file (`.csv`, `.xlsx`).
* **Smart Column Mapping:** Automatically detects and maps numeric, categorical, and grouping columns.
* **Behavioral Customer Segmentation:** Automatically classifies customers/records into behavior tiers (*Bronze / Budget*, *Silver / Regular*, *Gold / High-Value*) based on spending metrics.
* **Interactive Visualizations:**
  * Customer distribution across different behavioral segments (Bar Charts).
  * Feature correlation and comparative analysis (Scatter Plots).
* **Key Performance Indicators (KPIs):** Real-time metrics tracking total records, averages, and volume.
* **Raw Data Preview:** Filtered and searchable data table view.

---

## 🛠️ Tech Stack

* **Frontend & UI:** [Streamlit](https://streamlit.io/)
* **Data Processing:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
* **Visualizations:** [Plotly Express](https://plotly.com/python/plotly-express/)

---

## ⚙️ Installation & Local Setup

To run this dashboard locally on your machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/billaseth/sales-dashboard.git](https://github.com/billaseth/sales-dashboard.git)
   cd sales-dashboard
