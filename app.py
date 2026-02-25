import streamlit as st
import urllib.parse

st.set_page_config(page_title="Solar Expert Pro", page_icon="☀️")

# --- ESTILO E CABEÇALHO ---
st.title("☀️ Diagnóstico Solar Profissional")
st.markdown("---")

# --- ENTRADA DE DADOS ---
with st.expander("📝 Introduzir Dados da Usina", expanded=True):
    nome = st.text_input("Nome do Cliente")
    col1, col2 = st.columns(2)
    with col1:
        modulos = st.number_input("Nº de Painéis", min_value=1, step=1)
        geracao_real = st.number_input("Geração Real (kWh)", min_value=0.0)
    with col2:
        dias = st.number_input("Período (Dias)", min_value=1, value=30)
        valor_kwh = st.number_input("Tarifa Energia (R$)", value=0.90)

if st.button("GERAR ANÁLISE COMPLETA"):
    if not nome:
        st.error("Por favor, indique o nome.")
    else:
        # Lógica de cálculo
        meta = (70 / 30) * modulos * dias
        eficiencia = (geracao_real / meta) * 100
        perda_rs = max(0, meta - geracao_real) * valor_kwh
        
        # Diagnóstico
        if eficiencia >= 90:
            status, cor, msg = "EXCELENTE", "green", "Sistema operando perfeitamente."
        elif eficiencia >= 80:
            status, cor, msg = "ALERTA (SUJEIRA/CLIMA)", "orange", "Perda moderada. Provável necessidade de limpeza."
        else:
            status, cor, msg = "CRÍTICO (FALHA TÉCNICA)", "red", "Perda grave! Verifique inversor e disjuntores."

        # Exibição Visual
        st.subheader(f"📊 Resultado: {status}")
        st.metric("Eficiência", f"{eficiencia:.1f}%", delta=f"{eficiencia-100:.1f}%")
        
        st.write(f"**Análise técnica:** {msg}")
        st.write(f"**Prejuízo financeiro no período:** R$ {perda_rs:.2f}")

        # --- FUNÇÃO WHATSAPP ---
        texto_whats = f"Olá! Fiz o diagnóstico da usina {nome}:\nStatus: {status}\nEficiência: {eficiencia:.1f}%\nPrejuízo: R${perda_rs:.2f}\nPreciso de suporte técnico."
        texto_url = urllib.parse.quote(texto_whats)
        # Substitua o número abaixo pelo SEU número de telemóvel
        link_whats = f"https://wa.me/5561982579348?text={texto_url}"
        
        st.markdown(f"""
            <a href="{link_whats}" target="_blank">
                <button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">
                    💬 Enviar Resultado para Suporte Técnico
                </button>
            </a>
            """, unsafe_allow_html=True)
