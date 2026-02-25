import streamlit as st
import urllib.parse

# --- CONFIGURAÇÕES FIXAS (MATEUS - NOVA DISTRITO) ---
NOME_EMPRESA = "Nova Distrito"
TARIFA_FIXA = 0.95  
META_KWH_POR_PLACA = 70 
TELEFONE_SUPORTE = "5561982579348"

st.set_page_config(page_title=NOME_EMPRESA, page_icon="☀️", layout="centered")

# --- ESTILO CSS E ANIMAÇÃO ---
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #f8fafd !important;
        color: #1e354e !important;
    }
    
    .header-container {
        background: linear-gradient(135deg, #1e354e 0%, #2c4e70 100%);
        padding: 2.5rem 1rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .header-container h1 { color: white !important; font-size: 2.5rem !important; margin-bottom: 0; }
    .header-container p { color: #ffaa00 !important; font-size: 1.1rem; font-weight: 500; }

    div[data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 700 !important; }
    
    .stButton>button {
        background-color: #1e354e !important;
        color: white !important;
        border-radius: 8px !important;
        height: 3.5em !important;
        font-weight: bold !important;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown(f"""
    <div class="header-container">
        <h1>Nova Distrito</h1>
        <p>Monitoramento de Usinas Solares</p>
    </div>
    """, unsafe_allow_html=True)

# --- CORPO DO SITE ---
st.markdown("### 📊 Iniciar Análise")
st.info(f"Configuração Base: Tarifa R$ {TARIFA_FIXA:.2f} | Meta: {META_KWH_POR_PLACA}kWh/placa")

# Formulário de Entrada
with st.container():
    nome_cliente = st.text_input("Identificação (Nome ou Unidade)", placeholder="Ex: Residência Mateus")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        modulos = st.number_input("Nº de Placas", min_value=1, step=1)
    with col2:
        dias = st.number_input("Dias de Análise", min_value=1, value=30)
    with col3:
        geracao_real = st.number_input("Geração (kWh)", min_value=0.0)

    # Botão de Calcular
    btn_calcular = st.button("GERAR DIAGNÓSTICO TÉCNICO")

if btn_calcular:
    if not nome_cliente:
        st.error("⚠️ Identifique a unidade para continuar.")
    else:
        # Cálculos Técnicos
        meta_periodo = (META_KWH_POR_PLACA / 30) * modulos * dias
        eficiencia = (geracao_real / meta_periodo) * 100 if meta_periodo > 0 else 0
        perda_rs = max(0, meta_periodo - geracao_real) * TARIFA_FIXA

        # --- ANCORA PARA ANIMAÇÃO DE DESCER ---
        st.markdown('<div id="resultado"></div>', unsafe_allow_html=True)

        st.markdown("---")
        st.subheader(f"📋 Relatório: {nome_cliente}")
        
        # Métricas
        m1, m2, m3 = st.columns(3)
        m1.metric("Eficiência Real", f"{eficiencia:.1f}%")
        m2.metric("Meta do Período", f"{meta_periodo:.1f} kWh")
        m3.metric("Perda Financeira", f"R$ {perda_rs:.2f}", delta=f"-{perda_rs:.2f}" if perda_rs > 0 else None, delta_color="inverse")

        st.progress(min(eficiencia/100, 1.0))

        # Box de Diagnóstico
        if eficiencia >= 90:
            status = "✅ EXCELENTE"
            st.success(f"**Status: {status}** \nSistema operando com alta performance.")
        elif eficiencia >= 80:
            status = "🚨 ALERTA"
            st.warning(f"**Status: {status}** \nDesvio de performance detectado ({(100-eficiencia):.1f}%). Sugerimos limpeza técnica.")
        else:
            status = "💀 CRÍTICO"
            st.error(f"**Status: {status}** \nPerda grave detectada! Possível falha técnica no inversor ou strings.")

        # Botão WhatsApp Suporte
        msg = f"Olá! Sou {nome_cliente} e acabei de analisar minha usina na Nova Distrito.\n\n📈 *Diagnóstico:*\n- Eficiência: {eficiencia:.1f}%\n- Perda: R$ {perda_rs:.2f}\n- Status: {status}"
        url = f"https://wa.me/{TELEFONE_SUPORTE}?text={urllib.parse.quote(msg)}"
        
        st.markdown(f'''
            <br>
            <a href="{url}" target="_blank" style="text-decoration: none;">
                <div style="background-color:#ffaa00; color:#1e354e; padding:18px; border-radius:10px; text-align:center; font-weight:bold; font-size:18px; box-shadow: 0 4px 15px rgba(255,170,0,0.3); border: 2px solid #1e354e;">
                    💬 ACIONAR SUPORTE TÉCNICO AGORA
                </div>
            </a>
            <script>
                document.getElementById("resultado").scrollIntoView({{behavior: "smooth"}});
            </script>
        ''', unsafe_allow_html=True)

st.markdown("---")
st.markdown(f"<p style='text-align: center; color: #7f8c8d;'>Nova Distrito © 2026</p>", unsafe_allow_html=True)
