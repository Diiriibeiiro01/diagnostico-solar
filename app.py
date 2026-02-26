import streamlit as st
import urllib.parse
import random

# --- CONFIGURAÇÕES FIXAS (BY MATEUS - NOVA DISTRITO) ---
NOME_EMPRESA = "Nova Distrito"
SUBTITULO = "Monitoramento Solar"
TARIFA_FIXA = 0.95  
META_KWH_POR_PLACA = 70 
TELEFONE_SUPORTE = "5561982579348"

st.set_page_config(page_title=NOME_EMPRESA, layout="centered")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #f4f7f6 !important;
        color: #1e354e !important;
    }
    .header-box {
        background-color: #1e354e;
        padding: 3rem 1rem;
        text-align: center;
        margin-bottom: 2rem;
        border-bottom: 4px solid #ffaa00;
    }
    .header-box h1 { color: white !important; font-size: 2.8rem !important; margin: 0; font-weight: 800; }
    .header-box p { color: #ffaa00 !important; font-size: 1.1rem; margin-top: 5px; font-weight: 600; }
    .stButton>button {
        background-color: #1e354e !important;
        color: white !important;
        border-radius: 4px !important;
        height: 3em !important;
        font-weight: bold !important;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown(f'<div class="header-box"><h1>{NOME_EMPRESA}</h1><p>{SUBTITULO}</p></div>', unsafe_allow_html=True)

nome_cliente = st.text_input("Identificação da Unidade", placeholder="Nome do cliente")
col1, col2, col3 = st.columns(3)
with col1: modulos = st.number_input("Número de Placas", min_value=1, step=1)
with col2: dias = st.number_input("Período (Dias)", min_value=1, value=30)
with col3: geracao_real = st.number_input("Geração Real (kWh)", min_value=0.0)

if st.button("GERAR RELATÓRIO TÉCNICO"):
    if not nome_cliente:
        st.error("Identifique a unidade antes de prosseguir.")
    else:
        meta_periodo = (META_KWH_POR_PLACA / 30) * modulos * dias
        eficiencia = (geracao_real / meta_periodo) * 100 if meta_periodo > 0 else 0
        perda_rs = max(0, meta_periodo - geracao_real) * TARIFA_FIXA
        protocolo = random.randint(1000, 9999)

        st.markdown("---")
        st.markdown(f"### Resultado: {nome_cliente}")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Eficiência", f"{eficiencia:.1f}%")
        m2.metric("Meta", f"{meta_periodo:.1f} kWh")
        m3.metric("Perda", f"R$ {perda_rs:.2f}")

        if eficiencia >= 90: status_whats = "✅ EXCELENTE"; st.success(f"Status: {status_whats}")
        elif eficiencia >= 80: status_whats = "🚨 ALERTA"; st.warning(f"Status: {status_whats}")
        else: status_whats = "💀 CRÍTICO"; st.error(f"Status: {status_whats}")

        # --- MENSAGEM DO WHATSAPP APRIMORADA ---
        # Note o uso de asteriscos para negrito e quebras de linha para organização
        msg = (
            f"*NOVA DISTRITO - SUPORTE TÉCNICO*\n"
            f"------------------------------------------\n"
            f"*Protocolo:* #{protocolo}\n"
            f"*Unidade:* {nome_cliente}\n\n"
            f"*DADOS DO DIAGNÓSTICO:*\n"
            f"• Eficiência Real: {eficiencia:.1f}%\n"
            f"• Geração Real: {geracao_real} kWh\n"
            f"• Meta Esperada: {meta_periodo:.1f} kWh\n"
            f"• Perda Estimada: R$ {perda_rs:.2f}\n\n"
            f"*STATUS:* {status_whats}\n"
            f"------------------------------------------\n"
            f"Olá, Mateus! Gostaria de solicitar o suporte de monitoramento para esta usina."
        )
        
        url = f"https://wa.me/{TELEFONE_SUPORTE}?text={urllib.parse.quote(msg)}"
        
        st.markdown(f'''
            <br>
            <a href="{url}" target="_blank" style="text-decoration: none;">
                <div style="background-color:#ffaa00; color:#1e354e; padding:18px; border-radius:4px; text-align:center; font-weight:bold; font-size:1.1rem; border: 1px solid #1e354e;">
                    ACIONAR SUPORTE TÉCNICO
                </div>
            </a>
        ''', unsafe_allow_html=True)

st.markdown("---")
st.markdown(f"<p style='text-align: center; color: #7f8c8d; font-size: 0.8rem;'>{NOME_EMPRESA} - Todos os direitos reservados © 2026</p>", unsafe_allow_html=True)
