import streamlit as st
from activos import Accion
from portafolio import Portafolio
from datetime import timedelta

# Configuración de página
st.set_page_config(page_title="Simulador de Portafolio", layout="centered")

# Inicializar portafolio
if "portafolio" not in st.session_state:
    st.session_state.portafolio = Portafolio(10000)

portafolio = st.session_state.portafolio

# Título
st.title("Simulador de Portafolio")
st.markdown("Gestiona tus inversiones de forma simple")

if st.button("Reiniciar portafolio"):
    st.session_state.portafolio = Portafolio(10000)
    st.success("Portafolio reiniciado")

st.divider()

st.subheader("Renta Fija (CDT)")

if st.button("Ver CDTs"):
    st.subheader("Mis CDTs")

    if len(portafolio.cdts) == 0:
        st.info("No hay CDTs activos")
    else:
        for i, cdt in enumerate(portafolio.cdts):
            valor = cdt.actualizar()

            st.write({
                "CDT": i + 1,
                "Capital": cdt.capital,
                "Valor actual": round(valor, 2),
                "Interés acumulado": round(cdt.interes_acumulado, 2),
                "Días": cdt.dias_transcurridos
            })

capital_cdt = st.number_input("Capital CDT", min_value=100)
tasa = st.number_input("Tasa anual (%)", min_value=0.0) / 100
dias = st.number_input("Plazo en días", min_value=1)

if st.button("Crear CDT"):
    mensaje = portafolio.agregar_cdt(capital_cdt, tasa, dias)
    st.success(mensaje)

st.subheader("Renta variable (Acciones y ETFs)")
if len(portafolio.posiciones) == 0:
        st.info("No hay acciones o ETFs en el portafolio")
# Inputs
col1, col2 = st.columns(2)

with col1:
    ticker = st.text_input("Ticker", placeholder="Ej: AAPL")

with col2:
    cantidad = st.number_input("Cantidad", min_value=1, step=1)


# Botones
col3, col4, col5 = st.columns(3)

with col3:
    if st.button("Comprar"):
        if not ticker:
            st.warning("Ingresa un ticker")
        else:
            try:
                accion = Accion(ticker.upper())
                precio = accion.get_precio_actual()

                resultado = portafolio.comprar(accion, cantidad, precio)

                if resultado is None:
                    st.error("Error inesperado en la compra")
                elif "realizada" in resultado:
                    st.success(f"{resultado}: {cantidad} de {ticker.upper()}")
                else:
                    st.error(f"{resultado}")

            except Exception as e:
                st.error(f"Error en la compra: {str(e)}")

with col4:
    if st.button("Ver Wallet"):
        st.subheader("Acciones compradas")
        st.write("Capital:", round(portafolio.capital, 2))

        if not portafolio.posiciones:
            st.info("No hay posiciones")
        else:
            for t, data in portafolio.posiciones.items():
                st.write(f"{t} → Cantidad: {data['cantidad']} | Precio Prom: {data['precio_promedio']:.2f}")

#with col5:
#    if st.button("Valor total"):
 #       valor = portafolio.calcular_valor()
  #      st.info(f"Valor total: {round(valor, 2)}")

st.divider()


st.subheader("Estado de portafolio")

valor_acciones = portafolio.calcular_valor() - portafolio.capital - portafolio.valor_total_cdts()
valor_cdts = portafolio.valor_total_cdts()

st.write("Capital:", round(portafolio.capital, 2))
st.write("Acciones:", round(valor_acciones, 2))
st.write("CDTs:", round(valor_cdts, 2))
st.write("TOTAL PORTAFOLIO:", round(portafolio.calcular_valor(), 2))

st.subheader("Simulación del portafolio")

if st.button("Simular evolución"):
    if len(portafolio.posiciones) == 0:
        st.warning("No hay activos en el portafolio o no está diversificado.")
    else:
        historial = portafolio.simular()

        if historial is None:
            st.error("No se pudo generar la simulación")
        else:
            st.line_chart(historial)

            # ✔ Rentabilidad real (backend)
            rentabilidad = portafolio.calcular_rentabilidad()
            st.success(f"Rentabilidad: {rentabilidad * 100:.2f}%")

            # ✔ Dividendos
            dividendos = portafolio.calcular_dividendos()
            st.info(f"Dividendos acumulados: ${dividendos:.2f}")

st.caption("Proyecto simulador de portafolio de inversión")