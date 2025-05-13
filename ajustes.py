import pandas as pd
import streamlit as st

@st.cache_data
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

def preprocessar_dados(df):
    """
    Pré-processa os dados carregados do Excel.
    
    Args:
        df (pd.DataFrame): DataFrame com os dados brutos.
    
    Returns:
        pd.DataFrame: DataFrame pré-processado.
    """
    # Verificar se existem colunas que começam com "D"
    colunas_relevantes = [col for col in df.columns if col.startswith("D")]
    if not colunas_relevantes:
        raise ValueError("Nenhuma coluna de dezenas encontrada no DataFrame.")
    
    return df[colunas_relevantes]