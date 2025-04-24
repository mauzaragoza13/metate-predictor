import streamlit as st
import pandas as pd
from pytrends.request import TrendReq

# Configura pytrends
pytrends = TrendReq(hl='es', tz=360)

# Lista de términos de búsqueda
keywords = {
    "Restaurants Los Cabos": "Restaurants los cabos",
    "Best Restaurants in Cabo": "Best restaurants in Cabo",
    "Restaurants Cabo": "Restaurants Cabo"
}

# Valores base para Z (media y desviación estándar)
z_params = {
    "Restaurants Los Cabos": (52.48781, 12.99254),
    "Best Restaurants in Cabo": (53.90244, 12.07022),
    "Restaurants Cabo": (52.70732, 10.58594),
    "Ocupación": (59.70732, 10.22557)
}

# Función para obtener el último valor de Google Trends
def get_latest_trend(term):
    try:
        pytrends.build_payload([term], cat=0, timeframe='now 7-d', geo='MX')
        data = pytrends.interest_over_time()
        if not data.empty:
            return data[term].iloc[-1]
    except Exception as e:
        return None
    return None

# Función para calcular valores Z
def calcular_z(valor, media, desviacion):
    return (valor - media) / desviacion

# Predicción
def predecir_ventas(z_rlc, z_brc, z_rc, z_ocu):
    return (-44817.12 * z_rlc) + (2850.26 * z_brc) + (202813.22 * z_rc) + (-16759.48 * z_ocu) + 495774.07

# UI de Streamlit
st.title("📈 Predicción de Ventas - Metate Cabo")
st.markdown("Calculadora automática de ventas proyectadas con base en Google Trends y ocupación hotelera.")

# Obtener automáticamente valores de Google Trends
st.subheader("🔍 Índices de Google Trends (últimos 7 días)")
trend_values = {}
for key, term in keywords.items():
    value = get_latest_trend(term)
    trend_values[key] = value
    if value is not None:
        st.write(f"{key}: {value}")
    else:
        st.warning(f"No se pudo obtener el índice para: {key}")

# Ingresar ocupación manualmente
ocupacion = st.number_input("🏨 Índice de Ocupación Hotelera", min_value=0, max_value=100, step=1)

# Calcular Z y mostrar predicción
if st.button("📊 Calcular Predicción de Ventas"):
    try:
        z_rlc = calcular_z(trend_values["Restaurants Los Cabos"], *z_params["Restaurants Los Cabos"])
        z_brc = calcular_z(trend_values["Best Restaurants in Cabo"], *z_params["Best Restaurants in Cabo"])
        z_rc  = calcular_z(trend_values["Restaurants Cabo"], *z_params["Restaurants Cabo"])
        z_ocu = calcular_z(ocupacion, *z_params["Ocupación"])

        ventas = predecir_ventas(z_rlc, z_brc, z_rc, z_ocu)
        st.success(f"✅ Predicción de Ventas para la Semana: **${ventas:,.2f}**")
    except Exception as e:
        st.error("Ocurrió un error al calcular la predicción. Revisa los datos.")
