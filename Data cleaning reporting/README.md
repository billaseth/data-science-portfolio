# 🧹 Data Cleaning & Reporting Automation Dashboard

An automated data preprocessing and reporting application built with **Python**, **Streamlit**, and **Plotly**. This tool cleans raw, inconsistent datasets by handling missing values, removing duplicates, standardizing text formatting, and generating automated visual reports with one-click export capabilities.

---

## 🚀 Key Features

* **Automated Data Cleaning Pipeline:** Automatically detects and resolves missing values, eliminates duplicate rows, and strips unwanted whitespaces.
* **Text Standardization:** Converts inconsistent text cases and formats across categorical dimensions.
* **Automated Reporting & Visual Summaries:** Generates dynamic bar charts and outlier distribution box plots based on active dimensions.
* **One-Click Export:** Download cleaned datasets instantly as standardized CSV reports.
* **Before & After Comparison Tabs:** Easily toggle between raw input data and processed output tables.

---

## 🛠️ Tech Stack

* **Frontend & UI:** [Streamlit](https://streamlit.io/)
* **Data Manipulation:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
* **Visualizations:** [Plotly Express](https://plotly.com/python/plotly-express/)

---

## ⚙️ Installation & Local Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/billaseth/sales-dashboard.git](https://github.com/billaseth/sales-dashboard.git)
   cd sales-dashboard


pip install -r requirements.txt
streamlit run app.py
