import streamlit as st
import urllib.parse
import random

# --- CONFIGURAÇÕES FIXAS (MATEUS - NOVA DISTRITO) ---
NOME_EMPRESA = "Nova Distrito"
SUBTITULO = "Monitoramento Solar"
TARIFA_FIXA = 0.95  
META_KWH_POR_PLACA = 70 
TELEFONE_SUPORTE = "5561982579348"

st.set_page_config(page_title=NOME_EMPRESA, layout="centered")

# --- ESTILO CSS DINÂMICO ---
st.markdown("""
    <style>
    /* Estilização do Título com Gradiente */
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

    /* Estilo dos Cartões de Métrica */
    div[data-testid="metric-container"] {
        background-color: rgba(120, 120, 120, 0.1);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(243, 156, 18, 0.3);
    }

    /* Botão de Calcular Colorido */
    .stButton>button {
        background: linear-gradient(135deg, #f39c12 0%, #d35400 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        height: 50px !important;
        width: 100% !important;
        border-radius: 8px !important;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(211, 84, 0, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
st.markdown(f'<h1 class="main-title">{NOME_EMPRESA}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-title">{SUBTITULO}</p>', unsafe_allow_html=True)

# --- ENTRADA DE DADOS (FORA DE FORM PARA NÃO BUGAR) ---
st.markdown("### Diagnóstico Técnico")
nome_cliente = st.text_input("Identificação da Unidade", placeholder="Ex: Residência Mateus")

col1, col2, col3 = st.columns(3)
with col1:
    modulos = st.number_input("Quantidade de Painéis", min_value=1, step=1)
with col2:
    dias = st.number_input("Período de Análise (Dias)", min_value=1, value=30)
with col3:
    geracao_real = st.number_input("Geração Real (kWh)", min_value=0.0)

# Espaçamento
st.write("")

if st.button("CALCULAR PERFORMANCE"):
    if not nome_cliente:
        st.error("Por favor, preencha a identificação da unidade.")
    else:
        # Cálculos Técnicos
        meta_periodo = (META_KWH_POR_PLACA / 30) * modulos * dias
        eficiencia = (geracao_real / meta_periodo) * 100 if meta_periodo > 0 else 0
        perda_rs = max(0, meta_periodo - geracao_real) * TARIFA_FIXA
        protocolo = random.randint(10000, 99999)

        st.markdown("---")
        st.markdown(f"### Resultado: {nome_cliente}")
        st.write(f"Protocolo de Atendimento: {protocolo}")

        # Grid de Resultados Coloridos
        res1, res2, res3 = st.columns(3)
        res1.metric("Eficiência", f"{eficiencia:.1f}%")
        res2.metric("Meta Esperada", f"{meta_periodo:.1f} kWh")
        res3.metric("Perda Estimada", f"R$ {perda_rs:.2f}", delta=f"-R$ {perda_rs:.2f}" if perda_rs > 0 else None, delta_color="inverse")

        # Status com Cores de Destaque
        if eficiencia >= 90:
            st.info(f"STATUS: EXCELENTE - A usina está operando em alta performance.")
            status_txt = "EXCELENTE"
        elif eficiencia >= 80:
            st.warning(f"STATUS: ALERTA - Performance abaixo do esperado. Recomendada verificação.")
            status_txt = "ALERTA"
        else:
            st.error(f"STATUS: CRÍTICO - Perda de geração severa detectada.")
            status_txt = "CRÍTICO"

        # --- MENSAGEM WHATSAPP ---
        msg = (
            f"DIAGNÓSTICO NOVA DISTRITO\n"
            f"Protocolo: {protocolo}\n"
            f"Unidade: {nome_cliente}\n\n"
            f"DADOS:\n"
            f"- Eficiência: {eficiencia:.1f}%\n"
            f"- Geração: {geracao_real} kWh\n"
            f"- Perda: R$ {perda_rs:.2f}\n\n"
            f"STATUS: {status_txt}\n\n"
            f"Olá Mateus, gostaria de agendar o suporte para esta unidade."
        )
        
        link_wa = f"https://wa.me/{TELEFONE_SUPORTE}?text={urllib.parse.quote(msg)}"
        
        st.markdown(f'''
            <a href="{link_wa}" target="_blank" style="text-decoration: none;">
                <div style="background: #25D366; color: white; padding: 15px; border-radius: 8px; text-align: center; font-weight: bold; font-size: 1.2rem; margin-top: 20px; box-shadow: 0 4px 10px rgba(37, 211, 102, 0.3);">
                    ENVIAR PARA SUPORTE TÉCNICO
                </div>
            </a>
        ''', unsafe_allow_html=True)

st.markdown("---")
st.markdown(f"<p style='text-align: center; opacity: 0.6;'>{NOME_EMPRESA} - Todos os direitos reservados © 2026</p>", unsafe_allow_html=True)
