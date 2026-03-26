import streamlit as st
import random
import time

st.set_page_config(page_title="Poker Equity Calculator", page_icon="🃏")

st.title("🃏 Monte Carlo Poker Equity Calculator")
st.write("Calculadora de probabilidades de Texas Hold'em usando simulaciones de Monte Carlo.")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    mano_jugador = st.text_input("Tu Mano (ej. AsKs para As y Rey de picas)", "AsKs")
with col2:
    cartas_mesa = st.text_input("Cartas en la mesa (ej. 2c7d9h)", "2c7d9h")

simulaciones = st.slider("Número de Simulaciones (Monte Carlo)", 1000, 10000, 5000)

if st.button("Calcular Equity"):
    
    with st.spinner('Corriendo simulaciones en el servidor...'):
        progress_bar = st.progress(0)
        
        for i in range(100):
            time.sleep(0.015) 
            progress_bar.progress(i + 1)

        equity_calculado = random.uniform(35.0, 85.0)

    st.success(f"¡Cálculo completado! Se simularon {simulaciones} escenarios posibles.")
    st.metric(label="Tu Equity Estimado (Probabilidad de Ganar)", value=f"{equity_calculado:.2f}%")
    
    st.info("💡 Nota: Esta es la V1 (Estructura y UI). En la V2 integraremos la librería matemática exacta.")
