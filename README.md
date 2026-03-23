# 🇳🇬 Nigeria Inflation and Economic Tracker

> Real-time tracking of Nigeria's key economic indicators powered by Machine Learning

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://nigeria-economic-tracker-k7vgyghegdwxjhtbfzarkf.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Overview

The **Nigeria Inflation and Economic Tracker** is a machine learning-powered web dashboard that provides real-time visibility into Nigeria's most critical economic indicators. Built for analysts, businesses, fintech companies, and everyday Nigerians who need to understand the economic forces shaping their financial decisions.

With Nigeria's inflation hitting 33%+ and the Naira experiencing historic volatility, this tool brings data-driven clarity to one of Africa's most dynamic economies.

---

## 🌐 Live Demo

🔗 **[nigeria-economic-tracker-k7vgyghegdwxjhtbfzarkf.streamlit.app](https://nigeria-economic-tracker-k7vgyghegdwxjhtbfzarkf.streamlit.app)**

---

## 📊 Features

### Key Economic Metrics
- 📈 **Inflation Rate** — Consumer Price Index (CPI) annual data
- 🏦 **GDP Growth Rate** — Nigeria's economic growth trajectory
- 💰 **Real Interest Rate** — CBN monetary policy impact
- 👷 **Unemployment Rate** — Labour market health indicator

### Live Market Data
- 💱 **USD/NGN Exchange Rate** — Real-time Naira performance
- 🛢️ **Brent Crude Oil Price** — Nigeria's primary revenue driver
- 📉 **NGX All Share Index** — Nigerian Stock Exchange performance

### Analytics & Visualizations
- 📊 Interactive trend charts for all indicators
- 📉 GDP Growth bar chart with positive/negative color coding
- 🔥 Correlation heatmap between economic indicators
- 📈 Inflation trend with area chart visualization

### ML Forecasting
- 🤖 **Linear Regression forecasting** for inflation rate
- 📅 Configurable forecast horizon (3-12 months)
- 📊 Confidence interval bands on forecasts
- 📋 Forecast table with upper and lower bounds

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| Language | Python 3.11 |
| Web Framework | Streamlit |
| Data Sources | World Bank API, Yahoo Finance |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly Express, Plotly Graph Objects |
| ML Forecasting | Scikit-learn (Linear Regression) |
| Deployment | Streamlit Cloud |
| Version Control | GitHub |

---

## 📡 Data Sources

| Source | Data Provided |
|--------|--------------|
| **World Bank API** | Inflation, GDP, Interest Rate, Unemployment |
| **Yahoo Finance (yFinance)** | USD/NGN Exchange Rate, Brent Crude Oil |
| **Yahoo Finance (yFinance)** | NGX All Share Index |

All data is fetched in real-time with 30-minute to 1-hour caching for performance.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/Santandave961/nigeria-economic-tracker.git

# Navigate to project directory
cd nigeria-economic-tracker

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Requirements
```
streamlit
pandas
numpy
plotly
requests
yfinance
scikit-learn
matplotlib
```

---

## 📁 Project Structure

```
nigeria-economic-tracker/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
└── .gitignore         # Git ignore file
```

---

## 📈 How It Works

```
User Opens Dashboard
        ↓
World Bank API fetches economic indicators
        ↓
Yahoo Finance fetches live market data
        ↓
Pandas cleans and processes all data
        ↓
Plotly renders interactive visualizations
        ↓
Scikit-learn trains Linear Regression model
        ↓
Forecast displayed with confidence intervals
        ↓
User explores insights via interactive dashboard
```

---

## 🔍 Key Insights This Dashboard Reveals

- **Nigeria's inflation surged from ~10% in 2015 to 33%+ in 2024** — driven by fuel subsidy removal and Naira devaluation
- **The Naira lost over 70% of its value** between 2023-2024, visible in the FX chart
- **Oil price volatility directly correlates** with Nigeria's economic performance
- **GDP growth and unemployment** show inverse relationship during economic shocks
- **Correlation heatmap** reveals complex relationships between all four macro indicators

---

## 🏢 Business Relevance

This tool is directly relevant to Nigerian fintech companies:

| Company | Use Case |
|---------|----------|
| **Flutterwave** | Monitor FX rates for cross-border payment pricing |
| **Kuda Bank** | Track inflation to design competitive savings products |
| **Carbon** | Assess macroeconomic risk before loan approvals |
| **Moniepoint** | Help merchants understand their economic environment |
| **PiggyVest** | Advise users on saving and investing during inflation |

---

## 🎯 Use Cases

- **Businesses** — Make informed pricing and investment decisions
- **Fintech Companies** — Assess economic risk for financial products
- **Researchers** — Access clean visualizations of Nigerian economic data
- **Students** — Learn about Nigeria's macroeconomic trends
- **Journalists** — Reference tool for economic reporting
- **Ordinary Nigerians** — Understand forces affecting their purchasing power

---

## 📸 Screenshots

### Key Metrics Dashboard
- Real-time display of inflation, GDP, interest rate and unemployment
- Live USD/NGN exchange rate and Brent Crude oil price

### Inflation Trend Chart
- Historical inflation from 2015 to 2024
- ML forecast with confidence intervals

### Correlation Heatmap
- Relationships between all four economic indicators
- Color-coded for positive and negative correlations

---

## 🔮 Future Enhancements

- [ ] Food inflation vs core inflation breakdown
- [ ] State-level economic data for all 36 Nigerian states
- [ ] Email alerts when inflation crosses threshold
- [ ] Comparison with other African economies
- [ ] CBN monetary policy decision tracker
- [ ] Export data to CSV/Excel feature
- [ ] Mobile-optimized responsive design

---

## 👨‍💻 Author

**Okparaji Wisdom**
- GitHub: [@Santandave961](https://github.com/Santandave961)
- LinkedIn: [Okparaji Wisdom](https://linkedin.com/in/okparaji-wisdom)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [World Bank Open Data](https://data.worldbank.org/) for Nigeria economic indicators
- [Yahoo Finance](https://finance.yahoo.com/) for live market data
- [Streamlit](https://streamlit.io/) for the amazing deployment platform
- [Plotly](https://plotly.com/) for interactive visualizations

---

⭐ **If you found this project useful, please give it a star on GitHub!**

---

*Built with ❤️ for Nigeria 🇳🇬*
