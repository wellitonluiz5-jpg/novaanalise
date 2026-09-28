import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# ---------------------- CONFIGURAÇÃO DA PÁGINA ----------------------
st.set_page_config(
    page_title="⚽ Análise de Jogos de Futebol",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------- ESTILO PERSONALIZADO ----------------------
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .stApp {
        background: linear-gradient(135deg, #1a2b4a 0%, #2c3e50 100%);
    }
    h1, h2, h3 {
        color: #ffffff !important;
    }
    .metric-card {
        background: rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    .verde { color: #00ff88; }
    .vermelho { color: #ff4444; }
    .amarelo { color: #ffcc00; }
    .branco { color: #ffffff; }
</style>
""", unsafe_allow_html=True)

# ---------------------- TÍTULO ----------------------
st.title("⚽ Análise e Previsão de Jogos de Futebol")
st.subheader("Ferramenta de Cálculo de Probabilidades")
st.divider()

# ---------------------- FUNÇÃO DE CÁLCULO ----------------------
def calcular_probabilidades(pontos_casa, jogos_casa, pontos_fora, jogos_fora, media_gols_casa=1.5, media_gols_fora=1.0):
    # Evitar divisão por zero
    if jogos_casa == 0: jogos_casa = 1
    if jogos_fora == 0: jogos_fora = 1
    
    # Cálculo de pontos médios por jogo
    media_pontos_casa = pontos_casa / jogos_casa
    media_pontos_fora = pontos_fora / jogos_fora
    
    # Força relativa
    forca_total = media_pontos_casa + media_pontos_fora
    if forca_total == 0:
        prob_casa = 33.3
        prob_empate = 33.4
        prob_fora = 33.3
    else:
        # Cálculo simples de probabilidades
        prob_casa = (media_pontos_casa / forca_total) * 50
        prob_fora = (media_pontos_fora / forca_total) * 50
        prob_empate = 100 - prob_casa - prob_fora
        
        # Garantir valores positivos
        prob_empate = max(15, prob_empate)
        ajuste = (100 - prob_casa - prob_fora - prob_empate) / 2
        prob_casa += ajuste
        prob_fora += ajuste
    
    return {
        "prob_casa": round(prob_casa, 1),
        "prob_empate": round(prob_empate, 1),
        "prob_fora": round(prob_fora, 1),
        "media_pontos_casa": round(media_pontos_casa, 2),
        "media_pontos_fora": round(media_pontos_fora, 2)
    }

# ---------------------- ÁREA DE ENTRADA DE DADOS ----------------------
st.header("📊 Dados dos Times")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏠 Time da Casa")
    nome_casa = st.text_input("Nome do Time", value="Time da Casa")
    pontos_casa = st.number_input("Pontos no Campeonato", min_value=0, value=15)
    jogos_casa = st.number_input("Quantidade de Jogos", min_value=1, value=10)

with col2:
    st.subheader("✈️ Time Visitante")
    nome_fora = st.text_input("Nome do Time", value="Time Visitante")
    pontos_fora = st.number_input("Pontos no Campeonato", min_value=0, value=12)
    jogos_fora = st.number_input("Quantidade de Jogos", min_value=1, value=10)

st.divider()

# ---------------------- BOTÃO DE CÁLCULO ----------------------
if st.button("🔍 Calcular Probabilidades", type="primary", use_container_width=True):
    resultado = calcular_probabilidades(pontos_casa, jogos_casa, pontos_fora, jogos_fora)
    
    st.subheader("📈 Resultados da Análise")
    
    # Cartões com os resultados
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(f"""
        <div class="metric-card" style="text-align:center">
            <h3 style="color:#00ff88">{nome_casa}</h3>
            <p style="font-size:28px; font-weight:bold; color:#00ff88">{resultado['prob_casa']}%</p>
            <p style="color:#cccccc">Pontos/Jogo: {resultado['media_pontos_casa']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with c2:
        st.markdown(f"""
        <div class="metric-card" style="text-align:center">
            <h3 style="color:#ffcc00">Empate</h3>
            <p style="font-size:28px; font-weight:bold; color:#ffcc00">{resultado['prob_empate']}%</p>
            <p style="color:#cccccc">Probabilidade</p>
        </div>
        """, unsafe_allow_html=True)
    
    with c3:
        st.markdown(f"""
        <div class="metric-card" style="text-align:center">
            <h3 style="color:#ff4444">{nome_fora}</h3>
            <p style="font-size:28px; font-weight:bold; color:#ff4444">{resultado['prob_fora']}%</p>
            <p style="color:#cccccc">Pontos/Jogo: {resultado['media_pontos_fora']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Determinar o palpite
    st.divider()
    max_prob = max(resultado['prob_casa'], resultado['prob_empate'], resultado['prob_fora'])
    
    if max_prob == resultado['prob_casa']:
        st.success(f"✅ **PALPITE: {nome_casa} VENCE** — {resultado['prob_casa']} de chance")
    elif max_prob == resultado['prob_fora']:
        st.success(f"✅ **PALPITE: {nome_fora} VENCE** — {resultado['prob_fora']} de chance")
    else:
        st.info(f"⚖️ **PALPITE: EMPATE** — {resultado['prob_empate']} de chance")

# ---------------------- INFORMAÇÕES ----------------------
st.divider()
st.info("ℹ️ **Como usar:** Insira os pontos totais e quantidade de jogos de cada time no campeonato. Quanto mais jogos inseridos, mais preciso o cálculo!")

st.caption("⚠️ Esta é uma ferramenta de análise estatística simples. Sempre analise outros fatores como desfalques, motivação e histórico.")