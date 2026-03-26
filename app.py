import streamlit as st
from treys import Card, Evaluator, Deck
import plotly.express as px

st.set_page_config(page_title="Poker Equity Calculator", page_icon="🃏", layout="centered")
st.title("🃏 Calculadora Visual de Poker (Monte Carlo)")
st.write("Selecciona tus cartas visualmente y calcula tu probabilidad real de ganar.")
st.markdown("---")

VALORES = {"A": "As", "K": "Rey (K)", "Q": "Reina (Q)", "J": "Jota (J)", "T": "Diez (10)", "9": "9", "8": "8", "7": "7", "6": "6", "5": "5", "4": "4", "3": "3", "2": "2"}
PALOS = {"P": "♠️ Picas", "c": "♥️ Corazones", "d": "♦️ Diamantes", "t": "♣️ Tréboles"}

mazo_visual = []
mapa_cartas = {}

for v_codigo, v_nombre in VALORES.items():
    for p_codigo, p_nombre in PALOS.items():
        nombre_visual = f"{v_nombre} de {p_nombre}"
        codigo_maquina = f"{v_codigo}{p_codigo}"
        mazo_visual.append(nombre_visual)
        mapa_cartas[nombre_visual] = codigo_maquina

st.subheader("Tus Cartas")
mano_usuario_nombres = st.multiselect("Elige exactamente 2 cartas para tu mano:", mazo_visual, max_selections=2)

st.subheader("Cartas en la Mesa (Comunitarias)")
mesa_usuario_nombres = st.multiselect("Elige hasta 5 cartas (déjalo vacío si es Pre-Flop):", mazo_visual, max_selections=5)

simulaciones = st.slider("Número de Simulaciones (Mayor precisión = Más tiempo)", 1000, 10000, 5000)

if st.button("📊 Calcular Probabilidades"):
    
    if len(mano_usuario_nombres) != 2:
        st.warning("⚠️ Por favor, selecciona exactamente 2 cartas para tu mano antes de calcular.")
    else:
        jugador = [Card.new(mapa_cartas[nombre]) for nombre in mano_usuario_nombres]
        mesa = [Card.new(mapa_cartas[nombre]) for nombre in mesa_usuario_nombres]
        
        evaluador = Evaluator()
        victorias = 0
        derrotas = 0
        empates = 0
        
        progress_bar = st.progress(0)
        estado = st.empty()
        
        # BUCLE MONTE CARLO
        for i in range(simulaciones):
            baraja = Deck()
            
            for carta in jugador + mesa:
                try:
                    baraja.cards.remove(carta)
                except ValueError:
                    pass 
            
            mesa_simulada = list(mesa)
            cartas_faltantes = 5 - len(mesa_simulada)
            if cartas_faltantes > 0:
                mesa_simulada += baraja.draw(cartas_faltantes)
                
            oponente = baraja.draw(2)
            
            puntaje_jugador = evaluador.evaluate(mesa_simulada, jugador)
            puntaje_oponente = evaluador.evaluate(mesa_simulada, oponente)
            
            if puntaje_jugador < puntaje_oponente:
                victorias += 1
            elif puntaje_jugador > puntaje_oponente:
                derrotas += 1
            else:
                empates += 1
                
            if i % 500 == 0:
                progress_bar.progress(i / simulaciones)
                estado.text(f"Calculando línea temporal {i} de {simulaciones}...")
        
        progress_bar.empty()
        estado.empty()
        
        equity_win = (victorias / simulaciones) * 100
        equity_tie = (empates / simulaciones) * 100
        equity_loss = (derrotas / simulaciones) * 100
        
        st.success("¡Análisis completado!")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Prob. de Ganar", f"{equity_win:.2f}%")
        col2.metric("Prob. de Perder", f"{equity_loss:.2f}%")
        col3.metric("Prob. de Empatar", f"{equity_tie:.2f}%")
        
        etiquetas = ['Victorias', 'Derrotas', 'Empates']
        valores = [victorias, derrotas, empates]
        
        fig = px.pie(names=etiquetas, values=valores, title='Distribución de Posibles Resultados',
                     color=etiquetas, color_discrete_map={'Victorias':'#28a745', 'Derrotas':'#dc3545', 'Empates':'#ffc107'})
        
        fig.update_traces(textposition='inside', textinfo='percent+label', pull=[0.1, 0, 0])
        
        st.plotly_chart(fig)
