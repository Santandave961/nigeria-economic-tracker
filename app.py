import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")


st.set_page_config(
    page_title="Nigeria Economic Tracker",
    page_icon=" ",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html,body, [class*="css"]{
    font-family: 'Inter', sans-serif;
    background-color: #0e1117;
    color: #ffffff;
}
.metric-card {
    background: linear-gradient(135deg, #1a1f2e, #252d3d);
    border: 1px solid #2d3748;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    margin: 5px;
}
.metric-value {
    font-size: 2rem;
    font-weight: 700;
    margin-top: 5px;
}
.metric-label {
    font-size: 0.85rem;
    color: #a0aec0;
    margin-top: 5px;
}
.metric-change {
    font-size: 0.9rem;
    margin-top: 5px;
}  
.positive { color: #ff6b6b; }
.negative { color: #00d4aa; }
.section-header {
    font-size: 1.3rem;
    font-weight: 700;
    color: #00d4aa;
    border-bottom: 2px solid #00d4aa;
    padding-bottom: 8px;
    margin: 20px 0 15px 0;
}
.stSelectbox label, stSlider label {
    color: #a0aec0 !important;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def fetch_worldbank(indicator, country="NG", start=2010, end=2024):
    url = (
        "https://api.worldbank.org/v2/country/"
        + country
        + "/indicator/"
        + indicator
        + "?date="
        + str(start)
        + ":"
        + str(end)
        + "&format=json&per_page=100"
    )     
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        if len(data) < 2 or not data[1]:
            return pd.DataFrame()
        records = [{"Year": int(d["date"]), "Value": d["value"]}
                   for d in data[1] if d["value"] is not None]
        df = pd.DataFrame(records).sort_values("Year")
        return df
    except Exception:
        return pd.DataFrame()
    
@st.cache_data(ttl=1800)
def fetch_fx():
    try:
        df = yf.download("USDNGN=X", start="2020-01-01",
                         progress=False, auto_adjust=True)
        if df.empty:
            return pd.DataFrame()
        close = df["Close"]
        if hasattr(close, "squeeze"):
            close = close.squeeze()
        out = close.reset_index()
        out.columns = ["Date", "Rate"]
        out["Date"] = pd.to_datetime(out["Date"])
        return out.dropna()
    except Exception:
        return pd.DataFrame()
    
    
@st.cache_data(ttl=1800)
def fetch_oil():
    try:
        df = yf.download("BZ=F", start="2020-01-01", 
                         progress=False, auto_adjust=True)
        if df.empty:
            return pd.DataFrame()
        close = df["Close"]
        if hasattr(close, "squeeze"):
            close = close.squeeze()
        out = close.reset_index()
        out.columns = ["Date", "Price"]
        out["Date"] = pd.to_datetime(out["Date"])
        return out.dropna()
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=1800)
def fetch_ngx():
    try:
        df = yf.download("^NGSEASI", start="2020-01-01",
                         progress=False, auto_adjust=True)
        if df.empty:
            return pd.DataFrame()
        close = df["Close"].squeeze()
        out = close.reset_index()
        out.columns = ["Date", "Price"]
        out["Date"] = pd.to_datetime(out["Date"])
        return out.dropna()
    except Exception:
        return pd.DataFrame()
    
    
def forecast_sarima(series, steps=6):
    try:
        from sklearn.linear_model import LinearRegression
        import numpy as np
        df = series.reset_index()
        df.columns = ["Year", "Value"]
        df = dropna()
        X = df["Year"].values.reshape(-1, 1)
        y = df["Value"].values
        model = LinearRegression()
        model.fit(X, Y)
        last_year = int(df["Year"].iloc[-1])
        future_years = np.array(
            [last_year + i + 1 for i in range(steps)]
        ).reshape(-1, 1)
        predictions = model.predict(future_years)
        mean = pd.Series(
            predictions,
            index=range(steps)
        )
        margin = y.std() * 1.5
        ci = pd.DataFrame({
            "lower": predictions - margin,
            "upper": predictions + margin
        })
        return mean, ci
    except Exception:
        return None, None
        
def metric_card(col, label, df, unit="", invert=False):
    with col:
        if df is not None and not df.empty and "Value" in df.columns:
            latest = float(df["Value"].iloc[-1])
            prev = float(df["Value"].iloc[-2]) if len(df) > 1 else latest
            change = latest - prev
            arrow = "▲" if change > 0 else "▼"
            css = "positive" if (change > 0 and not invert) else "negative"
            val_display = str(round(latest, 1)) + unit
            chg_display = str(round(abs(change), 1)) + unit
            card_html = (
                '<div class="metric-card">'
                '<div class="metric-value">' + val_display + "</div>"
                '<div class="metric-label">' + label + "</div>"
                '<div class="metric-change ' + css + '">'
                + arrow + ' ' + chg_display + 'YoY'
                + '<div></div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)


def live_card(col, label, df, col_name, prefix="", unit="", invert=False):
    with col:
     if df is not None and not df.empty and col_name in df.columns:
        latest = float(df[col_name].iloc[-1])
        prev = float(df[col_name].iloc[-2]) if len(df) > 1 else latest
        change = latest - prev
        pct = (change / prev * 100) if prev else 0
        arrow = "▲" if change > 0 else "▼"
        css = "positive" if change > 0 else "negative"
        val_display = prefix + str("{:,.1f}".format(latest))
        pct_display = str(round(abs(pct),2))
        card_html = (
            '<div class="metric-card">'
            '<div class="metric-value">' + val_display + unit + "</div>"
            '<div class="metric-label">' + label + "</div>"
            '<div class="metric-change ' + css + '">'
            + arrow + ' ' + pct_display + ' pct'
            + '<div></div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)
     else:
         card_html = (
            '<div class="metric-card>'  
            '<div class="metric-value">N/A</div>'
            '<div class="metric-label">' + label + "</div>" 
            '</div>'
        )
         st.markdown(card_html, unsafe_allow_html=True)
    

st.sidebar.markdown("## Nigeria Economic Tracker") 
st.sidebar.markdown("*Real-time economic intelligence*")
st.sidebar.markdown("---")
start_year = st.sidebar.slider("Start Year", 2010, 2022, 2015)
forecast_months = st.sidebar.slider("Forecast Horizon (months)", 3, 12, 6)
show_forecast = st.sidebar.checkbox("Show ML Forecast", value=True)
st.sidebar.markdown("---")
st.sidebar.markdown("** Data Sources **")
st.sidebar.markdown("-  World Bank API")
st.sidebar.markdown(" Yahoo Finance")
st.sidebar.markdown(" CBN Data")
st.sidebar.markdown("---")
st.sidebar.markdown("Built by Okparaji Wisdom")

st.markdown(

     "<div style='text-align: center; padding: 20px'>"
     "<h1 style='color:#00d4aa; font-weight:700; margin-bottom:5px'>"
     "Nigeria Inflation and Economic Tracker"
     "</h1>" 
     "<p style='color:#a0aec0'>Real-time tracking of Nigeria's key economic indicators powered by ML</p>"
     "</div>",
      unsafe_allow_html=True
)
       


with st.spinner("Fetching live economic data..."):
    inflation_df = fetch_worldbank("FP.CPI.TOTL.ZG", start=start_year)
    gdp_df       = fetch_worldbank("NY.GDP.MKTP.KD.ZG", start=start_year)
    interest_df  = fetch_worldbank("FR.INR.RINR", start=start_year)
    unemployment_df = fetch_worldbank("SL.UEM.TOTL.ZS", start=start_year)
    fx_df = fetch_fx()
    oil_df = fetch_oil()
    ngx_df = fetch_ngx()


st.markdown('<p class="section-header"> Key Economic Indicators</p>',
            unsafe_allow_html=True)


col1, col2, col3, col4 = st.columns(4)   
metric_card(col1, "Inflation Rate", inflation_df, " pct", invert=True)
metric_card(col2, "GDP Growth Rate", gdp_df, " pct")
metric_card(col3, "Real Interest Rate", interest_df, " pct")
metric_card(col4, "Unemployment Rate", unemployment_df, " pct", invert=True)

st.markdown("")
col5, col6, col7 = st.columns(3)
live_card(col5, "USD/NGN Exchange Rate",fx_df, "Rate", "N")
live_card(col6, "Brent Crude Oil (USD)", oil_df, "Price", "$")
live_card(col7, "NGX All Share Index", ngx_df, "Index")


st.markdown("<p class='section-header'> Inflation Rate Trend</p>", unsafe_allow_html=True)

if not inflation_df.empty:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=inflation_df["Year"], y=inflation_df["Value"],
        mode="lines+markers", name="Inflation",
        line=dict(color='#00d4aa', width=3),
        fill="tozeroy",
        fillcolor="rgba(0,212,170,0.1)"
    ))

    if show_forecast:
        mean, ci = forecast_sarima(
             inflation_df.set_index("Year")["Value"], steps=forecast_months // 12 + 1)
        if mean is not None:
             last_year = int(inflation_df["Year"].iloc[-1])
             f_years = [last_year + i + 1 for i in range(len(mean))]
             fig.add_trace(go.Scatter(
                 x=f_years, y=mean.values,
                 mode="lines+markers", name="Forecast",
                 line=dict(color="#ffd700", width=2, dash="dash")
             ))
    fig.update_layout(
         template="plotly_dark",
         paper_bgcolor="#0e1117",
         plot_bgcolor="#0e1117",
         height=400,
         xaxis_title="Year",
         yaxis_title="Inflation Rate(%)"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Inflation data unavailable")


st.markdown('<p class="section-header">Exchange Rate and Oil Price</p>',
            unsafe_allow_html=True)

col_fx, col_oil = st.columns(2)

with col_fx:
    if not fx_df.empty:
        fig = px.line(fx_df, x="Date", y="Rate",
                    title="USD/NGN Exchange Rate",
                    color_discrete_sequence=["#00d4aa"])
        fig.update_layout(template="plotly_dark",
                          paper_bgcolor="#0e1117",
                          plot_bgcolor="#0e1117", height=350)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("FX Data unavailable")

with col_oil:
    if not oil_df.empty:
        fig = px.line(oil_df, x="Date", y="Price",
                      title="Brent Crude Oil Price (USD)",
                      color_discrete_sequence=["#ffd700"])
        fig.update_layout(template="plotly_dark",
                          paper_bgcolor="#0e1117",
                          plot_bgcolor="#0e1117", height=350)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Oil price data unavailable")


st.markdown('<p class="section-header">GDP Growth and Unemployment</p>',
            unsafe_allow_html=True)


col_gdp, col_unemp = st.columns(2)

with col_gdp:
    if not gdp_df.empty:
        colors = ["#ff6b6b" if v < 0 else "#00d4aa" for v in gdp_df["Value"]]
        fig = go.Figure(go.Bar(
            x=gdp_df["Year"], y=gdp_df["Value"],
            marker_color=colors, name="GDP Growth %"
        ))
        fig.update_layout(
            title="GDP Growth Rate (%)",
            template="plotly_dark",
            paper_bgcolor="#0e1117",
            plot_bgcolor="#0e1117", height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("GDP data unavailable")

with col_unemp:
    if not unemployment_df.empty:
        fig = px.area(unemployment_df, x="Year", y="Value",
                      title="Unemployment Rate (%)",
                      color_discrete_sequence=["#ff6b6b"])
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0e1117",
            plot_bgcolor="#0e1117", height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Unemployment data unavailable")


st.markdown('<p class="section-header">NGX All Share Index </p>',
            unsafe_allow_html=True)

if not ngx_df.empty:
    fig = px.line(ngx_df, x="Date", y="Index",
                  title="Nigerian Stock Exchange - All Share Index",  
                  color_discrete_sequence=["#a78bfa"])
    fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0e1117",
            plot_bgcolor="#0e1117", height=350
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("NGX data unavailable")


st.markdown('<p class="section-header"> Economic Indicators Correlation</p>',
            unsafe_allow_html=True)
    
dfs = {
     "Inflation": inflation_df,
     "GDP Growth": gdp_df, 
     "Interest Rate": interest_df,
     "Unemployment": unemployment_df,
}
merged = None
for name, df in dfs.items():
    if df is not None and not df.empty:
        tmp = df.rename(columns={"Value":name})
        merged = tmp if merged is None else merged.merge(tmp, on="Year", how="inner")


    if merged is not None and len(merged.columns) > 2:
       corr = merged.drop("Year", axis=1).corr()
       fig = px.imshow(corr, text_auto=True, color_continuous_scale="RdYlGn",
                       title="Correlation Between Economic Indicators")
       fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0e1117",
            plot_bgcolor="#0e1117", height=400
       )
       st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Not enough data for correlation analysis")
    
if show_forecast and not inflation_df.empty:
    st.markdown('<p class="section-header"> ML Inflation Forecast (SARIMA)</P>',unsafe_allow_html=True)

    mean, ci= forecast_sarima(
        inflation_df.set_index("Year")["Value"], steps=forecast_months // 12 + 2)

    if mean is not None:
        last_year = int(inflation_df["Year"].iloc[-1])
        forecast_table = pd.DataFrame({
             "Year": [last_year + i + 1 for i in range(len(mean))],
             "Forecasted Inflation (%)": mean.values.round(2),
             "Lower Bound (%)": ci.iloc[:, 0].values.round(2),
             "Upper Bound (%)": ci.iloc[:, 1].values.round(2),
        })
        st.dataframe(forecast_table, use_container_width=True)
    else:
        st.warning("Forecast unavailable")

    
st.markdown("---")
st.markdown(
    "<div style='text-align: center; padding: 10px'>"
    " Nigerian Inflation and Economic Tracker |"
    " Built by <strong style='color:#00d4aa'>Okparaji Wisdom</strong> |"
    " Data: World Bank API and Yahoo Finance"
    "</div>",
    unsafe_allow_html=True
)





    

                 



              
                 

    
    




        
            
            

            
