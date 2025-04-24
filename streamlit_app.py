import streamlit as st

# Valores base para Z (media y desviación estándar)
z_params = {
    "Restaurants Los Cabos": (52.48781, 12.99254),
    "Best Restaurants in Cabo": (53.90244, 12.07022),
    "Restaurants Cabo": (52.70732, 10.58594),
    "Ocupación": (59.70732, 10.22557),
    "Comentarios": (58.39024, 9.89666)
}

# Función para calcular valores Z
def calcular_z(valor, media, desviacion):
    return (valor - media) / desviacion

# Predicción
def predecir_ventas(z_rlc, z_brc, z_rc, z_ocu, z_com):
    return (-44817.12 * z_rlc) + (2850.26 * z_brc) + (202813.22 * z_rc) + (-16759.48 * z_ocu) + (21959.31 * z_com) + 495774.07

# UI de Streamlit
st.title("📊 Predicción de Ventas - Metate Cabo")
st.markdown("Ingresa manualmente los índices de Google Trends, ocupación hotelera y comentarios de Tripadvisor para calcular la predicción semanal de ventas.")

# Entradas manuales
trends_rlc = st.number_input("🔍 Índice Trends - Restaurants Los Cabos", min_value=0, max_value=100, step=1)
trends_brc = st.number_input("🔍 Índice Trends - Best Restaurants in Cabo", min_value=0, max_value=100, step=1)
trends_rc  = st.number_input("🔍 Índice Trends - Restaurants Cabo", min_value=0, max_value=100, step=1)
ocupacion  = st.number_input("🏨 Índice de Ocupación Hotelera", min_value=0, max_value=100, step=1)
comentarios = st.number_input("💬 Índice de Comentarios en Tripadvisor", min_value=0, max_value=100, step=1)

# Calcular Z y mostrar predicción
if st.button("📈 Calcular Predicción de Ventas"):
    z_rlc = calcular_z(trends_rlc, *z_params["Restaurants Los Cabos"])
    z_brc = calcular_z(trends_brc, *z_params["Best Restaurants in Cabo"])
    z_rc  = calcular_z(trends_rc,  *z_params["Restaurants Cabo"])
    z_ocu = calcular_z(ocupacion,  *z_params["Ocupación"])
    z_com = calcular_z(comentarios, *z_params["Comentarios"])

    ventas = predecir_ventas(z_rlc, z_brc, z_rc, z_ocu, z_com)
    st.success(f"✅ Predicción de Ventas para la Semana: **${ventas:,.2f}**")
