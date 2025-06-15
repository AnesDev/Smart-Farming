import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import plot_altair
import mysql.connector
import datetime


conn = mysql.connector.connect(
    user="railway",
    password="yL-iD82PjIlSjxB4MEvBDiPEC8OSVmvu",
    host="nozomi.proxy.rlwy.net",
    port=24836,
    database="railway"
)


cur = conn.cursor()

# === UI Styling ===
st.markdown("""
<style>
#MainMenu, footer {visibility: hidden;}
header {visibility: hidden;}
/* ===== App Theme Colors ===== */
[data-testid="stHeader"],
[data-testid="stAppViewContainer"] {
    background-color: #ECFAE5;
}
[data-testid="stSidebar"] {
    background-color: #DDF6D2;
}
[data-testid="stSidebarNav"]::before {
    content: "🌾 Smart Farming";
    font-size: 25px;
    font-weight: 600;
    color: green;
    display: block;
    padding: 10px 0 5px 16px;
}

/* ===== Custom Date Label ===== */
.custom-label {
    font-size: 20px;
    font-weight: bold;
    color: #174206;
    text-align: center;
    margin-bottom: 0px !important;
    line-height: 1 !important;
}

/* ===== Remove vertical spacing in columns ===== */
div[data-testid="column"] > div {
    gap: 0px !important;
    margin: 0px !important;
    padding: 0px !important;
}

/* ===== Streamlit DateInput Cleanup ===== */
div[data-testid="stDateInput"] {
    padding: 0 !important;
    margin: 0 !important;
}
div[data-testid="stDateInput"] > div:first-child {
    padding: 0 !important;
    margin: 0 !important;
}

/* ===== Input Wrapper Styling ===== */
div[data-baseweb="input"] {
    background-color: #F0FFF0 !important;
    border: 1.33px solid #2B7A0B !important;
    border-radius: 6px !important;
    padding: 0 !important;
    margin: 0 !important;
    box-shadow: none !important;
    display: flex;
    align-items: center;
    width: 100%;
}

/* ===== Actual Input Field ===== */
div[data-baseweb="input"] input {
    background-color: transparent !important;
    color: #174206 !important;
    border: none !important;
    padding: 8px 12px !important;
    font-weight: bold;
    font-size: 15px !important;
    width: 100%;
    outline: none !important;
    box-shadow: none !important;
}

/* ===== Fix calendar icon color ===== */
input[type="text"]::-webkit-calendar-picker-indicator {
    background: none !important;
    filter: invert(32%) sepia(76%) saturate(423%) hue-rotate(74deg) brightness(95%) contrast(92%);
    height: 20px !important;
    width: 20px !important;
    cursor: pointer;
    margin: 0 !important;
    padding: 0 !important;
}

/* ===== Hide Chrome's spin & clear buttons ===== */
input[type="text"]::-webkit-inner-spin-button,
input[type="text"]::-webkit-clear-button {
    display: none !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("### 📈 Évolution des paramètres agricoles")

st.write("")
st.write("")

Date_min_debut = datetime.date(2000, 1, 1)

cur.execute("SELECT date FROM plant_data LIMIT 1")
row = cur.fetchone()
if row:
    Date_min_debut = row[0]

# === Date selectors ===
col1, col2, col3, col4, col5 = st.columns([1.2,1.2,1.2,1.2,1.2])

with col2:
    st.markdown('<div class="custom-label">Date de début</div>', unsafe_allow_html=True)
    debut = st.date_input("", key="date_debut",
                              value=Date_min_debut,
                              min_value=Date_min_debut)

with col4:
    st.markdown('<div class="custom-label">Date de fin</div>', unsafe_allow_html=True)
    Date_fin_min = debut + datetime.timedelta(days=1)
    fin = st.date_input("", key="date_fin",
                            value=Date_fin_min,
                            min_value=Date_fin_min)


query = """
SELECT date, temperature_sol, humidite_sol, temperature_air, humidite_air
FROM plant_data
WHERE date BETWEEN %s AND %s
ORDER BY date
"""

cur.execute(query, (debut, fin))
rows = cur.fetchall()

df = pd.DataFrame(rows, columns=[
    "date", "temp_sol", "hum_sol", "temp_air", "hum_air"
])

st.write("")
st.write("")
st.markdown("##### 🌡️ Température du sol")
st.altair_chart(plot_altair(df, "temp_sol", "Température du sol"), use_container_width=False)

st.markdown("##### 💧 Humidité du sol")
st.altair_chart(plot_altair(df, "hum_sol", "Humidité du sol"), use_container_width=False)

st.markdown("##### 🌤️ Température de l'air")
st.altair_chart(plot_altair(df, "temp_air", "Température de l'air"), use_container_width=False)

st.markdown("##### ☁️ Humidité de l'air")
st.altair_chart(plot_altair(df, "hum_air", "Humidité de l'air"), use_container_width=False)
