import streamlit as st
from activos import Accion
from portafolio import Portafolio

# Configuración de página
st.set_page_config(page_title="Simulador de Portafolio", layout="centered")

# Inicializar portafolio
if "portafolio" not in st.session_state:
    st.session_state.portafolio = Portafolio(10000)

portafolio = st.session_state.portafolio

# Título
st.title("Simulador de Portafolio")
st.markdown("Gestiona tus inversiones de forma simple")

st.divider()

# Inputs
col1, col2 = st.columns(2)

with col1:
    ticker = st.text_input("Ticker", placeholder="Ej: AAPL")

with col2:
    cantidad = st.number_input("Cantidad", min_value=1, step=1)

st.divider()

# Botones
col3, col4, col5 = st.columns(3)

with col3:
    if st.button("Comprar"):
        try:
            accion = Accion(ticker.upper())
            precio = accion.get_precio_actual()
            portafolio.comprar(accion, cantidad, precio)
            st.success(f"Compra realizada: {cantidad} de {ticker.upper()}")
        except:
            st.error("Error en la compra")

with col4:
    if st.button("Ver portafolio"):
        st.subheader("Estado del portafolio")
        st.write("Capital:", round(portafolio.capital, 2))

        st.write("Posiciones:")
        for t, c in portafolio.posiciones.items():
            st.write(f"- {t}: {c}")

with col5:
    if st.button("Valor total"):
        valor = portafolio.calcular_valor()
        st.info(f"Valor total: {round(valor, 2)}")

st.divider()

#SIMULACIÓN
st.subheader("Simulación del portafolio")

if st.button("Simular evolución"):
    if len(portafolio.posiciones) == 0:
        st.warning("No hay activos en el portafolio")
    else:
        historial = portafolio.simular()

        st.line_chart(historial)

        # Rentabilidad
        valor_inicial = historial.iloc[0]
        valor_final = historial.iloc[-1]

        rentabilidad = (valor_final - valor_inicial) / valor_inicial

        st.success(f"Rentabilidad: {round(rentabilidad * 100, 2)}%")

st.divider()

st.caption("Proyecto simulador de portafolio de inversión")