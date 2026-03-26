import streamlit as st
from treys import Card, Evaluator, Deck
import plotly.express as px

st.set_page_config(page_title="Poker Equity Calculator", page_icon="🃏", layout="centered")
st.title("🃏 Calculadora Visual de Poker (Monte Carlo)")
st.write("Selecciona tus cartas visualmente y calcula tu probabilidad real de ganar.")
st.markdown("---")

VALORES_VISUALES = ["As", "Rey (K)", "Reina (Q)", "Jota (J)", "Diez (10)", "9", "8", "7", "6", "5", "4", "3", "2"]
PALOS_VISUALES = ["♠️ Picas", "♥️ Corazones", "♦️ Diamantes", "♣️ Tréboles"]

mazo_visual = []
for v in VALORES_VISUALES:
    for p in PALOS_VISUALES:
        mazo_visual.append(f"{v} de {p}")

def traducir_carta(nombre_visual):
    rango = ""
    palo = ""
    
    if "As" in nombre_visual: rango = "A"
    elif "Rey" in nombre_visual: rango = "K"
    elif "Reina" in nombre_visual: rango = "Q"
    elif "Jota" in nombre_visual: rango = "J"
    elif "10" in nombre_visual: rango = "T"
    elif "9" in nombre_visual: rango = "9"
    elif "8" in nombre_visual: rango = "8"
    elif "7" in nombre_visual: rango = "7"
    elif "6" in nombre_visual: rango = "6"
    elif "5" in nombre_visual: rango = "5"
    elif "4" in nombre_visual: rango = "4"
    elif "3" in nombre_visual: rango = "3"
    elif "2" in nombre_visual: rango = "2"
    
    if "Picas" in nombre_visual: palo = "s"
    elif "Corazones" in nombre_visual: palo = "h"
    elif "Diamantes" in nombre_visual: palo = "d"
    elif "Tréboles" in nombre_visual: palo = "c"
    
    return rango + palo

st.subheader("Tus Cartas")
mano_usuario_nombres = st.multiselect("Elige exactamente 2 cartas para tu mano:", mazo_visual, max_selections=2)

st.subheader("Cartas en la Mesa (Comunitarias)")
mesa_usuario_nombres = st.multiselect("Elige hasta 5 cartas (déjalo vacío si es Pre-Flop):", mazo_visual, max_selections=5)

simulaciones = st.slider("Número de Simulaciones (Mayor precisión = Más tiempo)", 1000, 10000, 5000)

if st.button("📊 Calcular Probabilidades"):
    
    if len(mano_usuario_nombres) != 2:
        st.warning("⚠️ Por favor, selecciona exactamente 2 cartas para tu mano antes de calcular.")
    else:
        try:
            jugador = [Card.new(traducir_carta(nombre)) for nombre in mano_usuario_nombres]
            mesa = [Card.new(traducir_carta(nombre)) for nombre in mesa_usuario_nombres]
            
            evaluador = Evaluator()
            victorias = 0
            derrotas = 0
            empates = 0
            
            progress_bar = st.progress(0)
            estado = st.empty()
            
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
                
                if puntaje_jugador < puntaje_oponente: victorias += 1
                elif puntaje_jugador > puntaje_oponente: derrotas += 1
                else: empates += 1
                    
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
            
        except Exception as e:
            st.error(f"Error interno: {e}")
