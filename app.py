import streamlit as st

# Configuração da Página
st.set_page_config(page_title="Monitoramento Solar Pro", page_icon="☀️", layout="centered")

# Estilização
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .main-card { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("☀️ Diagnóstico Solar Inteligente")
st.write("Analise a performance da sua usina em tempo real.")

# Sidebar para configurações de tarifa
with st.sidebar:
    st.header("⚙️ Configurações")
    valor_kwh = st.number_input("Preço do kWh (R$)", value=0.95, step=0.05)
    st.caption("Este valor define o cálculo do prejuízo financeiro.")

# Form de Entrada de Dados
with st.container():
    st.subheader("Dados da Usina")
    nome = st.text_input("Nome do Cliente ou Usina")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        modulos = st.number_input("Nº de Módulos", min_value=1, step=1)
    with col2:
        dias = st.number_input("Dias Analisados", min_value=1, value=30)
    with col3:
        geracao = st.number_input("Geração Real (kWh)", min_value=0.0)

if st.button("ANALISAR AGORA"):
    if not nome:
        st.warning("Por favor, digite o nome do cliente.")
    else:
        # --- LÓGICA DE CÁLCULO ---
        meta_ideal = (70 / 30) * modulos * dias
        eficiencia = (geracao / meta_ideal) * 100 if meta_ideal > 0 else 0
        perda_rs = max(0, meta_ideal - geracao) * valor_kwh

        st.divider()
        st.subheader(f"📊 Relatório: {nome}")
        
        # Métricas visuais
        m1, m2, m3 = st.columns(3)
        m1.metric("Eficiência", f"{eficiencia:.1f}%")
        m2.metric("Meta", f"{meta_ideal:.1f} kWh")
        m3.metric("Perda", f"R$ {perda_rs:.2f}", delta_color="inverse")

        # --- DIAGNÓSTICO AUTOMÁTICO (Sua regra de 20%) ---
        if eficiencia >= 90:
            st.success("### Status: ✅ EXCELENTE")
            st.write("**Análise:** O sistema está saudável. Continue acompanhando!")
            
        elif eficiencia >= 80:
            st.warning("### Status: 🚨 ALERTA (Sujeira ou Clima)")
            st.write(f"**Análise:** Perda de {(100-eficiencia):.1f}%. É provável que os módulos estejam sujos ou houve muita chuva no período.")
            
        else:
            st.error("### Status: 💀 CRÍTICO (Falha Técnica)")
            st.write("**Análise:** Perda superior a 20%. Provável problema no inversor, disjuntor ou queda de string. Recomenda-se visita técnica urgente!")

        # Dica de economia
        if perda_rs > 0:
            st.info(f"💡 **Atenção:** Se o problema persistir, você deixará de economizar cerca de **R$ {perda_rs * (30/dias):.2f}** por mês.")