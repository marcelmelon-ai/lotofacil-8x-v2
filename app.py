import streamlit as st
import os
import sys
import logging
import pandas as pd
from typing import Optional, Tuple, Dict

# ====== IMPORTAÇÕES INTERNAS ======
from maquininha import maquininha
from layout import menu_lateral
from ajustes import carregar_dados_excel
from inteligencia import aplicar_ia_para_jogos
from modelos import gerar_jogos_otimizados, treinar_modelo_xgb, prever_dezenas
from estatisticas import mostrar_dashboard_estatistico

# ====== IMPORTAÇÃO DAS PÁGINAS ======
from paginas.gerador import pagina_gerador
from paginas.estatisticas import pagina_estatisticas
from paginas.ia import pagina_ia
from paginas.dados_online import pagina_dados_online
from paginas.sobre import pagina_sobre

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== CONFIGURAÇÃO INICIAL DO STREAMLIT ======
st.set_page_config(page_title="🎯 Lotofácil 8X", layout="wide")
st.markdown("<h1 style='text-align: center; color: #6C63FF;'>🎯 Lotofácil 8X - Geração Inteligente</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>App com estatísticas + inteligência artificial</h4><br>", unsafe_allow_html=True)

# ====== MENU DE NAVEGAÇÃO ======
pagina = menu_lateral()

# ====== EXECUÇÃO DA PÁGINA SELECIONADA ======
if pagina == "🎰 Gerador de Jogos":
    pagina_gerador()
elif pagina == "📊 Estatísticas":
    pagina_estatisticas()
elif pagina == "🧠 IA e Previsões":
    pagina_ia()
elif pagina == "📁 Dados Online":
    pagina_dados_online()
elif pagina == "ℹ️ Sobre":
    pagina_sobre()

# ====== UPLOAD DO ARQUIVO EXCEL ======
st.sidebar.markdown("---")
st.sidebar.subheader("Envio de Dados")
uploaded_file = st.sidebar.file_uploader("Envie o arquivo Excel da Lotofácil", type=["xlsx"])

# ====== FUNÇÃO PARA PROCESSAR UPLOAD ======
def processa_upload(uploaded_file) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame], Optional[Dict[str, pd.DataFrame]]]:
    try:
        logger.info("📂 Processando arquivo Excel enviado pelo usuário...")
        X, y, estatisticas = maquininha(uploaded_file)
        return X, y, estatisticas
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
        logger.error(f"Erro no processamento do arquivo: {e}")
        return None, None, None

# ====== EXECUÇÃO DO PROCESSAMENTO DOS DADOS ======
if uploaded_file is not None:
    X, y, estatisticas = processa_upload(uploaded_file)

    if X is not None and y is not None:
        st.subheader("🧠 Características de Entrada para IA")
        st.write(X.head())

        st.subheader("🎯 Rótulos para IA")
        st.write(y[:10])

        st.subheader("📋 Tabelas Estatísticas da Numeromania")
        for nome, tabela in estatisticas.items():
            with st.expander(f"{nome}"):
                st.dataframe(tabela)

        try:
            modelo, acuracia = aplicar_ia_para_jogos(X, y)
            st.success(f"Acurácia do modelo: {acuracia:.2%}")
        except Exception as e:
            st.error(f"Erro ao treinar o modelo: {e}")
else:
    st.sidebar.info("📤 Envie um arquivo Excel válido para análise.")

# ====== AJUSTE DE CAMINHO PARA COMPATIBILIDADE ======
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
