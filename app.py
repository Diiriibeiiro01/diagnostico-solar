import streamlit as st
import urllib.parse
import random
import time

# --- CONFIGURAÇÕES FIXAS (MATEUS - NOVA DISTRITO) ---
NOME_EMPRESA = "Nova Distrito"
TARIFA_FIXA = 0.95  
META_KWH_POR_PLACA = 70 
TELEFONE_SUPORTE = "5561982579348"

st.set_page_config(page_title=NOME_EMPRESA, page_icon="☀️", layout="centered")

# --- ESTILO CSS ---
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
    .header-container h1 { color: white !important; font-size: 2.5rem !important; margin: 0; }
    .header-container p { color: #ffaa00 !important; font-size: 1.1rem; font-weight: 500; }
    
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
        <h1>{NOME_EMPRESA}</h1>
        <p>Monitoramento de Usinas Solares</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("### 📊 Iniciar Análise")

# --- ENTRADA DE DADOS ---
nome_cliente = st.text_input("Identificação (Nome ou Unidade)", placeholder="Ex: Residência Mateus")
col1, col2, col3 = st.columns(3)
with col1:
    modulos = st.number_input("Nº de Placas", min_value=1, step=1)
with col2:
    dias = st.number_input("Dias de Análise", min_value=1, value=30)
with col3:
    geracao_real = st.number_input("Geração (kWh)", min_value=0.0)

btn_calcular = st.button("GERAR DIAGNÓSTICO TÉCNICO")

if btn_calcular:
    if not nome_cliente:
        st.error("⚠️ Identifique a unidade para continuar.")
    else:
        # Simulação de carregamento para dar efeito de análise
        with st.spinner('Analisando dados de telemetria...'):
            time.sleep(1)

        # Cálculos
        meta_periodo = (META_KWH_POR_PLACA / 30) * modulos * dias
        eficiencia = (geracao_real / meta_periodo) * 100 if meta_periodo > 0 else 0
        perda_rs = max(0, meta_periodo - geracao_real) * TARIFA_FIXA
        protocolo = random.randint(1000, 9999)

        # RESULTADO (O Streamlit foca automaticamente no novo conteúdo gerado)
        st.markdown("---")
        st.subheader(f"📋 Relatório: {nome_cliente}")
        st.caption(f"Protocolo de Atendimento: #{protocolo}")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Eficiência Real", f"{eficiencia:.1f}%")
        m2.metric("Meta do Período", f"{meta_periodo:.1f} kWh")
        m3.metric("Perda Financeira", f"R$ {perda_rs:.2f}", delta=f"-{perda_rs:.2f}" if perda_rs > 0 else None, delta_color="inverse")

        st.progress(min(eficiencia/100, 1.0))

        if eficiencia >= 90:
            status = "✅ EXCELENTE"
            st.success(f"**Status: {status}** \nSistema operando com alta performance.")
        elif eficiencia >= 80:
            status = "🚨 ALERTA"
            st.warning(f"**Status: {status}** \nDesvio de performance detectado. Sugerimos limpeza técnica.")
        else:
            status = "💀 CRÍTICO"
            st.error(f"**Status: {status}** \nPerda grave detectada! Verifique o sistema ou acione o suporte.")

        # --- BOTÃO WHATSAPP ---
        msg = f"Olá! Sou {nome_cliente}.\nFiz a análise na Nova Distrito (Prot: #{protocolo})\n\n📊 *Diagnóstico:*\n- Eficiência: {eficiencia:.1f}%\n- Perda: R$ {perda_rs:.2f}\n- Status: {status}"
        url = f"https://wa.me/{TELEFONE_SUPORTE}?text={urllib.parse.quote(msg)}"
        
        st.markdown(f'''
            <br>
            <a href="{url}" target="_blank" style="text-decoration: none;">
                <div style="background-color:#ffaa00; color:#1e354e; padding:18px; border-radius:10px; text-align:center; font-weight:bold; font-size:18px; box-shadow: 0 4px 15px rgba(255,170,0,0.3); border: 2px solid #1e354e;">
                    💬 ACIONAR SUPORTE TÉCNICO AGORA
                </div>
            </a>
        ''', unsafe_allow_html=True)
        
        # Comando para forçar o scroll até o final da página
        st.components.v1.html(
            f"<script>window.parent.document.querySelector('section.main').scrollTo(0, 1000);</script>",
            height=0
        )

st.markdown("---")
st.markdown(f"<p style='text-align: center; color: #7f8c8d;'>{NOME_EMPRESA} - Todos os direitos reservados © 2026</p>", unsafe_allow_html=True)
