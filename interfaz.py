import streamlit as st
from activos import Accion
from portafolio import Portafolio
import pandas as pd

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Simulador de Portafolio", layout="wide")

# =========================
# ESTADO
# =========================
if "portafolio" not in st.session_state:
    st.session_state.portafolio = Portafolio(10000)

portafolio = st.session_state.portafolio

# =========================
# HEADER / KPIs GLOBALES
# =========================
st.title("📊 Simulador de Portafolio")

col1, col2, col3 = st.columns(3)

col1.metric("💰 Capital", f"${portafolio.capital:,.2f}")
col2.metric("💎 Valor total", f"${portafolio.calcular_valor():,.2f}")
col3.metric("🏦 CDTs activos", len(portafolio.cdts))

if st.button("🔄 Reiniciar portafolio"):
    st.session_state.portafolio = Portafolio(10000)
    st.success("Portafolio reiniciado")

st.divider()

# =========================
# TABS PRINCIPALES
# =========================
tab1, tab2, tab3, tab4 = st.tabs(["📊 Wallet", "🏦 CDTs", "📈 Trading", "🚀 Simulación"])

# =========================================================
# TAB 1 - WALLET (ACCIONES)
# =========================================================
with tab1:
    st.subheader("Wallet (Patrimonio total)")

    # =========================
    # CAPITAL
    # =========================
    st.metric("💰 Capital disponible", f"${portafolio.capital:,.2f}")

    st.divider()

    # =========================
    # ACCIONES
    # =========================
    st.markdown("### Renta Variable (Acciones)")

    if len(portafolio.posiciones) == 0:
        st.info("No tienes acciones")
    else:
        for t, data in portafolio.posiciones.items():
            st.write(f"🔹 {t} → {data['cantidad']} unidades | Promedio: {data['precio_promedio']:.2f}")

    # =========================
    # CDTs
    # =========================
    st.markdown("### Renta Fija (CDTs)")

    if len(portafolio.cdts) == 0:
        st.info("No tienes CDTs activos")
    else:
        for i, cdt in enumerate(portafolio.cdts):

            valor = cdt.actualizar()

            st.write(f"CDT #{i + 1}")

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric("Capital", f"${cdt.capital:,.2f}")

            with c2:
                st.metric("Valor actual", f"${valor:,.2f}")

            with c3:
                st.metric("Días", cdt.dias_transcurridos)

    st.divider()

    # =========================
    # RESUMEN TOTAL
    # =========================
    st.markdown("### Resumen del portafolio")

    valor_total = portafolio.calcular_valor()
    valor_cdts = portafolio.valor_total_cdts()

    st.write("💰 Capital:", round(portafolio.capital, 2))
    st.write("📈 Acciones:", round(valor_total - portafolio.capital - valor_cdts, 2))
    st.write("🏦 CDTs:", round(valor_cdts, 2))

    st.success(f"💎 VALOR TOTAL: ${valor_total:,.2f}")

    if st.button("📄 Generar reporte PDF"):

        archivo = portafolio.generar_reporte_pdf()

        with open(archivo, "rb") as f:
            st.download_button(
                label="⬇ Descargar reporte",
                data=f,
                file_name="reporte_portafolio.pdf",
                mime="application/pdf"
            )

# =========================================================
# TAB 2 - CDTs
# =========================================================
with tab2:
    st.subheader("🏦 Renta Fija (CDT)")

    capital_cdt = st.number_input("Capital CDT", min_value=100)
    tasa = st.number_input("Tasa anual (%)", min_value=0.0) / 100
    dias = st.number_input("Plazo en días", min_value=1)

    colA, colB = st.columns(2)

    with colA:
        if st.button("Crear CDT"):
            mensaje = portafolio.agregar_cdt(capital_cdt, tasa, dias)
            st.success(mensaje)

    with colB:
        if st.button("Ver CDTs"):
            if len(portafolio.cdts) == 0:
                st.info("No hay CDTs activos")
            else:
                for i, cdt in enumerate(portafolio.cdts):

                    valor = cdt.actualizar()

                    st.markdown(f"### 🏦 CDT #{i + 1}")

                    c1, c2, c3 = st.columns(3)

                    with c1:
                        st.metric("Capital", f"${cdt.capital:,.2f}")

                    with c2:
                        st.metric("Valor actual", f"${valor:,.2f}")

                    with c3:
                        st.metric("Días", cdt.dias_transcurridos)

                    st.caption(f"📈 Interés acumulado: ${cdt.interes_acumulado:,.2f}")

# =========================================================
# TAB 3 - TRADING
# =========================================================
with tab3:
    st.subheader("📈 Renta Variable (Acciones - Trading)")

    col1, col2 = st.columns(2)

    with col1:
        ticker = st.text_input("Ticker", placeholder="Ej: AAPL")

    with col2:
        cantidad = st.number_input("Cantidad", min_value=1, step=1)

    col3, col4 = st.columns(2)

    with col3:
        if st.button("Comprar"):
            if not ticker:
                st.warning("Ingresa un ticker")
            else:
                accion = Accion(ticker.upper())
                precio = accion.get_precio_actual()

                resultado = portafolio.comprar(accion, cantidad, precio)

                if "realizada" in resultado:
                    st.success("✔ " + resultado)
                else:
                    st.error("❌ " + resultado)

    with col4:
        if st.button("Ver Compras"):
            st.subheader("📦 Posiciones")

            if not portafolio.posiciones:
                st.info("No hay posiciones")
            else:
                for t, data in portafolio.posiciones.items():
                    st.write(f"{t} → {data['cantidad']} unidades | Promedio: {data['precio_promedio']:.2f}")

    st.divider()

    # =========================
    # VENTA
    # =========================
    with st.expander("Vender activos"):
        ticker_sell = st.text_input("Ticker", key="sell_ticker")
        qty_sell = st.number_input("Cantidad", min_value=1, key="sell_qty")

        if st.button("Vender"):
            if not ticker_sell:
                st.warning("Ingresa ticker")
            else:
                accion = Accion(ticker_sell.upper())
                precio = accion.get_precio_actual()

                portafolio.vender(accion, qty_sell, precio)

                st.success(f"Venta ejecutada: {qty_sell} de {ticker_sell.upper()}")

    st.divider()

with tab4:
    # =========================
    # SIMULACIÓN
    # =========================

    st.subheader("📊 Simulación del portafolio")

    dias_simulacion = st.number_input(
    "Días de simulación",
    min_value=5,
    max_value=365,
    value=30,
    step=5
    )

    if st.button("Simular evolución"):

        historial = portafolio.simular(dias=dias_simulacion)

        if historial is None:
            st.error("No se pudo generar simulación")
        else:
            # =========================
            # GRÁFICO PRINCIPAL
            # =========================
            st.line_chart(historial)

            # =========================
            # MÉTRICAS PRINCIPALES
            # =========================
            valor_final = historial.iloc[-1]
            valor_inicial = portafolio.capital_inicial

            retorno = (valor_final - valor_inicial) / valor_inicial

            st.divider()

            col1, col2, col3 = st.columns(3)

            col1.metric("💰 Inicial", f"${valor_inicial:,.2f}")
            col2.metric("📈 Actual", f"${valor_final:,.2f}")
            col3.metric("📊 Retorno", f"{retorno*100:.2f}%")

            # =========================
            # DRAWNDOWN SIMPLE
            # =========================
            pico = historial.max()
            drawdown = (valor_final - pico) / pico

            st.metric("📉 Drawdown", f"{drawdown*100:.2f}%")

            # =========================
            # BENCHMARK SIMPLE
            # =========================
            st.subheader("📉 Comparación base")

            base = pd.Series(
                [portafolio.capital_inicial] * len(historial),
                index=historial.index
            )

            st.line_chart({
                "Portafolio": historial,
                "Base": base
            })

            # =========================
            # DATOS DETALLADOS
            # =========================
            st.subheader("📋 Últimos datos")

            st.dataframe(historial.tail(10))
    

# =========================
# FOOTER
# =========================
st.caption("Proyecto simulador de portafolio de inversión")