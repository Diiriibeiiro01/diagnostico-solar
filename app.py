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

# --- ESTILO CSS MODERNO E CLEAN ---
st.markdown("""
    <style>
    /* Reset e Fundo */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #fcfcfc !important;
        color: #2c3e50 !important;
        font-family: 'Inter', sans-serif;
    }

    /* Cabeçalho Minimalista */
    .header-main {
        background-color: #1a2a3a;
        padding: 40px 10px;
        text-align: center;
        border-radius: 4px;
        margin-bottom: 30px;
    }
    .header-main h1 {
        color: #ffffff !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .header-main p {
        color: #f39c12 !important;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-top: 8px;
        font-weight: 600;
    }

    /* Card de Conteúdo */
    .stForm {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 8px;
        border: 1px solid #edf2f7;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }

    /* Botão Principal Estilo Apple/SaaS */
    .stButton>button {
        background-color: #1a2a3a !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        width: 100%;
        height: 50px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2c3e50 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    /* Alertas Personalizados sem Emojis */
    .stAlert {
        border-radius: 6px !important;
        border: none !important;
        background-color: #f8f9fa !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown(f"""
    <div class="header-main">
        <h1>{NOME_EMPRESA}</h1>
        <p>{SUBTITULO}</p>
    </div>
    """, unsafe_allow_html=True)

# --- FORMULÁRIO DE ENTRADA ---
with st.form("analise_form"):
    st.markdown("### Analisar Unidade")
    nome_cliente = st.text_input("Identificação", placeholder="Digite o nome da unidade")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        modulos = st.number_input("Painéis", min_value=1, step=1)
    with c2:
        dias = st.number_input("Período (Dias)", min_value=1, value=30)
    with c3:
        geracao_real = st.number_input("Geração (kWh)", min_value=0.0)
    
    calcular = st.form_submit_button("GERAR RELATÓRIO")

# --- PROCESSAMENTO E RESULTADO ---
if calcular:
    if not nome_cliente:
        st.error("Identificação obrigatória.")
    else:
        meta = (META_KWH_POR_PLACA / 30) * modulos * dias
        eficiencia = (geracao_real / meta) * 100 if meta > 0 else 0
        perda_financeira = max(0, meta - geracao_real) * TARIFA_FIXA
        protocolo = random.randint(10000, 99999)

        st.markdown("---")
        st.markdown(f"### Resultado Técnico: {nome_cliente}")
        st.markdown(f"**Protocolo de Atendimento:** {protocolo}")

        r1, r2, r3 = st.columns(3)
