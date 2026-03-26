import streamlit as st
from treys import Card, Evaluator, Deck
import plotly.express as px

st.set_page_config(page_title="Poker Pro Calculator", page_icon="🃏", layout="wide")

st.markdown("""
<style>
    div[data-testid="metric-container"] {
        background-color: #1e2127;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #333;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
    div.stButton > button {
        border-radius: 6px;
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button:hover {
        transform: scale(1.03);
        border-color: #ff4b4b;
    }
    h3 { text-align: center; }
</style>
""", unsafe_allow_html=True)

st.title("🃏 Poker Equity Pro")
st.markdown("---")

PALOS_MAP = {"s": "Picas ♠️", "h": "Corazones ♥️", "d": "Diamantes ♦️", "c": "Tréboles ♣️"}
RANKS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
SUITS = ["s", "h", "d", "c"]

if 'selected_hand' not in st.session_state: st.session_state.selected_hand = []
if 'selected_board' not in st.session_state: st.session_state.selected_board = []
if 'calc_run' not in st.session_state: st.session_state.calc_run = False

top_col1, top_col2, top_col3 = st.columns([1.5, 1.5, 1])

with top_col1:
    seleccionar_para = st.radio("🎯 Seleccionar para:", ["🟩 Tu Mano (Max 2)", "🟦 Mesa (Max 5)"], horizontal=True)
    simulaciones = st.select_slider("Precisión (Simulaciones)", options=[1000, 2500, 5000, 10000], value=5000)

with top_col2:
    st.write(f"**🟩 Tu Mano:** {st.session_state.selected_hand}")
    st.write(f"**🟦 Mesa:** {st.session_state.selected_board}")

with top_col3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Limpiar Todo", use_container_width=True):
        st.session_state.selected_hand = []
        st.session_state.selected_board = []
        st.session_state.calc_run = False
        st.rerun()
        
    calc_btn = st.button("🚀 CALCULAR EQUITY", type="primary", use_container_width=True)

if calc_btn:
    if len(st.session_state.selected_hand) != 2:
        st.error("⚠️ Selecciona exactamente 2 cartas para tu mano primero.")
        st.session_state.calc_run = False
    else:
        st.session_state.calc_run = True

if st.session_state.calc_run:
    try:
        jugador = [Card.new(c) for c in st.session_state.selected_hand]
        mesa = [Card.new(c) for c in st.session_state.selected_board]
        evaluador = Evaluator()
        victorias, derrotas, empates = 0, 0, 0
        
        progress_bar = st.progress(0)
        
        for i in range(simulaciones):
            baraja = Deck()
            for carta in jugador + mesa:
                try: baraja.cards.remove(carta)
                except ValueError: pass 
            
            mesa_simulada = list(mesa)
            cartas_faltantes = 5 - len(mesa_simulada)
            if cartas_faltantes > 0:
                mesa_simulada += baraja.draw(cartas_faltantes)
                
            oponente = baraja.draw(2)
            
            p_jugador = evaluador.evaluate(mesa_simulada, jugador)
            p_oponente = evaluador.evaluate(mesa_simulada, oponente)
            
            if p_jugador < p_oponente: victorias += 1
            elif p_jugador > p_oponente: derrotas += 1
            else: empates += 1
                
            if i % 1000 == 0: progress_bar.progress(i / simulaciones)
        progress_bar.empty()
        
        st.markdown("---")
        eq_win = (victorias / simulaciones) * 100
        eq_loss = (derrotas / simulaciones) * 100
        eq_tie = (empates / simulaciones) * 100
        
        res_col1, res_col2 = st.columns([1, 2])
        
        with res_col1:
            st.metric("🟩 WIN (Ganar)", f"{eq_win:.1f}%")
            st.metric("🟥 LOSS (Perder)", f"{eq_loss:.1f}%")
            st.metric("🟨 TIE (Empate)", f"{eq_tie:.1f}%")
            
        with res_col2:
            etiquetas = ['Victorias', 'Derrotas', 'Empates']
            valores = [victorias, derrotas, empates]
            fig = px.pie(names=etiquetas, values=valores, 
                         color=etiquetas, color_discrete_map={'Victorias':'#00cc96', 'Derrotas':'#ef553b', 'Empates':'#ab63fa'},
                         template='plotly_dark')
            fig.update_traces(textposition='inside', textinfo='percent+label', pull=[0.05, 0, 0])
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=250)
            st.plotly_chart(fig, use_container_width=True)
            
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

for i, suit_code in enumerate(SUITS):
    current_col = [col1, col2, col3, col4][i]
    with current_col:
        st.markdown(f"### {PALOS_MAP[suit_code]}")
        
        for rank_code in RANKS:
            card_code = rank_code + suit_code
            
            btn_label = f"{rank_code} {suit_code[-1]}" 
            btn_type = "secondary"
            selected = False
            
            if card_code in st.session_state.selected_hand:
                btn_label = f"🟩 {rank_code} {suit_code[-1]}" 
                btn_type = "primary"
                selected = "hand"
            elif card_code in st.session_state.selected_board:
                btn_label = f"🟦 {rank_code} {suit_code[-1]}"
                selected = "board"

            if st.button(btn_label, key=card_code, use_container_width=True, type=btn_type):
                if selected == "hand": st.session_state.selected_hand.remove(card_code)
                elif selected == "board": st.session_state.selected_board.remove(card_code)
                else:
                    if "Tu Mano" in seleccionar_para and len(st.session_state.selected_hand) < 2:
                        st.session_state.selected_hand.append(card_code)
                    elif "Mesa" in seleccionar_para and len(st.session_state.selected_board) < 5:
                        st.session_state.selected_board.append(card_code)
                st.rerun()
