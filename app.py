import streamlit as st
import urllib.parse

# --- CONFIGURAÇÕES FIXAS (O CLIENTE NÃO MEXE) ---
TARIFA_FIXA = 0.95  # Altere aqui o valor oficial da sua região
META_KWH_POR_PLACA = 70 

st.set_page_config(page_title="Distrito Solar - Diagnóstico", page_icon="☀️")

# --- ESTILO VISUAL ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #f4f7f6; }}
    .status-box {{ padding: 20px; border-radius: 10px; color: white; font-weight: bold; margin-bottom: 20px; }}
    </style>
    """, unsafe_allow_html=True)

st.title("☀️ Calculadora de Performance Distrito Solar")
st.info(f"ℹ️ Parâmetros Oficiais: Tarifa base R$ {TARIFA_FIXA:.2f}/kWh | Meta: {META_KWH_POR_PLACA}kWh mês/placa")

# --- ENTRADA DE DADOS DO CLIENTE ---
with st.container():
    st.subheader("📝 Dados da sua Usina")
    nome = st.text_input("Seu Nome ou Nome da Usina")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        modulos = st.number_input("Qtd de Placas", min_value=1, step=1, help="Número total de painéis instalados.")
    with col2:
        dias = st.number_input("Dias de Uso", min_value=1, value=30, help="Período que você está analisando.")
    with col3:
        geracao_real = st.number_input("Geração no Inversor (kWh)", min_value=0.0)

if st.button("CALCULAR DESEMPENHO"):
    if not nome:
        st.warning("Por favor, digite o seu nome para o relatório.")
    else:
        # --- CÁLCULO BLINDADO ---
        meta_periodo = (META_KWH_POR_PLACA / 30) * modulos * dias
        eficiencia = (geracao_real / meta_periodo) * 100 if meta_periodo > 0 else 0
        perda_rs = max(0, meta_periodo - geracao_real) * TARIFA_FIXA

        st.markdown("---")
        
        # --- EXIBIÇÃO DE RESULTADOS ---
        c1, c2, c3 = st.columns(3)
        c1.metric("Eficiência", f"{eficiencia:.1f}%")
        c2.metric("Meta Esperada", f"{meta_periodo:.1f} kWh")
        c3.metric("Economia Perdida", f"R$ {perda_rs:.2f}")

        # --- DIAGNÓSTICO AUTOMÁTICO ---
        if eficiencia >= 90:
            st.success(f"### Status: ✅ EXCELENTE\nSua usina está operando perfeitamente, {nome}!")
        elif eficiencia >= 80:
            st.warning(f"### Status: 🚨 ALERTA (Sujeira ou Tempo)\nSua usina perdeu {(100-eficiencia):.1f}% de eficiência. Recomendamos uma limpeza nos painéis.")
        else:
            st.error(f"### Status: 💀 CRÍTICO (Falha Técnica)\nAtenção! Perda grave detectada. Pode haver falha no inversor ou disjuntor desligado.")

        # --- BOTÃO WHATSAPP ---
        msg = f"Olá! Fiz o diagnóstico da usina {nome}:\n- Eficiência: {eficiencia:.1f}%\n- Perda: R$ {perda_rs:.2f}\n- Status: {status if 'status' in locals() else ''}"
        url = f"https://wa.me/5561982579348?text={urllib.parse.quote(msg)}" # COLOQUE SEU NUMERO AQUI
        
        st.markdown(f'''
            <a href="{url}" target="_blank">
                <button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:8px; font-weight:bold; cursor:pointer;">
                    💬 ENVIAR RESULTADO PARA SUPORTE TÉCNICO
                </button>
            </a>
        ''', unsafe_allow_html=True)

