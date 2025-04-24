import pandas as pd
import streamlit as st
from estatisticas import carregar_dados_excel


@st.cache_data
def calcular_frequencia(df):
    """
    Calcula a frequência de cada dezena em um DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame com os resultados da Lotofácil.
    
    Returns:
        pd.DataFrame: DataFrame com a frequência de cada dezena.
    """
    dezenas = df.filter(like="D").values.flatten()
    freq = pd.Series(dezenas).value_counts().sort_index().reset_index()
    freq.columns = ["Dezena", "Frequência"]
    freq["Dezena"] = freq["Dezena"].astype(str).str.zfill(2)
    return freq

def carregar_dados_excel(caminho_arquivo):
    """
    Carrega os dados de um arquivo Excel.

    Args:
        caminho_arquivo (str): Caminho para o arquivo Excel.

    Returns:
        pd.DataFrame: DataFrame com os dados carregados.
    """
    try:
        return pd.read_excel(caminho_arquivo)
    except FileNotFoundError:
        st.error(f"Arquivo não encontrado: {caminho_arquivo}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo Excel: {e}")
        return pd.DataFrame()
    
def mostrar_dashboard_estatistico(caminho_arquivo):
    """
    Exibe o dashboard estatístico com gráficos baseados nos dados do Excel.

    Args:
        caminho_arquivo (str): Caminho para o arquivo Excel com os resultados da Lotofácil.
    """
    st.title("📊 Dashboard de Estatísticas")
    st.write("Análise completa dos concursos anteriores.")

    # Carregar os dados do Excel
    df = carregar_dados_excel(caminho_arquivo)

    # Verificar se o DataFrame está vazio
    if df.empty:
        st.warning("⚠️ O arquivo Excel está vazio ou inválido. Por favor, carregue um arquivo válido.")
        return

    # Dividir a página em duas colunas
    col1, col2 = st.columns(2)

    with col1:
        # Calcular e exibir a frequência das dezenas
        freq = calcular_frequencia(df)
        st.subheader("Frequência das Dezenas")
        st.bar_chart(freq.set_index("Dezena")["Frequência"])

    with col2:
        # Placeholder para futuras funcionalidades
        st.subheader("Ocorrência por posição (em construção)")
        st.info("🔧 Essa funcionalidade está em desenvolvimento.")