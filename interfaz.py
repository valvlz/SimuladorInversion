import streamlit as st
from activos import Accion
from portafolio import Portafolio

# Inicializar portafolio
if "portafolio" not in st.session_state:
    st.session_state.portafolio = Portafolio(10000)

portafolio = st.session_state.portafolio

st.title("Simulador de Portafolio")

# Inputs
ticker = st.text_input("Ticker")
cantidad = st.number_input("Cantidad", min_value=1, step=1)

if st.button("Comprar"):
    try:
        accion = Accion(ticker)
        precio = accion.get_precio_actual()
        portafolio.comprar(accion, cantidad, precio)
        st.success(f"Compra realizada: {cantidad} de {ticker}")
    except:
        st.error("Error en la compra")

if st.button("Ver portafolio"):
    st.write("Capital:", round(portafolio.capital, 2))
    st.write("Posiciones:", portafolio.posiciones)

if st.button("Valor total"):
    valor = portafolio.calcular_valor()
    st.write("Valor total:", round(valor, 2))