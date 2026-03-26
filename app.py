import streamlit as st
from treys import Card, Evaluator, Deck
import plotly.express as px

st.set_page_config(page_title="Poker Pro Calculator", page_icon="🃏", layout="centered")

col_l, col_t = st.columns(2)
lang = col_l.radio("", ["ES", "EN"], horizontal=True, label_visibility="collapsed")
theme = col_t.radio("", ["Dark", "Light"], horizontal=True, label_visibility="collapsed")

if theme == "Dark":
    bg_metric = "#1e2127"
    text_color = "#ffffff"
    border_color = "#333333"
    plotly_template = "plotly_dark"
else:
    bg_metric = "#ffffff"
    text_color = "#000000"
    border_color = "#cccccc"
    plotly_template = "plotly_white"

st.markdown(f"""
<style>
    div[data-testid="metric-container"] {{
        background-color: {bg_metric};
        color: {text_color};
        border-radius: 10px;
        padding: 15px;
        border: 1px solid {border_color};
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }}
    div[data-testid="metric-container"] label {{
        color: {text_color} !important;
    }}
</style>
""", unsafe_allow_html=True)

T = {
    "ES": {
        "title": "🃏 Poker Equity Pro",
        "hand_title": "🟩 Tu Mano",
        "board_title": "🟦 Mesa (Comunitarias)",
        "pick_2": "Elige 2 cartas:",
        "pick_5": "Elige hasta 5 cartas:",
        "sims": "Precisión de cálculo",
        "btn_calc": "🚀 CALCULAR EQUITY",
        "err_hand": "⚠️ Debes seleccionar exactamente 2 cartas para tu mano.",
        "win": "🟩 WIN (Ganar)",
        "loss": "🟥 LOSS (Perder)",
        "tie": "🟨 TIE (Empate)",
        "current": "🏆 **Tu jugada actual es:**",
        "palos": {"s": "♠️ (Picas)", "h": "♥️ (Corazones)", "d": "♦️ (Diamantes)", "c": "♣️ (Tréboles)"},
        "manos": {"Straight Flush": "Escalera de Color", "Four of a Kind": "Póker", "Full House": "Full House", "Flush": "Color", "Straight": "Escalera", "Three of a Kind": "Trío", "Two Pair": "Doble Par", "Pair": "Par", "High Card": "Carta Alta"}
    },
    "EN": {
        "title": "🃏 Poker Equity Pro",
        "hand_title": "🟩 Your Hand",
        "board_title": "🟦 Board (Community)",
        "pick_2": "Choose 2 cards:",
        "pick_5": "Choose up to 5 cards:",
        "sims": "Calculation precision",
        "btn_calc": "🚀 CALCULATE EQUITY",
        "err_hand": "⚠️ You must select exactly 2 cards for your hand.",
        "win": "🟩 WIN",
        "loss": "🟥 LOSS",
        "tie": "🟨 TIE",
        "current": "🏆 **Current hand:**",
        "palos": {"s": "♠️ (Spades)", "h": "♥️ (Hearts)", "d": "♦️ (Diamonds)", "c": "♣️ (Clubs)"},
        "manos": {"Straight Flush": "Straight Flush", "Four of a Kind": "Four of a Kind", "Full House": "Full House", "Flush": "Flush", "Straight": "Straight", "Three of a Kind": "Three of a Kind", "Two Pair": "Two Pair", "Pair": "Pair", "High Card": "High Card"}
    }
}

st.title(T[lang]["title"])
st.markdown("---")

VALORES = {"A": "A", "K": "K", "Q": "Q", "J": "J", "T": "10", "9": "9", "8": "8", "7": "7", "6": "6", "5": "5", "4": "4", "3": "3", "2": "2"}

mazo_completo = []
mapa_codigos = {}
for v_key, v_val in VALORES.items():
    for p_key, p_val in T[lang]["palos"].items():
        nombre = f"{v_val} {p_val}"
        codigo = f"{v_key}{p_key}"
        mazo_completo.append(nombre)
        mapa_codigos[nombre] = codigo

def render_cards(card_list):
    if not card_list: return ""
    html = '<div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 15px;">'
    for c in card_list:
        rango = c.split()[0]
        palo_emoji = c.split()[1]
        color = "#e61919" if palo_emoji in ["♥️", "♦️"] else "#111111"
        html += f'<div style="background-color: white; border-radius: 8px; border: 1px solid #ccc; width: 70px; height: 100px; display: flex; flex-direction: column; justify-content: space-between; align-items: center; padding: 5px; box-shadow: 2px 2px 8px rgba(0,0,0,0.3); color: {color}; font-family: Arial, sans-serif; font-weight: bold;"><div style="align-self: flex-start; font-size: 16px; line-height: 1;">{rango}</div><div style="font-size: 32px; line-height: 1;">{palo_emoji}</div><div style="align-self: flex-end; font-size: 16px; line-height: 1; transform: rotate(180deg);">{rango}</div></div>'
    html += '</div>'
    return html

st.subheader(T[lang]["hand_title"])
mano_usuario = st.multiselect(T[lang]["pick_2"], mazo_completo, max_selections=2)
if mano_usuario:
    st.markdown(render_cards(mano_usuario), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.subheader(T[lang]["board_title"])
opciones_mesa = [c for c in mazo_completo if c not in mano_usuario]
mesa_usuario = st.multiselect(T[lang]["pick_5"], opciones_mesa, max_selections=5)
if mesa_usuario:
    st.markdown(render_cards(mesa_usuario), unsafe_allow_html=True)

if len(mano_usuario) == 2 and len(mesa_usuario) >= 3:
    try:
        temp_evaluator = Evaluator()
        temp_jugador = [Card.new(mapa_codigos[c]) for c in mano_usuario]
        temp_mesa = [Card.new(mapa_codigos[c]) for c in mesa_usuario]
        score = temp_evaluator.evaluate(temp_mesa, temp_jugador)
        hand_class = temp_evaluator.get_rank_class(score)
        hand_name_eng = temp_evaluator.class_to_string(hand_class)
        hand_name_final = T[lang]["manos"].get(hand_name_eng, hand_name_eng)
        st.success(f"{T[lang]['current']} {hand_name_final}")
    except Exception:
        pass

st.markdown("---")
simulaciones = st.select_slider(T[lang]["sims"], options=[1000, 2500, 5000, 10000], value=5000)

if st.button(T[lang]["btn_calc"], type="primary", use_container_width=True):
    if len(mano_usuario) != 2:
        st.error(T[lang]["err_hand"])
    else:
        try:
            jugador = [Card.new(mapa_codigos[c]) for c in mano_usuario]
            mesa = [Card.new(mapa_codigos[c]) for c in mesa_usuario]
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
            
            res_col1, res_col2 = st.columns([1, 1.5])
            
            with res_col1:
                st.metric(T[lang]["win"], f"{eq_win:.1f}%")
                st.metric(T[lang]["loss"], f"{eq_loss:.1f}%")
                st.metric(T[lang]["tie"], f"{eq_tie:.1f}%")
                
            with res_col2:
                etiquetas = ['Win', 'Loss', 'Tie'] if lang == "EN" else ['Victorias', 'Derrotas', 'Empates']
                valores = [victorias, derrotas, empates]
                fig = px.pie(names=etiquetas, values=valores, 
                             color=etiquetas, color_discrete_sequence=['#00cc96', '#ef553b', '#ab63fa'],
                             template=plotly_template)
                fig.update_traces(textposition='inside', textinfo='percent+label', pull=[0.05, 0, 0])
                fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
                
        except Exception as e:
            st.error(f"Error: {e}")
