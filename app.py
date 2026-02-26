import streamlit as st
import urllib.parse
import random

# --- CONFIGURAÇÕES FIXAS (NOVA DISTRITO) ---
NOME_EMPRESA = "Nova Distrito"
SUBTITULO = "Monitoramento Solar"
TARIFA_FIXA = 0.95  
META_KWH_POR_PLACA = 70 
TELEFONE_SUPORTE = "5561982579348"

st.set_page_config(page_title=NOME_EMPRESA, layout="centered")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    .main-title {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 0;
    }
    .sub-title {
        color: #f39c12;
        text-align: center;
        font-weight: 600;
        letter-spacing: 4px;
        text-transform: uppercase;
        font-size: 1rem;
        margin-bottom: 30px;
    }
    div[data-testid="metric-container"] {
        background-color: rgba(120, 120, 120, 0.05);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(243, 156, 18, 0.2);
    }
    .stButton>button {
        background: linear-gradient(135deg, #f39c12 0%, #d35400 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        height: 50px !important;
        width: 100% !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown(f'<h1 class="main-title">{NOME_EMPRESA}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-title">{SUBTITULO}</p>', unsafe_allow_html=True)

# --- INPUTS ---
st.markdown("### Diagnóstico Técnico")
nome_cliente = st.text_input("Identificação da Unidade", placeholder="Ex: Residência Mateus")

col1, col2, col3 = st.columns(3)
with col1:
    modulos = st.number_input("Quantidade de Painéis", min_value=1, step=1)
with col2:
    dias = st.number_input("Período (Dias)", min_value=1, value=30)
with col3:
    geracao_real = st.number_input("Geração Real (kWh)", min_value=0.0)

if st.button("ANALISAR PERFORMANCE"):
    if not nome_cliente:
        st.error("Por favor, preencha a identificação da unidade.")
    else:
        # Cálculos
        meta_periodo = (META_KWH_POR_PLACA / 30) * modulos * dias
        eficiencia = (geracao_real / meta_periodo) * 100 if meta_periodo > 0 else 0
        perda_rs = max(0, meta_periodo - geracao_real) * TARIFA_FIXA
        protocolo = random.randint(10000, 99999)

        st.markdown("---")
        st.markdown(f"### Resultado: {nome_cliente}")
        st.write(f"Protocolo: {protocolo}")

        res1, res2, res3 = st.columns(3)
        res1.metric("Eficiência", f"{eficiencia:.1f}%")
        res2.metric("Meta", f"{meta_periodo:.1f} kWh")
        res3.metric("Perda", f"R$ {perda_rs:.2f}")

        # --- LÓGICA DE MENSAGEM DINÂMICA ---
        if eficiencia >= 90:
            status_txt = "EXCELENTE"
            st.info(f"STATUS: {status_txt} - Sistema operando em alta performance.")
            texto_personalizado = "Minha usina está com ótimo desempenho, mas gostaria de manter o acompanhamento preventivo da Nova Distrito."
        
        elif eficiencia >= 80:
            status_txt = "ALERTA"
            st.warning(f"STATUS: {status_txt} - Performance abaixo do esperado.")
            texto_personalizado = f"Minha usina apresentou um alerta de performance ({eficiencia:.1f}%). Preciso de uma avaliação para identificar se é sujeira ou sombreamento."
        
        else:
            status_txt = "CRÍTICO"
            st.error(f"STATUS: {status_txt} - Perda severa detectada.")
            texto_personalizado = f"URGENTE: Minha usina está com desempenho CRÍTICO ({eficiencia:.1f}%). Preciso de suporte técnico imediato para verificar possíveis falhas."

        # Montagem da mensagem final
        msg = (
            f"DIAGNÓSTICO NOVA DISTRITO\n"
            f"Protocolo: {protocolo}\n"
            f"Unidade: {nome_cliente}\n\n"
            f"DADOS TÉCNICOS:\n"
            f"- Eficiência: {eficiencia:.1f}%\n"
            f"- Perda: R$ {perda_rs:.2f}\n"
            f"- Status: {status_txt}\n\n"
            f"{texto_personalizado}"
        )
        
        link_wa = f"https://wa.me/{TELEFONE_SUPORTE}?text={urllib.parse.quote(msg)}"
        
        st.markdown(f'''
            <a href="{link_wa}" target="_blank" style="text-decoration: none;">
                <div style="background: #25D366; color: white; padding: 15px; border-radius: 8px; text-align: center; font-weight: bold; font-size: 1.2rem; margin-top: 20px;">
                    ENVIAR PARA SUPORTE TÉCNICO
                </div>
            </a>
        ''', unsafe_allow_html=True)

st.markdown("---")
st.markdown(f"<p style='text-align: center; opacity: 0.6;'>{NOME_EMPRESA} - Todos os direitos reservados © 2026</p>", unsafe_allow_html=True)
