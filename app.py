import streamlit as st
from treys import Card, Evaluator, Deck
import time

st.set_page_config(page_title="Poker Equity Calculator", page_icon="🃏")
st.title("🃏 Monte Carlo Poker Equity Calculator")
st.write("Calculadora de probabilidades de Texas Hold'em usando simulaciones reales.")
st.markdown("---")

def parse_cartas(texto_cartas):
    if not texto_cartas: return []
    cartas = []
    for i in range(0, len(texto_cartas), 2):
        cartas.append(Card.new(texto_cartas[i:i+2]))
    return cartas

col1, col2 = st.columns(2)
with col1:
    mano_jugador = st.text_input("Tu Mano (ej. AsKs, Td9h)", "AsKs")
with col2:
    cartas_mesa = st.text_input("Mesa (Déjalo en blanco si es Pre-Flop, o ej. 2c7d9h)", "")

simulaciones = st.slider("Número de Simulaciones (Monte Carlo)", 1000, 10000, 5000)

if st.button("Calcular Equity Real"):
    try:
        jugador = parse_cartas(mano_jugador)
        mesa = parse_cartas(cartas_mesa)
        
        evaluador = Evaluator()
        victorias = 0
        empates = 0
        
        progress_bar = st.progress(0)
        estado = st.empty()
        
        for i in range(simulaciones):
            baraja = Deck()
            
            for carta in jugador + mesa:
                baraja.cards.remove(carta)
            
            mesa_simulada = list(mesa)
            cartas_faltantes = 5 - len(mesa_simulada)
            if cartas_faltantes > 0:
                mesa_simulada += baraja.draw(cartas_faltantes)
                
            oponente = baraja.draw(2)
            
            puntaje_jugador = evaluador.evaluate(mesa_simulada, jugador)
            puntaje_oponente = evaluador.evaluate(mesa_simulada, oponente)
            
            if puntaje_jugador < puntaje_oponente:
                victorias += 1
            elif puntaje_jugador == puntaje_oponente:
                empates += 1
                
            if i % 500 == 0:
                progress_bar.progress(i / simulaciones)
                estado.text(f"Simulando escenario {i} de {simulaciones}...")
        
        progress_bar.empty()
        estado.empty()
        
        equity = ((victorias + (empates / 2)) / simulaciones) * 100
        
        st.success(f"¡Cálculo exacto completado! Basado en {simulaciones} escenarios aleatorios.")
        st.metric(label="Tu Equity Real (Probabilidad de Ganar/Empatar)", value=f"{equity:.2f}%")
        
    except Exception as e:
        st.error("⚠️ Error en el formato de las cartas. Asegúrate de usar mayúsculas para los valores (A, K, Q, J, T) y minúsculas para los palos (s, h, d, c).")
