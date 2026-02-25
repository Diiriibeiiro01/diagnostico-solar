import streamlit as st
import urllib.parse

# --- CONFIGURAÇÕES FIXAS (DEFINIDAS POR MATEUS) ---
NOME_EMPRESA = "Nova Distrito"
TARIFA_FIXA = 0.95  
META_KWH_POR_PLACA = 70 
TELEFONE_SUPORTE = "5561982579348"

# Configuração da página e forçar tema claro via código
st.set_page_config(page_title=NOME_EMPRESA, page_icon="☀️", layout="centered")

# --- ESTILO VISUAL (FORÇANDO MODO CLARO E CORES DA MARCA) ---
st.markdown("""
    <style>
    /* Forçar cores de texto e fundo para evitar erro no modo escuro */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #f4f7f6 !important;
        color: #1e354e !important;
    }
    
    /* Cabeçalho Elegante */
    .cabecalho-custom {
        background-color: #1e354e;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .cabecalho-custom h1 {
        color: white !important;
        margin: 0;
        font-family: 'Arial', sans-serif;
        font-size: 2.2rem;
    }
    .cabecalho-custom p {
        color: #ffaa00 !important;
        margin: 5px 0 0 0;
        font-size: 1.1rem;
        font-weight: bold;
    }

    /* Estilo dos inputs para garantir visibilidade */
    input { color: #1e354e !important; }
    label { color: #1e354e !important; font-weight: bold !important; }

    /* Cartões de métricas */
    div[data-testid="metric-container"] {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
st.markdown(f"""
    <div class="cabecalho-custom">
        <h1>☀️ {NOME_EMPRESA}</h1>
        <p>Diagnóstico de Performance Solar</p>
    </div>
    """, unsafe_allow_html=True)

st.info(f"⚡ **Parâmetros Oficiais:** Tarifa R$ {TARIFA_FIXA:.2f}/kWh | Meta: {META_KWH_POR_PLACA}kWh mês/placa")

# --- ENTRADA DE DADOS ---
st.markdown("### 📝 Dados da Usina")
nome_cliente = st.text_input("Nome do Cliente ou Usina", placeholder="Ex: Residência Mateus")

col1, col2, col3 = st.columns(3)
with col1:
    modulos = st.number_input("Qtd de Placas", min_value=1, step=1)
with col2:
    dias = st.number_input("Dias de Uso", min_value=1, value=30)
with col3:
    geracao_real = st.number_input("Geração (kWh)", min_value=0.0, step=10.0)

st.write("") 

if st.button("CALCULAR DESEMPENHO", type="primary", use_container_width=True):
    if not nome_cliente:
        st.warning("Por favor, introduza o nome para o relatório.")
    else:
        meta_periodo = (META_KWH_POR_PLACA / 30) * modulos * dias
        eficiencia = (geracao_real / meta_periodo) * 100 if meta_periodo > 0 else 0
        perda_rs = max(0, meta_periodo - geracao_real) * TARIFA_FIXA

        st.markdown("---")
        st.markdown("### 📊 Resultado do Diagnóstico")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Eficiência", f"{eficiencia:.1f}%")
        c2.metric("Meta Esperada", f"{meta_periodo:.1f} kWh")
        c3.metric("Economia Perdida", f"R$ {perda_rs:.2f}")

        if eficiencia >= 90:
            status = "✅ EXCELENTE"
            st.success(f"**{status}**\n\nOlá {nome_cliente}, a sua usina está produzindo exatamente como esperado!")
        elif eficiencia >= 80:
            status = "🚨 ALERTA (Sujeira/Clima)"
            st.warning(f"**{status}**\n\nA sua usina perdeu {(100-eficiencia):.1f}% de eficiência. Sugerimos uma limpeza nos painéis.")
        else:
            status = "💀 CRÍTICO (Falha Técnica)"
            st.error(f"**{status}**\n\nAtenção! Perda superior a 20%. Verifique o inversor ou contate o suporte.")

        # --- BOTÃO WHATSAPP ---
        msg = f"Olá! Sou {nome_cliente} e acabei de analisar a minha usina no site da {NOME_EMPRESA}.\n\n📊 *Resultado:*\n- Eficiência: {eficiencia:.1f}%\n- Perda Estimada: R$ {perda_rs:.2f}\n- Status: {status}"
        url = f"https://wa.me/{TELEFONE_SUPORTE}?text={urllib.parse.quote(msg)}"
        
        st.markdown(f'''
            <br>
            <a href="{url}" target="_blank" style="text-decoration: none;">
                <div style="background-color:#f5a623; color:white; padding:15px; border-radius:8px; text-align:center; font-weight:bold; font-size:16px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    💬 ENVIAR RESULTADO PARA O SUPORTE TÉCNICO
                </div>
            </a>
        ''', unsafe_allow_html=True)

st.markdown("---")
st.markdown(f"<p style='text-align: center; color: gray; font-size: 12px;'>© 2026 {NOME_EMPRESA} - Todos os direitos reservados.</p>", unsafe_allow_html=True)
