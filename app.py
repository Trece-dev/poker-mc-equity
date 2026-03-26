import streamlit as st
from treys import Card, Evaluator, Deck
import plotly.express as px

st.set_page_config(page_title="Poker Grid Calculator (V4)", page_icon="🃏", layout="wide") # Layout ancho para la matriz
st.title("🃏 POKER GRID CALCULATOR (V4)")
st.write("Selección visual ultrarrápida para jugadores online.")
st.markdown("---")

PALOS_MAP = {"s": "Picas ♠️", "h": "Corazones ♥️", "d": "Diamantes ♦️", "c": "Tréboles ♣️"}
RANK_ICONS = {"A":"🂱", "K":"🃎", "Q":"🃍", "J":"🃋", "T":"🃊", "9":"🂩", "8":"🂨", "7":"🂧", "6":"🂦", "5":"🂥", "4":"🂤", "3":"🂣", "2":"🂢"}
RANKS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
SUITS = ["s", "h", "d", "c"]

if 'selected_hand' not in st.session_state:
    st.session_state.selected_hand = [] 
if 'selected_board' not in st.session_state:
    st.session_state.selected_board = []
if 'calc_run' not in st.session_state:
    st.session_state.calc_run = False 


seleccionar_para = st.radio("🎯 Seleccionar para:", ["Tus Cartas (Max 2)", "Mesa (Max 5)"], horizontal=True)

col1, col2, col3, col4 = st.columns(4)
st.markdown("<br>", unsafe_allow_html=True)

for i, suit_code in enumerate(SUITS):
    current_col = [col1, col2, col3, col4][i]
    
    with current_col:
        st.markdown(f"### {PALOS_MAP[suit_code]}")
        
        for rank_code in RANKS:
            card_code = rank_code + suit_code
            
            btn_label = f"{RANK_ICONS[rank_code]} {rank_code} {suit_code[-1]}"
            btn_type = "secondary"
            selected = False
            
            if card_code in st.session_state.selected_hand:
                btn_label = f"🟢 [H] {rank_code} {suit_code[-1]}" 
                btn_type = "primary"
                selected = "hand"
            elif card_code in st.session_state.selected_board:
                btn_label = f"🔵 [B] {rank_code} {suit_code[-1]}"
                btn_type = "secondary"
                selected = "board"

            if st.button(btn_label, key=card_code, use_container_width=True, type=btn_type):
                if selected == "hand":
                    st.session_state.selected_hand.remove(card_code)
                elif selected == "board":
                    st.session_state.selected_board.remove(card_code)
                else:
                    if "Tus Cartas" in seleccionar_para:
                        if len(st.session_state.selected_hand) < 2:
                            st.session_state.selected_hand.append(card_code)
                    else:
                        if len(st.session_state.selected_board) < 5:
                            st.session_state.selected_board.append(card_code)
                st.rerun()

st.markdown("---")
res_col1, res_col2, res_col3 = st.columns([1,1,1])

with res_col1:
    st.write("**TUS CARTAS:**")
    st.write(f"[{', '.join(st.session_state.selected_hand)}]")
with res_col2:
    st.write("**MESA:**")
    st.write(f"[{', '.join(st.session_state.selected_board)}]")
with res_col3:
    if st.button("🔄 Resetear Todo", use_container_width=True):
        st.session_state.selected_hand = []
        st.session_state.selected_board = []
        st.session_state.calc_run = False
        st.rerun()

simulaciones = st.slider("Número de Simulaciones", 1000, 10000, 5000)

if st.button("📊 Calcular", type="primary", use_container_width=True):
    if len(st.session_state.selected_hand) != 2:
        st.warning("⚠️ Selecciona exactamente 2 cartas para tu mano.")
        st.session_state.calc_run = False
    else:
        st.session_state.calc_run = True


if st.session_state.calc_run:
    try:
        jugador = [Card.new(code) for code in st.session_state.selected_hand]
        mesa = [Card.new(code) for code in st.session_state.selected_board]
        
        evaluador = Evaluator()
        victorias = 0
        derrotas = 0
        empates = 0
        
        progress_bar = st.progress(0)
        
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
                
            if i % 1000 == 0:
                progress_bar.progress(i / simulaciones)
        
        progress_bar.empty()
        
        equity_win = (victorias / simulaciones) * 100
        equity_tie = (empates / simulaciones) * 100
        equity_loss = (derrotas / simulaciones) * 100
        
        st.success("¡Análisis completado!")
        mcol1, mcol2, mcol3 = st.columns(3)
        mcol1.metric("Prob. de Ganar (WIN)", f"{equity_win:.2f}%")
        mcol2.metric("Prob. de Perder (LOSS)", f"{equity_loss:.2f}%")
        mcol3.metric("Prob. de Empatar (TIE)", f"{equity_tie:.2f}%")
        
        etiquetas = ['Victorias', 'Derrotas', 'Empates']
        valores = [victorias, derrotas, empates]
        
        fig = px.pie(names=etiquetas, values=valores, title='Distribución de Posibles Resultados',
                     color=etiquetas, color_discrete_map={'Victorias':'#28a745', 'Derrotas':'#dc3545', 'Empates':'#ffc107'})
        fig.update_traces(textposition='inside', textinfo='percent+label', pull=[0.1, 0, 0])
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error interno en el cálculo: {e}")
