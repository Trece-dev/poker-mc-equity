import streamlit as st
from treys import Card, Evaluator, Deck
import plotly.express as px

st.set_page_config(page_title="Poker Pro Calculator", page_icon="🃏", layout="centered")

col_l, col_t = st.columns(2)
lang = col_l.radio("", ["ES", "EN"], horizontal=True, label_visibility="collapsed")
theme = col_t.radio("", ["Dark", "Light"], horizontal=True, label_visibility="collapsed")

if theme == "Dark":
    bg_main = "#0e1117"
    text_main = "#ffffff"
    bg_metric = "#1e2127"
    border = "#333333"
    ptemplate = "plotly_dark"
else:
    bg_main = "#ffffff"
    text_main = "#111111"
    bg_metric = "#f8f9fa"
    border = "#dddddd"
    ptemplate = "plotly_white"

st.markdown(f"""
<style>
    [data-testid="stAppViewContainer"] {{
        background-color: {bg_main};
    }}
    [data-testid="stHeader"] {{
        background-color: transparent;
    }}
    [data-testid="stAppViewContainer"] p, 
    [data-testid="stAppViewContainer"] h1, 
    [data-testid="stAppViewContainer"] h2, 
    [data-testid="stAppViewContainer"] h3, 
    [data-testid="stAppViewContainer"] label,
    [data-testid="stMetricLabel"] div,
    [data-testid="stMetricValue"] div {{
        color: {text_main} !important;
    }}
    div[data-testid="metric-container"] {{
        background-color: {bg_metric} !important;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid {border};
        text-align: center;
    }}
</style>
""", unsafe_allow_html=True)

T = {
    "ES": {
        "title": "🃏 Poker Equity Pro", "ht": "🟩 Tu Mano", "bt": "🟦 Mesa (Comunitarias)",
        "p2": "Elige 2 cartas:", "p5": "Elige hasta 5 cartas:", "sims": "Precisión de cálculo",
        "calc": "🚀 CALCULAR EQUITY", "err": "⚠️ Selecciona exactamente 2 cartas.",
        "w": "🟩 WIN (Ganar)", "l": "🟥 LOSS (Perder)", "t": "🟨 TIE (Empate)",
        "curr": "🏆 **Tu jugada actual es:**",
        "palos": {"s": "♠️ (Picas)", "h": "♥️ (Corazones)", "d": "♦️ (Diamantes)", "c": "♣️ (Tréboles)"},
        "m": {"Straight Flush": "Escalera de Color", "Four of a Kind": "Póker", "Full House": "Full House", "Flush": "Color", "Straight": "Escalera", "Three of a Kind": "Trío", "Two Pair": "Doble Par", "Pair": "Par", "High Card": "Carta Alta"}
    },
    "EN": {
        "title": "🃏 Poker Equity Pro", "ht": "🟩 Your Hand", "bt": "🟦 Board (Community)",
        "p2": "Choose 2 cards:", "p5": "Choose up to 5 cards:", "sims": "Calculation precision",
        "calc": "🚀 CALCULATE EQUITY", "err": "⚠️ Select exactly 2 cards.",
        "w": "🟩 WIN", "l": "🟥 LOSS", "t": "🟨 TIE",
        "curr": "🏆 **Current hand:**",
        "palos": {"s": "♠️ (Spades)", "h": "♥️ (Hearts)", "d": "♦️ (Diamonds)", "c": "♣️ (Clubs)"},
        "m": {"Straight Flush": "Straight Flush", "Four of a Kind": "Four of a Kind", "Full House": "Full House", "Flush": "Flush", "Straight": "Straight", "Three of a Kind": "Three of a Kind", "Two Pair": "Two Pair", "Pair": "Pair", "High Card": "High Card"}
    }
}

st.title(T[lang]["title"])
st.markdown("---")

RANKS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
SUITS = ["s", "h", "d", "c"]
deck_codes = [r + s for r in RANKS for s in SUITS]

def fmt_card(code):
    val = "10" if code[0] == "T" else code[0]
    palo = T[lang]["palos"][code[1]]
    return f"{val} {palo}"

def render_cards(codes):
    if not codes: return ""
    html = '<div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 15px;">'
    for c in codes:
        val = "10" if c[0] == "T" else c[0]
        palo = "♠️" if c[1] == "s" else "♥️" if c[1] == "h" else "♦️" if c[1] == "d" else "♣️"
        col = "#e61919" if c[1] in ["h", "d"] else "#111111"
        html += f'<div style="background-color: white; border-radius: 8px; border: 1px solid #ccc; width: 70px; height: 100px; display: flex; flex-direction: column; justify-content: space-between; align-items: center; padding: 5px; box-shadow: 2px 2px 8px rgba(0,0,0,0.3); color: {col}; font-family: Arial, sans-serif; font-weight: bold;"><div style="align-self: flex-start; font-size: 16px; line-height: 1;">{val}</div><div style="font-size: 32px; line-height: 1;">{palo}</div><div style="align-self: flex-end; font-size: 16px; line-height: 1; transform: rotate(180deg);">{val}</div></div>'
    html += '</div>'
    return html

st.subheader(T[lang]["ht"])
mano = st.multiselect(T[lang]["p2"], deck_codes, format_func=fmt_card, max_selections=2)
if mano: st.markdown(render_cards(mano), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.subheader(T[lang]["bt"])
opciones_mesa = [c for c in deck_codes if c not in mano]
mesa = st.multiselect(T[lang]["p5"], opciones_mesa, format_func=fmt_card, max_selections=5)
if mesa: st.markdown(render_cards(mesa), unsafe_allow_html=True)

if len(mano) == 2 and len(mesa) >= 3:
    try:
        ev = Evaluator()
        j = [Card.new(c) for c in mano]
        m = [Card.new(c) for c in mesa]
        sc = ev.evaluate(m, j)
        h_eng = ev.class_to_string(ev.get_rank_class(sc))
        h_final = T[lang]["m"].get(h_eng, h_eng)
        st.success(f"{T[lang]['curr']} {h_final}")
    except Exception:
        pass

st.markdown("---")
sims = st.select_slider(T[lang]["sims"], options=[1000, 2500, 5000, 10000], value=5000)

if st.button(T[lang]["calc"], type="primary", use_container_width=True):
    if len(mano) != 2:
        st.error(T[lang]["err"])
    else:
        try:
            jugador = [Card.new(c) for c in mano]
            mesa_c = [Card.new(c) for c in mesa]
            ev = Evaluator()
            v, d, e = 0, 0, 0
            
            pb = st.progress(0)
            
            for i in range(sims):
                baraja = Deck()
                for c in jugador + mesa_c:
                    try: baraja.cards.remove(c)
                    except ValueError: pass 
                
                m_sim = list(mesa_c)
                faltantes = 5 - len(m_sim)
                if faltantes > 0: m_sim += baraja.draw(faltantes)
                    
                op = baraja.draw(2)
                
                pj = ev.evaluate(m_sim, jugador)
                po = ev.evaluate(m_sim, op)
                
                if pj < po: v += 1
                elif pj > po: d += 1
                else: e += 1
                    
                if i % 1000 == 0: pb.progress(i / sims)
            pb.empty()
            
            st.markdown("---")
            ew = (v / sims) * 100
            el = (d / sims) * 100
            et = (e / sims) * 100
            
            c1, c2 = st.columns([1, 1.5])
            
            with c1:
                st.metric(T[lang]["w"], f"{ew:.1f}%")
                st.metric(T[lang]["l"], f"{el:.1f}%")
                st.metric(T[lang]["t"], f"{et:.1f}%")
                
            with c2:
                etiq = ['Win', 'Loss', 'Tie'] if lang == "EN" else ['Victorias', 'Derrotas', 'Empates']
                val = [v, d, e]
                fig = px.pie(names=etiq, values=val, color=etiq, color_discrete_sequence=['#00cc96', '#ef553b', '#ab63fa'], template=ptemplate)
                fig.update_traces(textposition='inside', textinfo='percent+label', pull=[0.05, 0, 0])
                fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
                
        except Exception as ex:
            st.error(f"Error: {ex}")
