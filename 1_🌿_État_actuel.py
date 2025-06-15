import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import ast
from models.decoder_latent_onnx_v1 import decode_vector
from utils import *
import mysql.connector

conn = mysql.connector.connect(
    user="railway",
    password="yL-iD82PjIlSjxB4MEvBDiPEC8OSVmvu",
    host="nozomi.proxy.rlwy.net",
    port=24836,
    database="railway"
)


cur = conn.cursor()


sidebar_bg_css = """
<style>
/* Hide Streamlit's top-right menu */
[data-testid="stToolbar"] {
    visibility: hidden !important;
}
[data-testid="stHeader"] {
    background-color: #ECFAE5;
}
[data-testid="stAppViewContainer"] {
    background-color: #ECFAE5;
}
[data-testid="stSidebar"] {
    background-color: #DDF6D2;
}
</style>
"""

st.markdown("""
<style>
/* Custom Sidebar Title */
[data-testid="stSidebarNav"]::before {
    content: "🌾 Smart Farming";
    font-size: 28px;
    font-weight: 600;
    color: green;
    display: block;
    padding: 10px 0 5px 16px;
    margin: 0px 15px 20px 15px;
}


#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown(sidebar_bg_css, unsafe_allow_html=True)

# === Charger les données ===

st.markdown("### 🌿 Paramètres agricoles en temps réel")

# === Input ===

query = """
SELECT temperature_sol, humidite_sol, temperature_air, humidite_air, vecteur_latent
FROM plant_data
ORDER BY id DESC
"""
cur.execute(query)


row = cur.fetchone()

temperature_sol, humidite_sol, temperature_air, humidite_air, latent_vector = row

# === affichage de l'image ===
latent_vector = np.array(ast.literal_eval(latent_vector), dtype=np.float32)
latent_vector = latent_vector.reshape(1, 2, 16, 16)

image_reconstruite = decode_vector(latent_vector, model_path="models/decoder_v1.onnx")

col1, col2, col3 = st.columns([1, 1.2, 1])
with col2:
    st.image(image_reconstruite, use_container_width=True)

col1, col2 = st.columns([0.25,1])
with col1:
    # === Choisir le mode d'affichage ===
    view_mode = st.radio("Mode de visualisation", ["Jauge", "Tableau"])

if view_mode == "Jauge":
    col1, col2= st.columns(2)

    with col1:
        plot_gauge(temperature_sol, "Température du sol (°C)", 0, 50, [18, 30], [30, 35], [(0, 18), (35, 50)])
        plot_gauge(humidite_sol, "Humidité du sol (%)", 0, 100, [40, 70], [30, 40], [(0, 30), (70, 100)])

    with col2:
        plot_gauge(temperature_air, "Température de l'air (°C)", 0, 60, [20, 35], [35, 40], [(0, 20), (40, 60)])
        plot_gauge(humidite_air, "Humidité de l'air (%)", 0, 100, [40, 70], [30, 40], [(0, 30), (70, 100)])

    col1, col2, col3 = st.columns([0.83,1,1])

else:
    valeurs = list(map(int, [temperature_sol, humidite_sol, temperature_air, humidite_air]))
    units = ["°C", "%", "°C", "%"]

    valeurs_affichee = [f"{val} {unit}" for val, unit in zip(valeurs, units)]
    data = {
        "Paramètre": [
            "Température du sol (°C)",
            "Humidité du sol (%)",
            "Température de l'air (°C)",
            "Humidité de l'air (%)"
        ],
        "valeur": valeurs_affichee,
        "Intervalle optimale": [
            "[18, 30]",
            "[40, 70]",
            "[20, 35]",
            "[40, 70]"
        ]
    }


    df_table = pd.DataFrame(data)
    st.dataframe(style_plant_table1(df_table), hide_index=True)
