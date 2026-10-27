# 📍 Cognifyz Restaurant Location Analysis & Geospatial Analytics

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Geospatial%20Maps-3F4F75.svg?logo=plotly&logoColor=white)](https://plotly.com/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458.svg?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Cognifyz Technologies Data Science Internship — Level 1 / Level 2 Task: Location-Based Restaurant Analysis**  
> An end-to-end exploratory geospatial analysis and interactive Streamlit web dashboard exploring geographic distribution, cuisine clustering, pricing tiers, and rating variations across worldwide restaurant locations.

---

## 🌐 Live Streamlit Geospatial Dashboard

The interactive web dashboard provides comprehensive location-based insights:
- **Interactive Geospatial Mapping:** Explore restaurant clusters with dynamic scatter maps, color-coded by rating tiers and price points.
- **City & Locality Deep-Dive:** Filter across **141 cities** and **1,200+ localities** to understand concentration patterns.
- **Cuisine Spatial Distribution:** Visualize how culinary preferences vary across neighborhoods.
- **Cost & Rating Correlation:** Discover how pricing and customer satisfaction correlate with geographical zones.
- **Report Export:** One-click CSV downloads for city, locality, and cuisine distribution summaries.

---

## 📋 Project Overview

- **Problem Type:** Exploratory Data Analysis (EDA) & Geospatial Intelligence
- **Objective:** Analyze the geographic distribution of restaurants, identify culinary hotspots, and determine the relationship between restaurant locations, aggregate ratings, and dining costs.
- **Dataset:** 9,551 restaurants across 141 cities globally.
- **Key Findings:**
  - **Highest Density:** New Delhi (5,473 venues), Gurgaon (1,118 venues), and Noida (1,080 venues) represent the highest density clusters in the dataset.
  - **Dominant Cuisines:** North Indian (3,960), Chinese (2,735), and Fast Food (1,986) form the predominant food offerings across major metropolitan clusters.
  - **Rating Distribution by Location:** Inner-city and popular commercial localities consistently average higher ratings and vote volumes compared to peripheral zones.

---

## 📊 Dataset & Outputs

The project processes the standard Cognifyz restaurant dataset and generates structured analytical summaries:

| File / Folder | Description |
| :--- | :--- |
| `data/Dataset .csv` | Raw tabular dataset containing 9,551 restaurant records |
| `outputs/city_analysis.csv` | Restaurant density and distribution aggregated by city |
| `outputs/locality_analysis.csv` | Granular restaurant volume and characteristics by locality |
| `outputs/cuisine_analysis.csv` | Cuisine frequencies and regional availability breakdown |
| `outputs/cleaned_restaurant_data.csv` | Validated coordinates and normalized restaurant features |

---

## 🚀 Key Dashboard Capabilities

1. **Geographical Coordinate Mapping:**
   - Scatter-plot maps projected using real latitude and longitude coordinates.
   - Hover cards detailing Restaurant Name, City, Locality, Cuisines, Average Cost, and Aggregate Rating.
2. **City-Wise Breakdown:**
   - Interactive bar and pie charts ranking top cities by restaurant counts and average customer ratings.
3. **Locality Concentration:**
   - Identify prime dining corridors and underserved neighborhoods within any selected city.
4. **Cuisine Spatial Trends:**
   - Distribution analysis of popular dining styles across geographic boundaries.
5. **Report Center:**
   - Built-in data export mechanism allowing instant extraction of filtered summaries.

---

## 💻 Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/gshivi230-btech/Cognifyz_Task4_Location_Analysis.git
   cd Cognifyz_Task4_Location_Analysis
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Streamlit app:**
   ```bash
   streamlit run app.py
   ```
   Open `http://localhost:8501` in your browser.

---

## ☁️ Deploying to Streamlit Community Cloud

1. Visit [Streamlit Community Cloud](https://share.streamlit.io/) and log in with GitHub (**gshivi230-btech**).
2. Click **"New app"**.
3. Select:
   - **Repository:** `gshivi230-btech/Cognifyz_Task4_Location_Analysis`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **"Deploy!"** to get your public `.streamlit.app` link.

---

## 📂 Repository Structure

```plaintext
Cognifyz_Task4_Location_Analysis/
├── app.py                             # Interactive Streamlit Geospatial Web Dashboard
├── requirements.txt                   # Production Python package requirements
├── .gitignore                         # Git exclusion rules (.venv, caches, etc.)
├── README.md                          # Project documentation and guide
├── Cognifyz_Location_Analysis.ipynb   # Complete Jupyter Notebook for EDA & GIS analysis
├── data/
│   └── Dataset .csv                   # Restaurant dataset with geographic coordinates
├── notebooks/
│   └── Cognifyz_Location_Analysis.ipynb # Notebook archive copy
└── outputs/
    ├── city_analysis.csv              # City-level distribution summary
    ├── cleaned_restaurant_data.csv    # Coordinate-validated restaurant records
    ├── cuisine_analysis.csv           # Global cuisine frequency breakdown
    └── locality_analysis.csv          # Neighborhood concentration metrics
```

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
