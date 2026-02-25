import streamlit as st
import urllib.parse
import random
import time

# --- CONFIGURAÇÕES FIXAS (MATEUS - NOVA DISTRITO) ---
NOME_EMPRESA = "Nova Distrito"
SUBTITULO = "Monitoramento Solar"
TARIFA_FIXA = 0.95  
META_KWH_POR_PLACA = 70 
TELEFONE_SUPORTE = "5561982579348"

st.set_page_config(page_title=NOME_EMPRESA, layout="centered")

# --- ESTILO CSS AVANÇADO ---
st.markdown("""
    <style>
    /* Forçar Modo Claro */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #f0f2f6 !important;
        color: #1e354e !important;
    }
    
    /* Cabeçalho Minimalista Profissional */
    .header-box {
        background-color: #1e354e;
        padding: 3rem 1rem;
        border-radius: 4px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .header-box h1 { 
        color: white !important; 
        font-size: 3rem !important; 
        margin: 0; 
        letter-spacing: -1px;
    }
    .header-box p { 
        color: #ffaa00 !important; 
        font-size: 1.2rem; 
        text-transform: uppercase; 
        letter-spacing: 2px;
        margin-top: 10px;
    }

    /* Cards de Resultado */
    .result-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1e354e;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-top: 20px;
    }

    /* Botão Customizado */
    .stButton>button {
        background-color: #1e354e !important;
        color: white !important;
        border-radius: 4px !important;
        border: none !important;
        height: 3.5em !important;
        font-weight: 600 !important;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown(f"""
    <div class="header-box">
        <h1>{NOME_EMPRESA}</h1>
        <p>{SUBTITULO}</p>
    </div>
    """, unsafe_allow_html=True)

# --- INPUTS ---
st.markdown("### Dados de Análise")
nome_cliente = st.text_input("Identificação da Unidade", placeholder="Nome do cliente")

col1, col2, col3 = st.columns(3)
with col1:
    modulos = st.number_input("Painéis", min_value=1, step=1)
with col2:
    dias = st.number_input("Dias", min_value=1, value=30)
with col3:
    geracao_real = st.number_input("Geração (kWh)", min_value=0.0)

# Criando um espaço vazio para a âncora do scroll
placeholder_resultado = st.empty()

if st.button("ANALISAR DESEMPENHO"):
    if not nome_cliente:
        st.error("Por favor, preencha a identificação.")
    else:
        with st.spinner('Processando dados...'):
            time.sleep(0.8)

        # Cálculos
        meta_periodo = (META_KWH_POR_PLACA / 30) * modulos * dias
        eficiencia = (geracao_real / meta_periodo) * 100 if meta_periodo > 0 else 0
        perda_rs = max(0, meta_periodo - geracao_real) * TARIFA_FIXA
        protocolo = random.randint(1000, 9999)

        # Conteúdo do Resultado
        with placeholder_resultado.container():
            st.markdown("---")
            st.markdown(f"### Relatório: {nome_cliente}")
            st.caption(f"Protocolo: {protocolo}")
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Eficiência", f"{eficiencia:.1f}%")
            c2.metric("Meta", f"{meta_periodo:.1f} kWh")
            c3.metric("Perda", f"R$ {perda_rs:.2f}", delta=f"-{perda_rs:.2f}" if perda_rs > 0 else None, delta_color="inverse")

            if eficiencia >= 90:
                st.success(f"Status: EXCELENTE | Sistema operando dentro da meta.")
                status_txt = "EXCELENTE"
            elif eficiencia >= 80:
                st.warning(f"Status: ALERTA | Necessário verificar limpeza dos módulos.")
                status_txt = "ALERTA"
            else:
                st.error(f"Status: CRÍTICO | Possível falha técnica detectada.")
                status_txt = "CRÍTICO"

            # Botão de Suporte
            msg = f"Olá! Sou {nome_cliente}. Analisei minha usina na Nova Distrito (Prot: {protocolo})\n\nResultado:\n- Eficiência: {eficiencia:.1f}%\n- Status: {status_txt}"
            url = f"https://wa.me/{TELEFONE_SUPORTE}?text={urllib.parse.quote(msg)}"
            
            st.markdown(f'''
                <a href="{url}" target="_blank" style="text-decoration: none;">
                    <div style="background-color:#ffaa00; color:#1e354e; padding:18px; border-radius:4px; text-align:center; font-weight:bold; font-size:1.1rem; border: 1px solid #1e354e;">
                        ACIONAR SUPORTE TÉCNICO
                    </div>
                </a>
            ''', unsafe_allow_html=True)
            
            # Script de scroll que funciona em qualquer navegador/dispositivo
            st.components.v1.html(
                f"<script>window.parent.document.getElementById('resultado').scrollIntoView({{behavior: 'smooth'}});</script>",
                height=0
            )

st.markdown("<br><br><br><div id='resultado'></div>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: #7f8c8d; font-size: 0.8rem;'>{NOME_EMPRESA} - Todos os direitos reservados © 2026</p>", unsafe_allow_html=True)
