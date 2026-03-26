import streamlit as st
from treys import Card, Evaluator, Deck
import plotly.express as px

st.set_page_config(page_title="Poker Pro Calculator", page_icon="🃏", layout="centered")

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
</style>
""", unsafe_allow_html=True)

st.title("🃏 Poker Equity Pro")
st.markdown("---")

VALORES = {"A": "A", "K": "K", "Q": "Q", "J": "J", "T": "T", "9": "9", "8": "8", "7": "7", "6": "6", "5": "5", "4": "4", "3": "3", "2": "2"}
PALOS = {"s": "♠️ (Picas)", "h": "♥️ (Corazones)", "d": "♦️ (Diamantes)", "c": "♣️ (Tréboles)"}

mazo_completo = []
mapa_codigos = {}
for v_key, v_val in VALORES.items():
    for p_key, p_val in PALOS.items():
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
        html += f'''
        <div style="background-color: white; border-radius: 8px; border: 1px solid #ccc; width: 70px; height: 100px; display: flex; flex-direction: column; justify-content: space-between; align-items: center; padding: 5px; box-shadow: 2px 2px 8px rgba(0,0,0,0.3); color: {color}; font-family: Arial, sans-serif; font-weight: bold;">
            <div style="align-self: flex-start; font-size: 16px; line-height: 1;">{rango}</div>
            <div style="font-size: 32px; line-height: 1;">{palo_emoji}</div>
            <div style="align-self: flex-end; font-size: 16px; line-height: 1; transform: rotate(180deg);">{rango}</div>
        </div>
        '''
    html += '</div>'
    return html

st.subheader("🟩 Tu Mano")
mano_usuario = st.multiselect("Elige 2 cartas:", mazo_completo, max_selections=2)
if mano_usuario:
    st.markdown(render_cards(mano_usuario), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("🟦 Mesa (Comunitarias)")
opciones_mesa = [c for c in mazo_completo if c not in mano_usuario]
mesa_usuario = st.multiselect("Elige hasta 5 cartas:", opciones_mesa, max_selections=5)
if mesa_usuario:
    st.markdown(render_cards(mesa_usuario), unsafe_allow_html=True)

st.markdown("---")
simulaciones = st.select_slider("Precisión de cálculo", options=[1000, 2500, 5000, 10000], value=5000)

if st.button("🚀 CALCULAR EQUITY", type="primary", use_container_width=True):
    if len(mano_usuario) != 2:
        st.error("⚠️ Debes seleccionar exactamente 2 cartas para tu mano.")
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
                fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
                st.plotly_chart(fig, use_container_width=True)
                
        except Exception as e:
            st.error(f"Error: {e}")
